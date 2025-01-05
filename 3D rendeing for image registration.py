# Case study 3: Manula Registration prototype

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import numpy as np

#Global variables for the cuboid's position and orientation
cuboid_x, cuboid_y, cuboid_z = 0.0, 0.0, -5.0
cuboid_roll, cuboid_pitch, cuboid_yaw = 0.0, 0.0, 0.0  

def setup_window(width, height):
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluPerspective(45, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

def load_video_frame(video_capture):
    ret, frame = video_capture.read()
    if not ret:
        return None
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def draw_cuboid_with_border():
    global cuboid_x, cuboid_y, cuboid_z, cuboid_roll, cuboid_pitch, cuboid_yaw

    cuboid_width = 2.0
    cuboid_height = 1.0
    cuboid_depth = 3.0

    glPushMatrix()
    glTranslatef(cuboid_x, cuboid_y, cuboid_z)
    glRotatef(cuboid_pitch, 1, 0, 0)  
    glRotatef(cuboid_yaw, 0, 1, 0)    
    glRotatef(cuboid_roll, 0, 0, 1)   
    glColor4f(1.0, 1.0, 1.0, 0.5)  
    glLineWidth(5)  
    glBegin(GL_LINES)
    
    #Front face edges
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)

    #Back face edges
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)

    #Connecting between front and back faces
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, -cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)
    
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, cuboid_depth / 2)
    glVertex3f(-cuboid_width / 2, cuboid_height / 2, -cuboid_depth / 2)

    glEnd()

    glPopMatrix()

def render_video_with_cuboid(video_capture, width, height, texture_id):
    frame = load_video_frame(video_capture)
    if frame is None:
        return False

    frame = cv2.flip(frame, 0)
    frame_data = np.frombuffer(frame.tobytes(), dtype=np.uint8)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, frame_data)

    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-4.0, -3.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -3.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(4.0, 3.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 3.0, -1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    draw_cuboid_with_border()

    return True

def handle_user_input():
    global cuboid_x, cuboid_y, cuboid_z, cuboid_roll, cuboid_pitch, cuboid_yaw

    keys = pygame.key.get_pressed()
    
    if keys[K_LEFT]: #X-axis (left)
        cuboid_x -= 0.1
    if keys[K_RIGHT]:  #X-axis (right)
        cuboid_x += 0.1
    if keys[K_UP]:   #Y-axis  (up)
        cuboid_y += 0.1
    if keys[K_DOWN]:   #Y-axis (down)
        cuboid_y -= 0.1

    if keys[K_w]:  #Z-axis (forward)
        cuboid_z += 0.1
    if keys[K_s]:  #Z-axis (backward)
        cuboid_z -= 0.1

    #Rotation (Roll, Pitch, Yaw)
    if keys[K_q]:  #Roll (counter-clockwise around Z-axis)
        cuboid_roll += 1
    if keys[K_e]:  #Roll (clockwise around Z-axis)
        cuboid_roll -= 1

    if keys[K_r]:  #Pitch (upward around X-axis)
        cuboid_pitch += 1
    if keys[K_f]:  #Pitch (downward around X-axis)
        cuboid_pitch -= 1

    if keys[K_a]:  #Yaw (left around Y-axis)
        cuboid_yaw += 1
    if keys[K_d]:  #Yaw (right around Y-axis)
        cuboid_yaw -= 1

def main():
    video_path = "/home/dfki.uni-bremen.de/nvasantakumaar/surgar/stream.mp4" #please change the path for the video file stream.mp4
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    width, height = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    setup_window(width, height)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                video_capture.release()
                pygame.quit()
                return

        handle_user_input()

        if not render_video_with_cuboid(video_capture, width, height, texture_id):
            print("Error: Could not load video frame.")
            break

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
