import random
from black import re
import numpy as np
import utils
import matplotlib.pyplot as plt
    
import math
strips_per_unit = 5
num_units = 1
rect_width = 0.5

#heights array
H = random.choices(range(10), k=strips_per_unit)
H = [height/100 for height in H]
H = np.array(H)

#colors array
COL = np.random.default_rng().uniform(0,1,strips_per_unit)
COL = np.array(COL)
        
# midpoints of each strip
rectangle_centers = np.array([1 + val*rect_width + rect_width/2 for val in range(strips_per_unit)])


def plot_vector(origin, direction, length = 100):
    end_point = Point(origin.array + direction.array*length)
    x_values = [origin.x, end_point.x]
    y_values = [origin.y, end_point.y]
    print(x_values)
    print(y_values)
    plt.plot(x_values, y_values)


class Point:
    def __init__(self, point_array):
        self.x = point_array[0]
        self.y = point_array[1]
        self.array = point_array
    
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
#ray is origin + t *
def h_to_theta(i, ray, H_i):
    x_0 = 1 #left start of strips
    x = ray.origin.x
    d = ray.direction
    theta = H_i - (d.y/d.x)*((x_0 - x + (i+1)*rect_width))
    return theta

def theta_to_h(i, ray, theta):
    x_0 = 1 #left start of strips
    x = ray.origin.x
    d = ray.direction
    H_i = theta - (d.y/d.x)*((x_0 - x + (i+1)*rect_width))
    return H_i



d = np.array([1,-0.5])
d = d / np.linalg.norm(d)
d = Point(d)
origin = np.array([0,0.5]) # origin point
origin = Point(origin)
#plt.quiver(*origin, d[:,0], d[:,1], color=['black'], scale=2, linewidths = [0.01], edgecolors='k')

#plot_vector(origin, d)
colors = [utils.get_color(col) for col in COL]
plt.bar(rectangle_centers, H, width=rect_width, color = colors)
plt.xlim(-1, 5)
plt.ylim(0, 1.5)

ray = Ray(origin, d)

def plot_thetas(H):
    for i in range(len(H)):
        theta = h_to_theta(i, ray, H[i])
        theta_point = np.array([0, theta])
        theta_point = Point(theta_point)
        plot_vector(theta_point, d)

plot_thetas(H)
plt.show()
        
