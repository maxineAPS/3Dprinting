from curses.textpad import rectangle
from turtle import left
from xxlimited import new
import matplotlib.pyplot as plt
import random
import numpy as np
#random.seed(1)
import time
import copy

#For each camera i, define matrix Ci = [pi1, pi2, .... pin] where pij is the jth ray pixel coordinate of camera i
#Define cix, ciy as the origin of camera camera i

#orthogonal camera
plt.ion()

color_map = {0: 'g', 1: 'r'}


fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [2, 1]})



class Printed_Matter:
    
    def __init__(self, num_strips = 100, rect_width = 0.1):
        
        self.rect_width = rect_width
        H = random.choices(range(100), k=num_strips)
        self.H = [height/100 for height in H]
        self.COL = random.choices([0, 1], k=num_strips)
        self.rectangle_centers = [1 + val*rect_width + rect_width/2 for val in range(num_strips)]

    
    def plot_matter(self):  
        colors = [color_map[col] for col in self.COL]
        axs[0].bar(self.rectangle_centers, self.H, width=self.rect_width, color = colors)
        
    
    #https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    def ccw(self, A,B,C):
        #return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def segment_intersect(self,A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)




    def intersect(self, ray, rectangle, cam_center):
        ray_start = cam_center
        ray_end = ray
    
        ray_dir = ray_end - ray_start
        segment_AB = [ray_start, ray_start + 100*ray_dir]
    
    
        segment_top_side = [rectangle[0], rectangle[1]]
        segment_side = [rectangle[0], rectangle[2]]
    
    
        if self.segment_intersect(segment_AB[0], segment_AB[1], segment_top_side[0], segment_top_side[1]):
            #print(segment_top_side[0])
            #print(segment_top_side[1])
            #print("Top intersect")
            return 1
        
        if self.segment_intersect(segment_AB[0], segment_AB[1], segment_side[0], segment_side[1]):
            #print(segment_side[0])
            #print(segment_side[1])
            #print("Side intersect")
            return 1

        else:
            return 0

    def pertubate_heights(self, step_amount = 0.1, probability_of_change = 0.5):
        p1 = probability_of_change/2
        p2 = 1-probability_of_change
        for i in range(len(self.H)):
            change = random.choices([-step_amount, 0, step_amount], weights=(p1, p2, p1), k=1)[0]
            self.H[i] = self.H[i] + change
            #self.H[i] = self.H[i] + random.choice([-step_amount, 0, step_amount])
        
    def pertubate_colors(self, probability_of_change = 0.5):

        for i in range(len(self.COL)):
            change = random.choices([0, 1], weights=(1-probability_of_change, probability_of_change), k=1)[0]
            if change:
                self.COL[i] = 1-self.COL[i]
            #self.H[i] = self.H[i] + random.choice([-step_amount, 0, step_amount])
            
    def take_photo(self, camera):
        R = ['black']*camera.num_pixels

        for i in range(len(camera.pixel_centers)):
            cix = camera.pixel_centers[i][0]
            ciy = camera.pixel_centers[i][1] #pixel origin
            ray = camera.ray_ends[i]
            for j in range(len(p.H)):
                rect_height = p.H[j]
                rect_center = p.rectangle_centers[j]
                rect_top_left = [rect_center-p.rect_width/2, rect_height]
                rect_top_right = [rect_center+p.rect_width/2, rect_height]
                rect_bottom_left = [rect_center-p.rect_width/2, 0]
                rect_bottom_right = [rect_center+p.rect_width/2, 0]
        
                rectangle = np.array([rect_top_left, rect_top_right, rect_bottom_left, rect_bottom_right])
                if self.intersect(ray, rectangle, np.array([cix, ciy])):

                    R[i] = p.COL[j]
                    break
        camera.set_R(R)
        return R

  
    
class Camera:
    def __init__(self, left_edge, right_edge, num_pixels=10, ray_length = 100, camera_num = 1):
        self.left_edge = left_edge
        self.right_edge = right_edge
        self.num_pixels = num_pixels
        
        x_coords = [left_edge[0], right_edge[0]]
        y_coords = [left_edge[1], right_edge[1]]
        xs = np.linspace(x_coords[0], x_coords[1], num_pixels)
        ys = np.linspace(y_coords[0], y_coords[1], num_pixels)
        self.pixel_centers = np.array(list(zip(xs,ys)))
        
        camera_face_direction_v  = right_edge - left_edge
        self.orthogonal_direction_v = np.array([camera_face_direction_v[1], -camera_face_direction_v[0]])

        self.ray_ends = np.array([x + self.orthogonal_direction_v*ray_length for x in self.pixel_centers])

        #desired colors, default all green
        self.D = np.zeros(num_pixels)
        self.camera_num = camera_num
        
    def plot_rays(self):
        
        for i, pixel in enumerate(self.pixel_centers):
            pixel_x = pixel[0]
            xs = [pixel[0], self.ray_ends[i][0]]
            ys = [pixel[1], self.ray_ends[i][1]]
            axs[0].plot(xs, ys, color = 'b', linewidth = 0.1)
      
    def set_R(self, R):
        self.R = R
        
    def plot_view(self, height = 10):
        axs[self.camera_num].set_aspect('equal', adjustable='box')
        colors = [color_map[col] for col in self.R]
        heights = [height]*self.num_pixels
        axs[self.camera_num].bar([i +0.5 for i in range(len(self.pixel_centers))], heights, width = 1,  color = colors)

        
    def plot_desired_view(self, height = 5):
        axs[self.camera_num].set_aspect('equal', adjustable='box')
        
        colors = [color_map[col] for col in self.D]
        heights = [height]*self.num_pixels
        axs[self.camera_num].bar([i +0.5 for i in range(len(self.pixel_centers))], heights, width = 1,  color = colors)
        axs[self.camera_num].hlines(5, xmin=0, xmax = self.num_pixels, color = 'black')
        
        
    def set_desired(self, D):
        self.D = D

    def set_random_desired(self):
        random_choices = np.array(random.choices([0, 1], k = self.num_pixels))
        self.set_desired(random_choices)
        
    def get_cam_loss(self):
        mse = ((self.D - self.R)**2).mean(axis=0)
        return mse
        
        
def set_plot_bounds():

    axs[0].axis(xmin=0, xmax=12, ymin=0, ymax=4)
    axs[0].set_aspect('equal', adjustable='box')


def update(cameras, p):


    for camera in cameras:
        R = p.take_photo(camera)
        camera.plot_view()
        camera.plot_desired_view()



         
left_edge = np.array([1,3])
right_edge = np.array([2,4])


left_edge2 = np.array([0,3])
right_edge2 = np.array([1,4])



num_pixels = 100
camera = Camera(left_edge, right_edge, num_pixels, camera_num=1)

p = Printed_Matter()
#camera.set_random_desired()
desired_manual = [0]*30 + [1] *20 + [0]* 40 + [1]*10
camera.set_desired(np.array(desired_manual))

set_plot_bounds()
cameras = [camera]
update(cameras, p)
p.plot_matter()


old_heights = copy.deepcopy(p.H)
old_cols = copy.deepcopy(p.COL)

old_loss = camera.get_cam_loss()
step_size_e = 0.1
step_size_r = 0.8


prob_e = 0.5
prob_r = 0.8

color_e = 0.4
color_r = 0.8

update_ratio = 3 #num normal updates per color update

for i in range(100):
    camera.plot_rays()

    if i%update_ratio == 0:
        p.pertubate_colors(probability_of_change=prob_e)

    else:
        p.pertubate_heights(step_amount=step_size_e, probability_of_change=prob_e)
    cameras = [camera]
    update(cameras, p)
    
    
    new_loss = camera.get_cam_loss()
    
    #print()
    #print("old loss " + str(old_loss) + "new_loss" + str(new_loss))

    print("LOSS: " + str(old_loss))


    if new_loss <= old_loss:
        
        old_loss = new_loss
        
        if i%update_ratio == 0:
            old_cols = copy.deepcopy(p.COL)
            color_e = color_e*color_r
        else:
            old_heights = copy.deepcopy(p.H)
        
            prob_e = prob_e * prob_r
            step_size_e = step_size_e * step_size_r
        
    
    else:
        if i%update_ratio == 0:
            p.COL = copy.deepcopy(old_cols)
        else:
            p.H = copy.deepcopy(old_heights)
        

        p.plot_matter()
        update(cameras, p)

        
    
    #print(p.H)

    p.plot_matter()
    set_plot_bounds()
    plt.draw()
    plt.pause(0.00001)
    axs[0].cla()


















'''
camera2 = Camera(left_edge2, right_edge2, num_pixels, camera_num=2)
camera2.plot_rays()
R2 = p.take_photo(camera2)
camera2.plot_view()
camera2.plot_desired_view()
'''







