# Imports
import base64
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


# Plot 2D Graph
def plot2d(numFrames, frame, joint, leftRoll, leftPitch, leftYaw, rightRoll, rightPitch, rightYaw):
    fig, axs = plt.subplots(2)

    fig.suptitle('2D ' + joint + ' Angle Graph', y=1.005)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.6)
    
    axs[0].plot(range(numFrames), leftRoll, label = 'Roll')
    axs[0].plot(range(numFrames), leftPitch, label = 'Pitch')
    axs[0].plot(range(numFrames), leftYaw, label = 'Yaw')
    axs[0].set_title('Left ' + joint)

    axs[1].plot(range(numFrames), rightRoll, label = 'Roll')
    axs[1].plot(range(numFrames), rightPitch, label = 'Pitch')
    axs[1].plot(range(numFrames), rightYaw, label = 'Yaw')
    axs[1].set_title('Right ' + joint)

    for ax in axs:
        ax.axvline(x=frame, color='r', linestyle='--')

    for ax in axs.flat:
        ax.set(xlabel='Time (Seconds)', ylabel='Angle (Degrees)')
        ax.set(ylim=[0, 180])
        ax.set_yticks(list(np.linspace(start=0, stop=180, num=10)))
        ax.grid()
        ax.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=200)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close()

    return data


# Plot 3D Graph
def plot3d(numFrames, frame, joint, left3d, right3d):
    fig, axs = plt.subplots(2)

    fig.suptitle('3D ' + joint + ' Angle Graph', y=1.005)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.1, wspace=0.4, hspace=0.6)

    axs[0].plot(range(numFrames), left3d)
    axs[0].set_title('Left ' + joint)

    axs[1].plot(range(numFrames), right3d)
    axs[1].set_title('Right ' + joint)

    for ax in axs:
        ax.axvline(x=frame, color='r', linestyle='--')

    for ax in axs.flat:
        ax.set(xlabel='Time (Seconds)', ylabel='Angle (Degrees)')
        ax.set(ylim=[0, 180])
        ax.set_yticks(list(np.linspace(start=0, stop=180, num=10)))
        ax.grid()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight", dpi=200)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    plt.close()

    return data
