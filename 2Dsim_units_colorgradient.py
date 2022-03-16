from curses.textpad import rectangle
from turtle import left
from xxlimited import new
import matplotlib.pyplot as plt
import random
import numpy as np
#random.seed(1)
import time
import copy
import matplotlib as mpl
from camera_system import Camera_System
from  printed_matter import Printed_Matter
from camera import Camera
import utils

#For each camera i, define matrix Ci = [pi1, pi2, .... pin] where pij is the jth ray pixel coordinate of camera i
#Define cix, ciy as the origin of camera camera i


        
opts = {"subdivide": True, "num_pixels": 50}
#orthogonal camera
plt.ion()

color_map = {0: 'g', 1: 'r', -1: 'black'}
fig, axs = plt.subplots(3, gridspec_kw={'height_ratios': [2, 1, 1]})


###################################################
#                  CAMERA SETUP  
###################################################

num_pixels = opts["num_pixels"]
#Camera 0
left_edge0 = np.array([1,3])
right_edge0 = np.array([2,4])
camera0 = Camera(left_edge0, right_edge0, num_pixels, camera_num=1)
desired_all_red = [1] * num_pixels
camera0.set_random_desired()
camera0.set_desired(np.array(desired_all_red))

#Camera 1
left_edge1 = np.array([10,4])
right_edge1 = np.array([11, 3])
camera1 = Camera(left_edge1, right_edge1, num_pixels, camera_num=2, dir = "right")
desired_all_green = [0] * num_pixels
camera1.set_desired(np.array(desired_all_green))

#Camera 2
left_edge2 = np.array([0,3])
right_edge2 = np.array([1,4])


p = Printed_Matter()
#camera.set_random_desired()
desired_manual = [0]*30 + [1] *20 + [0]* 40 + [1]*10


utils.set_plot_bounds(axs)
cameras = [camera0, camera1]
utils.update(cameras, axs, p)
p.plot_matter(axs)


old_heights = copy.deepcopy(p.Repeated_H)
old_cols = copy.deepcopy(p.COL)

old_loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
step_size_e = 0.1
step_size_r = 0.8

prob_e = 0.5
prob_r = 0.8

color_e = 0.4
color_r = 0.8

update_ratio = 4 #num normal updates per color update


def get_gradient():
    
    old_heights = copy.deepcopy(p.Repeated_H)
    old_H = copy.deepcopy(p.H)
    old_color = copy.deepcopy(p.COL)
    
    gradient = [0]*(len(p.H) + len(p.COL))
    utils.update(cameras, axs, p)
    original_loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
    
    for i in range(len(p.H)):
        change_height = p.pertubate_height(i)
        utils.update(cameras, axs, p)
        loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
        gradient[i] = loss-original_loss/change_height         #loss wrt change in height i
        p.H = copy.deepcopy(old_H)
        p.Repeated_H = copy.deepcopy(p.Repeated_H)
        #print(gradient)

    for j in range(len(p.COL)):
        change_col = p.pertubate_colors(i)
        utils.update(cameras, axs, p)
        loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
        gradient[i] = loss-original_loss/change_height         #loss wrt change in height i
        p.H = copy.deepcopy(old_H)
        p.Repeated_H = copy.deepcopy(p.Repeated_H)
        #print(gradient)
        
    return gradient

#get_gradient()
     

'''
num_steps = 0
for i in range(100):
    num_steps += 1
    print("STEP" + str(num_steps))

    camera0.plot_rays(axs)
    camera1.plot_rays(axs)

    if i%update_ratio == 0:
        p.pertubate_colors(probability_of_change=prob_e)

    else:
        gradients = get_gradient()
        p.update_heights_with_grad(gradients)


    utils.update(cameras, axs, p)
    
    new_loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
    
    #print()
    #print("old loss " + str(old_loss) + "new_loss" + str(new_loss))

    print("LOSS: " + str(old_loss))
    if new_loss < old_loss:
        
        old_loss = new_loss
        
        if i%update_ratio == 0:
            old_cols = copy.deepcopy(p.COL)
            color_e = color_e*color_r
        else:
            old_heights = copy.deepcopy(p.Repeated_H)
        
            prob_e = prob_e * prob_r
            step_size_e = step_size_e * step_size_r
        
        
    else:
        if i%update_ratio == 0:
            print(len(p.COL))
            p.COL = copy.deepcopy(old_cols)
            print("JUST set p.COL to array of")
            print(len(p.COL))

        else:
            p.Repeated_H = copy.deepcopy(old_heights)
        p.plot_matter(axs)
        utils.update(cameras, axs, p)

        
    
    #print(p.H)

    p.plot_matter(axs)
    utils.set_plot_bounds(axs)
    plt.draw()
    plt.pause(0.00001)
    axs[0].cla()
    
   

    






   
'''


def get_gradients(p):
    color_derviatives = [0] * len(p.COL)
    height_derivatives = [0] * len(p.Repeated_H)
    return color_derviatives, height_derivatives

def update_params(p, learning_rate):
    col_derivs, height_derivs = get_gradients(p)
    p.COL -= col_derivs #* learning_rate
    p.Repeated_H -= height_derivs #* learning_rate

r = 1
cameras = [camera0, camera1]

for i in range(100):
    camera0.plot_rays(axs)
    camera1.plot_rays(axs)
    if i%update_ratio == 0:
        p.pertubate_colors(probability_of_change=prob_e)
    elif i%update_ratio == 1:
        p.pertubate_heights(step_amount=step_size_e, probability_of_change=prob_e)
    else:
        update_params(p, 0.1)
        
    utils.update(cameras, axs, p)  
    new_loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
    
    print("LOSS: " + str(old_loss))
    
    if new_loss <= old_loss:
        old_loss = new_loss
        
        if i%update_ratio == 0:
            old_cols = copy.deepcopy(p.COL)
            color_e = color_e*color_r
        elif i%update_ratio == 1:
            old_heights = copy.deepcopy(p.Repeated_H)
        
            prob_e = prob_e * prob_r
            step_size_e = step_size_e * step_size_r

        else:
            old_cols = copy.deepcopy(p.COL)
            color_e = color_e*color_r
            old_heights = copy.deepcopy(p.Repeated_H)
            prob_e = prob_e * prob_r
            step_size_e = step_size_e * step_size_r
            
            
    else:
        if i%update_ratio == 0:
            p.COL = copy.deepcopy(old_cols)
        elif i%update_ratio == 1:
            p.Repeated_H = copy.deepcopy(old_heights)
            
        else:
            p.COL = copy.deepcopy(old_cols)
            p.Repeated_H = copy.deepcopy(old_heights)
            
        p.plot_matter(axs)
        utils.update(cameras, axs, p)

        
    
    #print(p.H)

    p.plot_matter(axs)
    utils.set_plot_bounds(axs)
    plt.draw()
    plt.pause(0.00001)
    axs[0].cla()
    
    if i%int(6*r) == 0:
        p.double_resolution()
        old_cols = copy.deepcopy(p.COL)
        old_heights = copy.deepcopy(p.Repeated_H)
        r *= 1.5




'''

for i in range(100):
    camera0.plot_rays(axs)
    camera1.plot_rays(axs)
    if i%update_ratio == 0:
        p.pertubate_colors(probability_of_change=prob_e)
    else:
        p.pertubate_heights(step_amount=step_size_e, probability_of_change=prob_e)

    utils.update(cameras, axs, p)  
    new_loss = (camera0.get_cam_loss() + camera1.get_cam_loss())/2
    
    print("LOSS: " + str(old_loss))
    
    if new_loss <= old_loss:
        old_loss = new_loss
        
        if i%update_ratio == 0:
            old_cols = copy.deepcopy(p.COL)
            color_e = color_e*color_r
        else:
            old_heights = copy.deepcopy(p.Repeated_H)
        
            prob_e = prob_e * prob_r
            step_size_e = step_size_e * step_size_r
    
    else:
        if i%update_ratio == 0:
            p.COL = copy.deepcopy(old_cols)
        else:
            p.Repeated_H = copy.deepcopy(old_heights)
        p.plot_matter(axs)
        utils.update(cameras, axs, p)

        
    
    #print(p.H)

    p.plot_matter(axs)
    utils.set_plot_bounds(axs)
    plt.draw()
    plt.pause(0.00001)
    axs[0].cla()
    
    if i%int(6*r) == 0:
        p.double_resolution()
        old_cols = copy.deepcopy(p.COL)
        old_heights = copy.deepcopy(p.Repeated_H)
        r *= 1.5

'''











