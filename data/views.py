import cv2
import json
import uuid
import matplotlib
from datetime import datetime
from rest_framework import status
from django.shortcuts import render
from datastore.datastore import DataStore
from .models import User, InvolvedIn, Session
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse as response, JsonResponse
from data.visualise import create_2D_visualisation, create_3D_visualisation

matplotlib.use('Agg')

def dashboard(request):
    user = request.user
    involvements = InvolvedIn.objects.filter(user=user)
    sessions = [inv.session for inv in involvements]
    context = {'sessions': sessions}
    return render(request, 'dashboard.html', context)


@csrf_exempt
def user_init(request):
    '''Initialise a new user.'''
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get user details from request data
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Generate a unique user id
        uid = str(uuid.uuid4())

        # Create and save new user
        new_user = User(uid, first_name, last_name)
        new_user.save()

        # Return a success response with the new user id
        return JsonResponse({'uid': uid}, status=201)

    # Handle non-POST requests
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def session_init(request):
    '''Initialise session metadata for a newly started session.'''
    data = json.loads(request.body)

    uids = data.get('uids')
    session = data.get('session')

    # First, ensure every user that is involved in this session exists
    users = User.objects.filter(id__in=uids)
    if len(users) != len(uids):
        return response("one or more invalid users provided", status=status.HTTP_401_UNAUTHORIZED)

    # Create and save new session
    new_sid = str(uuid.uuid4())
    new_session = Session(
        new_sid,
        session.get('name'),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session.get('description')
    )
    new_session.save()

    # Record each user as being involved in this session
    for user in users:
        InvolvedIn(id=str(uuid.uuid4()), user=user, session=new_session).save()

    return response(
        json.dumps({'sid': new_sid}),
        content_type="application/json",
        status=status.HTTP_200_OK
    )

# Decorator is just to mitigate some cookies problem that was preventing testing
@csrf_exempt
def frames_upload(request):
    '''Receive frame data from the frontend and store this data persistently in the backend.'''
    data = json.loads(request.body)

    uid = data.get('uid')
    sid = data.get('sid')
    clip_num = data.get('clipNum')
    session_finished = data.get('sessionFinished')
    pose_data = data.get('poses')
    image_data = data.get('tensorAsArray')

    # NOTE -> skip error checking for demonstration
    #user = User.objects.filter(id=uid)
    #if not len(user):
    #    return response("user with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    #session = Session.objects.filter(id=sid)
    #if not len(session):
    #    return response("session with this id does not exist", status=status.HTTP_401_UNAUTHORIZED)
    #if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
    #    return response("user was not involved in this session", status=status.HTTP_403_FORBIDDEN)
    
    store = DataStore()
    store.set_poses(pose_data)
    store.set_images(image_data)
    store.write_poses_locally(sid, clip_num)
    store.write_images_locally(sid, clip_num)

    # Write to Azure blob only when the session has been completed
    if session_finished:
        store.write_poses_to_cloud(sid)
        store.write_images_to_cloud(sid)

    return response(status=status.HTTP_200_OK)


@csrf_exempt
def visualise_2D(request):
    '''Present a 2D visualisation of pose data overlayed over the video from 
    which this data was extracted.'''
    # NOTE ->   skip error checking involving users
    #           don't expect user id in request currently

    # use sample data if request is empty (happens when page is first loaded by url)
    sid = "12983129"
    clip_num = "1"
    if request.GET:
        # if request non-empty, use this data
        sid = request.GET.get('sid')
        clip_num = request.GET.get('clipNum')

    store = DataStore()
    if not store.populate_poses(sid, clip_num):
        print("Error: Pose data not found in Azure Blob Storage.")
        return render(request, 'visualise2D.html', {'frames': None})
    if not store.populate_video(sid, clip_num):
        print("Error: Video not found in Azure Blob Storage.")
        return render(request, 'visualise2D.html', {'frames': None})

    cap = cv2.VideoCapture(store.get_video_path(sid, clip_num))
    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return render(request, 'visualise2D.html', {'frames': None})

    frames = json.dumps(create_2D_visualisation(store.get_poses(), cap))
    return render(request, 'visualise2D.html', {'frames': frames}, content_type='text/html')


@csrf_exempt
def visualise_3D(request):
    '''Present a 3D visualisation of pose data.'''
    sid = "e73b5edc-7f2f-43ae-acd6-f2b68b3d0497"
    clip_num = "1"
    if request.GET:
        # if request non-empty, use this data
        sid = request.GET.get('sid')
        clip_num = request.GET.get('clipNum')

    store = DataStore()
    if not store.populate_poses(sid, clip_num):
        print("Error: Pose data not found in Azure Blob Storage.")
        return render(request, '3D_visualise2D.html', {'image': None})
    
    frames = json.dumps(create_3D_visualisation(store.get_poses()))
    return render(request, '3D_visualise2D.html', {'frames': frames})

# WORK IN PROGRESS 3D VISUALISATION
# def visualise_3D(request):
#     '''Present an animation of the frame data for a session.'''
#     uid = "a4db80a8-bac7-4831-8954-d3e402f469bc"
#     sid = "e2b7957a-a1e3-490f-a5a3-b4d00905dd6e"
#     clip_num = 2

#     user = User.objects.filter(id=uid)
#     if not len(user):
#         print("user doesn't exist ... this case is not yet handled!")

#     if not len(InvolvedIn.objects.filter(session=sid, user=uid)):
#         print("user was not involved in this session ... this case is not yet handled!")

#     store = DataStore()
#     if not store.populate_poses(sid, clip_num):
#         print("No session data exists for this session ... this case is not yet handled!")

#     session_frames = store.get_poses()

#     # create a list of numpy arrays for each keypoint
#     frames = []
#     for frame_num, session_frame in enumerate(session_frames):
#         keypoints3D_arrays = []
#         for kp in session_frame.get("keypoints3D"):
#             keypoints3D_arrays.append(np.array([kp.get('x', 0), kp.get('y', 0), kp.get('z', 0)]))

#         xdata = np.array([kp[0] for kp in keypoints3D_arrays])
#         ydata = np.array([kp[1] for kp in keypoints3D_arrays])
#         zdata = np.array([kp[2] for kp in keypoints3D_arrays])

#         trace = go.Scatter3d(
#             x=xdata,
#             y=ydata,
#             z=zdata,
#             mode='markers',
#             marker=dict(size=2, color='red')
#         )

#         lines = [
#             go.Scatter3d(
#                 x=[xdata[joint1], xdata[joint2]],
#                 y=[ydata[joint1], ydata[joint2]],
#                 z=[zdata[joint1], zdata[joint2]],
#                 mode='lines',
#                 line=dict(width=2, color='blue')
#             )
#             for joint1, joint2 in const.KP_CONNS
#         ]

#         frames.append(go.Frame(data=[trace] + lines, name=str(frame_num)))

#     layout = go.Layout(
#         scene=dict(
#             aspectmode="data",
#             aspectratio=dict(x=2, y=2, z=1),
#             xaxis=dict(range=[-2, 2], visible=False),
#             yaxis=dict(range=[-2, 2], visible=False),
#             zaxis=dict(range=[-2, 2]),
#         ),
#         showlegend=False,
#         height=800,
#         margin=dict(l=0, r=0, b=0, t=0),
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         updatemenus=[
#             dict(
#                 type="buttons",
#                 showactive=False,
#                 buttons=[dict(label="Play",
#                             method="animate",
#                             args=[None, {"frame": {"duration": 100, "redraw": True}}])])  # Adjust duration for speed
#         ]
#     )

#     fig = go.Figure(
#         data=[trace] + lines,
#         layout=layout,
#         frames=frames
#     )

#     plot_div = opy.plot(fig, auto_open=False, output_type='div')

#     return render(request, 'visualise_coordinates.html', context={'plot_div': plot_div})
