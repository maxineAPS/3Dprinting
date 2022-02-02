import matplotlib.pyplot as plt
import random

#For each camera i, define matrix Ci = [pi1, pi2, .... pin] where pij is the jth ray pixel coordinate of camera i
#Define cix, ciy as the origin of camera camera i

#eg C1 with two rays, one down, one 45 degrees,

C1 = [(i, 0) for i in range(1, 12)]
cix, ciy = (0, 4)

ray_x_vals = [ray[0] for ray in C1]
ray_y_vals = [ray[1] for ray in C1]


plt.xlim(0, 12)
plt.ylim(0, 4)
#plt.gca().set_aspect('equal', adjustable='box')
plt.draw()

for ray in C1:
    ray_x_dir = ray[0] - cix
    ray_y_dir = ray[1] - ciy
    ray_x = cix + 100*ray_x_dir #(times 100 to draw line to infinity)
    ray_y = ciy + 100*ray_y_dir
    xs = [ray_x, cix]
    ys = [ray_y, ciy]
    plt.plot(xs, ys, color = 'b')
 
#Let matrix H = [h1, h2, .... hm] be the heights of rectangles r1, ... rm
#Let matrix COL = [col1, col2, .... colm] be the colors of rectangles r1, ... rm
#Let rectangle width rect_width = 1

random.seed = 1

rect_width = 0.1

H = random.choices(range(100), k=100)
H = [height/100 for height in H]
COL = random.choices(['r', 'g'], k=100)
rectangle_centers = [val + 0.5 for val in range(100)]
rectangle_centers = [1 + center/10 for center in rectangle_centers]



plt.bar(rectangle_centers, H, width=rect_width, color = COL)
plt.plot([cix], [ciy], marker='o', markersize=3, color="red")

plt.show()