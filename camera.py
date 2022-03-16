
import random
import numpy as np
import utils

color_map = {0: 'g', 1: 'r', -1: 'black'}


class Camera:
    def __init__(self, left_edge, right_edge, num_pixels=10, ray_length = 100, camera_num = 1, dir = "left"):
        self.left_edge = left_edge
        self.right_edge = right_edge
        self.num_pixels = num_pixels
        
        self.dir = dir
        
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
        
    def plot_rays(self, axs):
        
        for i, pixel in enumerate(self.pixel_centers):
            pixel_x = pixel[0]
            xs = [pixel[0], self.ray_ends[i][0]]
            ys = [pixel[1], self.ray_ends[i][1]]
            axs[0].plot(xs, ys, color = 'b', linewidth = 0.1)
      
    def set_R(self, R):
        self.R = R
        
    def plot_view(self, axs, height = 10):
        axs[self.camera_num].set_aspect('equal', adjustable='box')
        #colors = [color_map[col] for col in self.R]
        colors = [utils.get_color(col) for col in self.R]
        heights = [height]*self.num_pixels
        axs[self.camera_num].bar([i +0.5 for i in range(len(self.pixel_centers))], heights, width = 1,  color = colors)

        
    def plot_desired_view(self, axs, height = 5):
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
        
        
