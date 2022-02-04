from curses.textpad import rectangle
from turtle import left
import matplotlib.pyplot as plt
import random
import numpy as np
random.seed(3)

#For each camera i, define matrix Ci = [pi1, pi2, .... pin] where pij is the jth ray pixel coordinate of camera i
#Define cix, ciy as the origin of camera camera i

#orthogonal camera

class Printed_Matter:
    
    def __init__(self, num_strips = 100, rect_width = 0.1):
        
        self.rect_width = rect_width
        H = random.choices(range(100), k=num_strips)
        self.H = [height/100 for height in H]
        self.COL = random.choices(['r', 'g'], k=num_strips)
        self.rectangle_centers = [1 + val*rect_width + rect_width/2 for val in range(num_strips)]

    
    def plot_matter(self):  
        plt.bar(self.rectangle_centers, self.H, width=self.rect_width, color = self.COL)
        
        
    
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


    def take_photo(self, camera):
        R1 = ['black']*100

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

                    R1[i] = p.COL[j]
                    break
                
        return R1

  
    
class Camera:
    def __init__(self, left_edge, right_edge, num_pixels=10, ray_length = 100):
        self.left_edge = left_edge
        self.right_edge = right_edge
        
        x_coords = [left_edge[0], right_edge[0]]
        y_coords = [left_edge[1], right_edge[1]]
        xs = np.linspace(x_coords[0], x_coords[1], num_pixels)
        ys = np.linspace(y_coords[0], y_coords[1], num_pixels)
        self.pixel_centers = np.array(list(zip(xs,ys)))
        
        camera_face_direction_v  = right_edge - left_edge
        self.orthogonal_direction_v = np.array([camera_face_direction_v[1], -camera_face_direction_v[0]])

        self.ray_ends = np.array([x + self.orthogonal_direction_v*ray_length for x in self.pixel_centers])


    def plot_rays(self):
        
        for i, pixel in enumerate(self.pixel_centers):
            pixel_x = pixel[0]
            xs = [pixel[0], self.ray_ends[i][0]]
            ys = [pixel[1], self.ray_ends[i][1]]
            plt.plot(xs, ys, color = 'b', linewidth = 1, linestyle = "dashed")
      

    def plot_view(self, R1, height = 5):
        plt.bar([i for i in range(len(camera.pixel_centers))], [height for i in range(len(camera.pixel_centers))], width = 1, color = R1)

        
    
       

plt.xlim(0, 12)
plt.ylim(0, 4)
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()
 

left_edge = np.array([1,3])
right_edge = np.array([2,4])


left_edge2 = np.array([0,3])
right_edge2 = np.array([1,4])


num_pixels = 10

camera = Camera(left_edge, right_edge, num_pixels)
camera.plot_rays()


camera2 = Camera(left_edge2, right_edge2, num_pixels)
camera2.plot_rays()

p = Printed_Matter()
p.plot_matter()



R1 = p.take_photo(camera)
R2 = p.take_photo(camera2)

plt.show()

plt.clf()
camera.plot_view(R1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

plt.clf()
camera.plot_view(R2)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

plt.show()






'''
x_coords = [left_edge[0], right_edge[0]]
y_coords = [left_edge[1], right_edge[1]]

xs = np.linspace(x_coords[0], x_coords[1], 10)
ys = np.linspace(y_coords[0], y_coords[1], 10)

camera_face_direction_v  = right_edge - left_edge

print(camera_face_direction_v)

orthogonal_direction = np.array([camera_face_direction_v[1], -camera_face_direction_v[0]])
print(orthogonal_direction)


C1 = np.array(list(zip(xs,ys)))

plt.plot([left_edge[0]], [left_edge[1]], marker='o', markersize=4, color="purple")
plt.plot([right_edge[0]], [right_edge[1]], marker='o', markersize=4, color="purple")

C1 = np.array(list(zip(xs,ys)))



C1_forward_points = np.array([x + orthogonal_direction*100 for x in C1])

for i, pixel in enumerate(C1):
    print(pixel)
    pixel_x = pixel[0]
    print(C1_forward_points[i])
    xs = [pixel[0], C1_forward_points[i][0]]
    ys = [pixel[1], C1_forward_points[i][1]]
    plt.plot(xs, ys, color = 'b', linewidth = 1, linestyle = "dashed")




plt.xlim(0, 12)
plt.ylim(0, 4)
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()


 
 

#Let matrix H = [h1, h2, .... hm] be the heights of rectangles r1, ... rm
#Let matrix COL = [col1, col2, .... colm] be the colors of rectangles r1, ... rm
#Let rectangle width rect_width = 1

m = 100

rect_width = 0.1
H = random.choices(range(100), k=m)
H = [height/100 for height in H]
COL = random.choices(['r', 'g'], k=m)
rectangle_centers = [1 + val/10 for val in range(m)]



plt.bar(rectangle_centers, H, width=rect_width, color = COL)



#https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    #return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def segment_intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def intersect(ray, rectangle, cam_center):
    ray_start = cam_center
    ray_end = ray
    
    ray_dir = ray_end - ray_start
    segment_AB = [ray_start, ray_start + 100*ray_dir]
    
    
    segment_top_side = [rectangle[0], rectangle[1]]
    segment_side = [rectangle[0], rectangle[2]]
    
    
    if segment_intersect(segment_AB[0], segment_AB[1], segment_top_side[0], segment_top_side[1]):
        print(segment_top_side[0])
        print(segment_top_side[1])
        print("Top intersect")
        return 1
        
    if segment_intersect(segment_AB[0], segment_AB[1], segment_side[0], segment_side[1]):
        print(segment_side[0])
        print(segment_side[1])
        print("Side intersect")
        return 1

    
    else:
        return 0

R1 = ['black']*100

for i in range(len(C1)):
    cix = C1[i][0]
    ciy = C1[i][1] #pixel origin
    ray = C1_forward_points[i]
    for j in range(len(H)):
        rect_height = H[j]
        rect_center = rectangle_centers[j]
        rect_top_left = [rect_center-rect_width/2, rect_height]
        rect_top_right = [rect_center+rect_width/2, rect_height]
        rect_bottom_left = [rect_center-rect_width/2, 0]
        rect_bottom_right = [rect_center+rect_width/2, 0]
        
        rectangle = np.array([rect_top_left, rect_top_right, rect_bottom_left, rect_bottom_right])
        if intersect(ray, rectangle, np.array([cix, ciy])):
            print("ray " + str(i) + " intersects rectangle " + str(j))
            print("RECT COLOR " + str(COL[j]))
            print("RECT HEIGHT " + str(H[j]))
            print()
            R1[i] = COL[j]
            break

plt.show()

print("shown plot 1")
plt.clf()

print("cleared")
plt.gca().set_aspect('equal', adjustable='box')


plt.bar([i for i in range(len(C1))], [10 for i in range(len(C1))], width = 1, color = R1)
plt.show()

print("shown")


plt.show()

'''

'''
pixel_centers = np.linspace()
#eg C1 with two rays, one down, one 45 degrees,

edges = np.array([[1, 0], [11, 0]])


cix, ciy = np.array([1, 3])

ray_x_vals = np.array([ray[0] for ray in edges])
ray_y_vals = np.array([ray[1] for ray in edges])

left_edge = edges[0]
right_edge = edges[-1]

left_edge_unit_vector = (left_edge - [cix, ciy])/np.linalg.norm(left_edge - [cix, ciy])
right_edge_unit_vector = (right_edge - [cix, ciy])/np.linalg.norm(right_edge - [cix, ciy])


left_edge_point = left_edge_unit_vector + [cix, ciy]

right_edge_point = right_edge_unit_vector + [cix, ciy]

x_coords = [left_edge_point[0], right_edge_point[0]]
y_coords = [left_edge_point[1], right_edge_point[1]]

xs = np.linspace(x_coords[0], x_coords[1], 100)
ys = np.linspace(y_coords[0], y_coords[1], 100)

C1 = np.array(list(zip(xs,ys)))


plt.plot([left_edge_point[0]], [left_edge_point[1]], marker='o', markersize=4, color="purple")
plt.plot([right_edge_point[0]], [right_edge_point[1]], marker='o', markersize=4, color="purple")



plt.xlim(0, 12)
plt.ylim(0, 4)
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()

for ray in C1:
    ray_x_dir = ray[0] - cix
    ray_y_dir = ray[1] - ciy
    ray_x = cix + 100*ray_x_dir #(times 100 to draw line to infinity)
    ray_y = ciy + 100*ray_y_dir
    xs = [ray_x, cix]
    ys = [ray_y, ciy]
    plt.plot(xs, ys, color = 'b', linewidth = 1, linestyle = "dashed")
 
 

#Let matrix H = [h1, h2, .... hm] be the heights of rectangles r1, ... rm
#Let matrix COL = [col1, col2, .... colm] be the colors of rectangles r1, ... rm
#Let rectangle width rect_width = 1

m = 100

rect_width = 0.1
H = random.choices(range(100), k=m)
H = [height/100 for height in H]
COL = random.choices(['r', 'g'], k=m)
rectangle_centers = [1 + val/10 for val in range(m)]



plt.bar(rectangle_centers, H, width=rect_width, color = COL)
plt.plot([cix], [ciy], marker='o', markersize=10, color="black")


#https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    #return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def segment_intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def intersect(ray, rectangle, cam_center):
    ray_start = cam_center
    ray_end = ray
    
    ray_dir = ray_end - ray_start
    segment_AB = [ray_start, ray_start + 100*ray_dir]
    
    
    segment_top_side = [rectangle[0], rectangle[1]]
    segment_side = [rectangle[0], rectangle[2]]
    
    
    if segment_intersect(segment_AB[0], segment_AB[1], segment_top_side[0], segment_top_side[1]):
        print(segment_top_side[0])
        print(segment_top_side[1])
        print("Top intersect")
        return 1
        
    if segment_intersect(segment_AB[0], segment_AB[1], segment_side[0], segment_side[1]):
        print(segment_side[0])
        print(segment_side[1])
        print("Side intersect")
        return 1

    
    else:
        return 0

R1 = ['black']*100

for i in range(len(C1)):
    ray = C1[i]
    for j in range(len(H)):
        rect_height = H[j]
        rect_center = rectangle_centers[j]
        rect_top_left = [rect_center-rect_width/2, rect_height]
        rect_top_right = [rect_center+rect_width/2, rect_height]
        rect_bottom_left = [rect_center-rect_width/2, 0]
        rect_bottom_right = [rect_center+rect_width/2, 0]
        
        rectangle = np.array([rect_top_left, rect_top_right, rect_bottom_left, rect_bottom_right])
        if intersect(ray, rectangle, np.array([cix, ciy])):
            print("ray " + str(i) + " intersects rectangle " + str(j))
            print("RECT COLOR " + str(COL[j]))
            print("RECT HEIGHT " + str(H[j]))
            print()
            R1[i] = COL[j]
            break

plt.show()

print("shown plot 1")
plt.clf()

print("cleared")
plt.gca().set_aspect('equal', adjustable='box')


plt.bar([i for i in range(len(C1))], [10 for i in range(len(C1))], width = 1, color = R1)
plt.show()

print("shown")

'''