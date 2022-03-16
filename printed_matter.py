
import random
import numpy as np
import utils

color_map = {0: 'g', 1: 'r', -1: 'black'}


class Printed_Matter:
    
    def __init__(self, strips_per_unit = 2, num_units = 20, rect_width = 0.4):
        self.dir = dir
        self.strips_per_unit = strips_per_unit
        self.num_units = num_units
        self.rect_width = rect_width
        H = random.choices(range(100), k=strips_per_unit)
        self.H = np.array([height/100 for height in H])
        self.Repeated_H = self.H * num_units
        #self.COL = random.choices([0, 1], k=strips_per_unit)
        self.COL = np.array(np.random.default_rng().uniform(0,1,strips_per_unit))
        self.rectangle_centers = np.array([1 + val*rect_width + rect_width/2 for val in range(strips_per_unit*num_units)])

    def double_resolution(self):
        #print("Doubling resolution")
        #print(len(self.rectangle_centers))
        self.rect_width = self.rect_width/2
        self.num_units = self.num_units
        self.strips_per_unit = self.strips_per_unit*2
        new_H = []
        for h in self.H:
            new_H.append(h)
            new_H.append(h)
        self.H = new_H
        self.Repeated_H = self.H * self.num_units

        new_COL = []
        for col in self.COL:
            new_COL.append(col)
            new_COL.append(col)
        self.COL = new_COL

        #print("updated centers")
        self.rectangle_centers = [1 + val*self.rect_width + self.rect_width/2 for val in range(self.strips_per_unit*self.num_units)]
        #print(len(self.rectangle_centers))

        
    def plot_matter(self, axs):  
        #colors = [color_map[col] for col in self.COL]
        colors = [utils.get_color(col) for col in self.COL]
        #print(len(self.rectangle_centers))
        #print(len(self.Repeated_H))
        axs[0].bar(self.rectangle_centers, self.Repeated_H, width=self.rect_width, color = colors)
        
    
    #https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    def ccw(self, A,B,C):
        #return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    # Return true if line segments AB and CD intersect
    def segment_intersect(self,A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def intersect(self, ray, rectangle, cam_center, dir = "left"):
        ray_start = cam_center
        ray_end = ray
        ray_dir = ray_end - ray_start
        segment_AB = [ray_start, ray_start + 100*ray_dir]
    
    
        segment_top_side = [rectangle[0], rectangle[1]]
        if dir == "left":
            segment_side = [rectangle[0], rectangle[2]]
        else:
            segment_side = [rectangle[1], rectangle[3]]

    
    
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
        
    def update_repeated_H(self):
        #print("updating H")
        #print(self.H)
        self.Repeated_H = self.H * self.num_units
        #print(self.Repeated_H)
        
    def pertubate_heights(self, step_amount = 0.1, probability_of_change = 0.5):
        p1 = probability_of_change/2
        p2 = 1-probability_of_change
        for i in range(len(self.H)):
            change = random.choices([-step_amount, 0, step_amount], weights=(p1, p2, p1), k=1)[0]
            self.H[i] = self.H[i] + change
            #self.H[i] = self.H[i] + random.choice([-step_amount, 0, step_amount])
        
        self.update_repeated_H()
        
    def update_heights_with_grad(self, gradients, factor = 0.03):
        
        for i in range(len(self.H)):
            self.H[i] = self.H[i] + gradients[i] * factor
        
        self.update_repeated_H()
    
    
    def pertubate_height(self, i, step_amount = 0.1, probability_of_change = 0.5):
        change = random.choice([-step_amount, step_amount])
        self.H[i] = self.H[i] - change
        self.update_repeated_H()
        return change

    def pertubate_colors(self, probability_of_change = 0.5, step_amount = 0.1):
        for i in range(len(self.COL)):
            change = random.uniform(-0.1, 0.1)
            self.COL[i] = max(0,(min(1, self.COL[i] - change)))
        self.update_repeated_H()
        return change
    
    def take_photo(self, camera):
        R = [-1]*camera.num_pixels

        for i in range(len(camera.pixel_centers)):
            
            #print()
            #print("RAY :" + str(i))
            
            cix = camera.pixel_centers[i][0]
            ciy = camera.pixel_centers[i][1] #pixel origin
            ray = camera.ray_ends[i]
            
            for j in range(len(self.Repeated_H)):
                if camera.dir == "left":
                    j_ = j
                else:
                    j_ = len(self.Repeated_H) - j - 1
                
                rect_height = self.Repeated_H[j_]
                rect_center = self.rectangle_centers[j_]
                rect_top_left = [rect_center-self.rect_width/2, rect_height]
                rect_top_right = [rect_center+self.rect_width/2, rect_height]
                rect_bottom_left = [rect_center-self.rect_width/2, 0]
                rect_bottom_right = [rect_center+self.rect_width/2, 0]
                if cix < rect_center:
                    dir = "left"
                else:
                    dir = "right"

        
                
                rectangle = np.array([rect_top_left, rect_top_right, rect_bottom_left, rect_bottom_right])
                if self.intersect(ray, rectangle, np.array([cix, ciy]), dir):
                    #print("Rect Height: "+ str(rect_height))
                    #print(R)
                
                    #print("color length " + str(len(p.COL)))
                    #print(j)
                    #print(p.strips_per_unit)
                    R[i] = self.COL[j_%self.strips_per_unit]
                    break
        camera.set_R(R)
        return R
