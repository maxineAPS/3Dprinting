import matplotlib as mpl
import numpy as np

def get_color(val, c1 = 'green', c2 = 'red'):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((val)*c1 + (1-val)*c2)


def set_plot_bounds(axs):

    axs[0].axis(xmin=0, xmax=12, ymin=0, ymax=4)
    axs[0].set_aspect('equal', adjustable='box')

def update(cameras, axs, p):
    for camera in cameras:
        R = p.take_photo(camera)
        camera.plot_view(axs)
        camera.plot_desired_view(axs)
        


  