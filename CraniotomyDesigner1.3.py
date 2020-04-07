import pygame 
from RESOURCES.GUI_elements_by_flav import *
import subprocess
import math
import numpy as np
from numpy import linalg
import os

##import tkinter as Tk #Note: "Tkinter" in python 2 (capital T)
##from tkinter.filedialog import askopenfilename, asksaveasfile

from tkinter import filedialog
from tkinter import *
import CranioHelperFunctions 

red         = (255,0,0)
green       = (0,255,0)
blue        = (0,0,255)
gray        = (150,150,150)
darkgray    = (50,50,50)
lightgray   = (200,200,200)
black       = (0,0,0)
white       = (255,255,255)
yellow      = (255,255,0)
pink        = (255, 192, 203)
pink1= (255, 181, 197, 255),
pink2= (238, 169, 184, 255),
pink3= (205, 145, 158, 255),
pink4= (139, 99, 108, 255),


lightpurple  = (160,12,75)
darkpurple  = (51,5,25)


def collide_point(pt,  cur_x,cur_y,  radius):
    if pt[0] - radius  <=cur_x <= pt[0] + 4* radius:
        if pt[1] - radius  <=cur_y<= pt[1] + 4 * radius:
                print("COLLIDED")
                return True
        else:
            return False

def collide_line(line,cur_x,cur_y,  radius):
    pass
    
def distance_between_2_pts(p1,p2):
    dist = math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))
    return dist

def dist_from_pt_to_line(p0,line): #(p1 = point,  line  = (p1,p2)
        ''' to go from 2 points to a standard form line:
                    (y1 – y2)x + (x2 – x1)y + (x1y2 – x2y1) = 0   ### from https://bobobobo.wordpress.com/2008/01/07/solving-linear-equations-ax-by-c-0/
                    a = y1-y2
                    b = x2-x1
                    c = x1y2 - x2y1
            line: ax + by + c = 0
            distance = abs(ax + by + c) / sqrt(a*a + b*b)        ###from https://brilliant.org/wiki/dot-product-distance-between-point-and-a-line/
        '''
        x = p0[0]
        y = p0[1]

        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]
        a= (y1-y2)
        b= (x2-x1)
        c = (x1*y2 - x2*y1)

        if (a*a + b*b) > 0:
                dist = abs(a * x  + b * y + c) / math.sqrt(a*a + b*b)# in pixels, not mm!
                print ("dist: ", dist)
        else:
            print("What?  math.sqrt(a*a + b*b) = 0")
        return dist

def draw_circular_craniotomy(bregma, ctrx,ctry, r,num_points=16):
     points = []

     deg_per_point = 360.0/num_points
     for a in np.arange(0,361,.5):
         x = int(bregma[0] - ctrx + r * np.cos(a*np.pi/180.0))
         y = int(bregma[1] - ctry + r * np.sin(a*np.pi/180.0))
      
         if a%22.5 == 0.0:# 16 point circle = 360/22.5
                 points.append((x,y))
     print ("num points: ",len(points))
     print(points)
     return points

#################################
#  MAIN PROGRAM
     
def DrawCraniotomy():

     
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,30) # Place window on computer screen
    UMNlogo = pygame.image.load(r'.\RESOURCES\UMNlogo.PNG')
    pygame.display.set_icon(UMNlogo)
    TNElogo = pygame.image.load(r'.\RESOURCES\TNE logo.jpg')
    TNElogo = pygame.transform.scale(TNElogo, (70, 55))
    mice_skull_graphic = pygame.image.load(r'.\RESOURCES\mouseLARGE.png')
    rats_skull_graphic= pygame.image.load(r'.\RESOURCES\skullGraphicRealLARGE.png')

    # Using Paint, we see that the image is 446 pix wide by 600 pixels tall
    # On my screen, i measure 99.03 mm x 134.29 mm
    pix_per_mm = 4.5




    pygame.display.set_caption('CraniotomyDesigner1.2 by F. da Silva March 23, 2020') # Enter your window caption here

  
    ########################
    # Prepare Screen
    #########################
    myscreen = pygame.display.set_mode((700,800),pygame.RESIZABLE,32)
    myscreen.fill(pink1)
    # LABELS
    labels = []
    labels.append(MyLabel(myscreen,20,10,   "LEFT Mouse button to ADD new points'",16))
    labels.append(MyLabel(myscreen,20,30,   "LEFT Mouse button on existing line iserts new point",16))
    labels.append(MyLabel(myscreen,20,50,   "SHFT + LEFT Mouse button to MOVE points'",16))
    labels.append(MyLabel(myscreen,20,70,   "RIGHT Mouse Key to DELETE points'",16))

    labels.append(MyLabel(myscreen,20,170,   "Drilling",16))
    labels.append(MyLabel(myscreen,20,190,   "Cutting",16))
    labels.append(MyLabel(myscreen,20,210,   "Relocating",16))

    labels.append(MyLabel(myscreen,500,30,   "Rats",16))
    labels.append(MyLabel(myscreen,500,50,   "Mice",16))
    
    # RADIO BUTTONS
    radio_buttons = []
    #(self,screen,index, x,y,radius, ONOFF, on_color)
    radio_buttons.append(radio_button(myscreen,0,   540,30, 7, "ON", (255,200,200))) # RATS
    radio_buttons.append(radio_button(myscreen,1,   540,50, 7, "OFF", (255,200,200))) # Mice

    
    # BUTTONS
    buttons = []
    #                                                        idx,  x,   y,    wd,  ht,  Label,                      font size

    buttons.append(MyButton(myscreen,0,   20,100, 120,30,"Load Existing",16))
    buttons.append(MyButton(myscreen,1, 150,100, 120,30,"Circle Craniotomy",16))
    buttons.append(MyButton(myscreen,2, 280,100, 120,30,"Create Craniotomy",16))
    buttons.append(MyButton(myscreen,3, 410,100, 120,30,"Add Screw Holes",16))
    buttons.append(MyButton(myscreen,4, 540,100, 55,30,"Save",16))
    buttons.append(MyButton(myscreen,5, 605,100, 55,30,"Clr All",16))

    # VARIABLES
    screw_holes = []
    cranio_points = []
    craniotomies = []

    lines=[]
    #########################
    #  Create GUI elements
    #########################


    drill_radius = 5 #pixels   
    # FLAGS
    LEFT_MOUSE_DOWN = False
    MID_MOUSE_DOWN = False
    RIGHT_MOUSE_DOWN = False
    PATH_COMPLETE = False
    MOVE_POINT  =False
    MOVE_EXISTING_CRANIO_PT =False
    MOVE_SCREW_HOLE =False
    DRILLING_SCREW_HOLES = False
    DRILLING_CRANIOTOMY = False
    DRAWING_NEW_CRANIO_PATH = False
    EXISTING_CRANIOTOMY = False
    SHIFT_KEY_PRESSED = False
    LINE_CLICKED = False
    RATS = True
    MICE = False
    #############################
    #  MAIN LOOP
    #############################
    while True:
        # FOR RATS
        # 50 mm = 9 scrn_mm on
        # therfore 1 mm on rat = 5.555 mm on screen (=50/9).   5.555 mm / scrn_mm
 
        if RATS: scale = pix_per_mm * 5.5555555555   # = 25 pixels

        # FOR MICE
        # 50 mm = 4.2 scrn_mm on  = 11.90476 mm/scrn_mm
        # therfore 1 mm on rat = 11.90476 mm on screen (=50/9).   11.90476 mm / scrn_mm

        if MICE: scale = pix_per_mm * 11.90476   # = 25 pixels
    

##    pix_per_scrn_mm = pix_per_mm / 5.555555555555 # in scrn mm
        ############################################################################
        #  HANDLE SYSTEM EVENTS
        ############################################################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            ############################################################################
            #  HANDLE KEY PRESSES
            ############################################################################
            elif (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_SPACE:
                        print("Space Bar pressed")
                        
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT or \
                       event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                        print("Shift  or Ctrl key pressed")
                        SHIFT_KEY_PRESSED = True
                               
                    # ARROW KEYS 
                    elif event.key == pygame.K_DOWN:
                         print("down arrow")
                   
                    elif event.key == pygame.K_UP:
                         print("up arrow")
                         
            elif (event.type == pygame.KEYUP):
                     SHIFT_KEY_PRESSED = False
                     MOVE_POINT = False
                     MOVE_POINT  =False
                     MOVE_EXISTING_CRANIO_PT =False
                     MOVE_SCREW_HOLE =False                            
                     print("key UP")
            ############################################################################
            #  HANDLE MOUSE MOVES
            ############################################################################

            elif (event.type == pygame.MOUSEMOTION):#
                cur_x,cur_y = pygame.mouse.get_pos()

                
                #if MOVE_POINT and DRILLING_CRANIOTOMY:
                if MOVE_EXISTING_CRANIO_PT:
                            print("Moving (",cur_x,", ",cur_y,") in Cranio: ", cur_cranio_idx, " Point", cur_point_in_cranio_idx)
                            craniotomies[cur_cranio_idx][cur_point_in_cranio_idx]= (cur_x,cur_y)
                            
                elif MOVE_POINT:
                        if len(cranio_points) > 0:
                            print("Moving (",cur_x,", ",cur_y,")")
                            cranio_points[cur_point_idx]= (cur_x,cur_y)
                    
                if MOVE_SCREW_HOLE:
                    print("Moving (",cur_x,", ",cur_y,")")
                    screw_holes[cur_hole_idx]= (cur_x,cur_y)

            ############################################################################
            #  HANDLE MOUSE CLICKS
            ############################################################################                       
            # MOUSE DOWN
            '''
            1 - left clickcur

            2 - middle click

            3 - right click

            4 - scroll up

            5 - scroll down
            '''
            if (event.type == pygame.MOUSEBUTTONDOWN ):#Mouse Clicked
                print("MOUSE CLICKED: ", event.button)
                # LEFT MOUSE BUTTON: ADD cranio_points
                if event.button == 1  and not SHIFT_KEY_PRESSED:
                        LEFT_MOUSE_DOWN = True
                        RIGHT_MOUSE_DOWN = False
                        MID_MOUSE_DOWN = False

                        # RADIO BUTTONS
                        rad_button_idx = 0
                        rad_button_on = 0
                        for rad_button in radio_buttons: # Check for collision with EXISTING buttons
                                if rad_button.rect.collidepoint(cur_x,cur_y):
                                        rad_button.ONOFF = "ON"
                                        if  rad_button.index == 0:
                                            MICE = False
                                            RATS = True
                                            radio_buttons[1].ONOFF = "OFF"
                                        if  rad_button.index == 1: 
                                            MICE = True
                                            RATS = False
                                            radio_buttons[0].ONOFF = "OFF"
                                            
                                    
                        # BUTTONS
                        for button in buttons: # Check for collision with EXISTING buttons
                                if button.rect.collidepoint(cur_x,cur_y):
                                    button.UP_DN = "DN"
                                    button.face_color = (138, 169, 184)
                                    if "Screw" in button.text:
                                         DRILLING_SCREW_HOLES = True
                                         DRILLING_CRANIOTOMY = False
                                         DRAWING_NEW_CRANIO_PATH = False
                                         
                                    if "Circle" in button.text:
                                         print("\n\nUSER INPUTS!")
                                         radius = scale * float(input("Enter Radius (mm)"))
                                         x_offset = scale * float(input("Enter lateral offset from Bregma (+left, -right in mm)"))
                                         y_offset = scale * float(input("Enter offset from Bregma along anterior-posteror axis (+Ant, -Pos in mm)"))
                                         #number_of_points = int(input("Number of points"))
                                         print("r= ",radius,"x= ",x_offset, "y+ ",y_offset)
                                         craniotomies.append(draw_circular_craniotomy(bregma, x_offset, y_offset, radius))

                                    if "Square" in button.text:
                                         pass
                                        
                                    if "Craniotomy" in button.text:
                                         PATH_COMPLETE = False
                                         DRILLING_CRANIOTOMY = True
                                         NEW_CRANIOTOMY = True
                                         DRILLING_SCREW_HOLES = False
                                         DRAWING_NEW_CRANIO_PATH = True
                                         cranio_points = []


                                    if "Load" in button.text:
                                         LOADING_SCREW_HOLES = False
                                         LOADING_CRANIOS = False
                                         cwd = os.getcwd()
                                         print(cwd)

                                         RODENT, screw_holes, screw_holes_scrn, craniotomies,craniotomies_rat = CranioHelperFunctions.load_design(cwd,scale,bregma)
                                         print ("RODENT: ",RODENT)
                                         if 'RAT' in RODENT:
                                             RATS  = True
                                             MICE = False
                                         elif 'MICE' in RODENT:
                                             RATS = False
                                             MICE  = True
                                         

                                                 
                                    if "Clr" in button.text:
                                            screw_holes = []
                                            cranio_points = []
                                            craniotomies = []
                                        
                                    if "Save" in button.text:
                                         DRILLING_CRANIOTOMY = False
                                         DRILLING_SCREW_HOLES = False

                                         cwd = os.getcwd()
                                         print(cwd)
                                         if RATS: RODENT = "RATS"
                                         elif MICE: RODENT = "MICE"
                                         CranioHelperFunctions.save_design( cwd, RODENT, scale,bregma,craniotomies,screw_holes)
                                     
                        # CUTTING & DRILLING             
                        if DRILLING_CRANIOTOMY:
                        #if len(craniotomies) > 0:
                                DRILLING_SCREW_HOLES = False

                                if cur_y > skull_y:  # Prevents drilling above skull graphic
                                        
                                        #  ADD POINTS TO EXISTING LINES
                                        if len(cranio_points) == 0: 
                                                LINE_CLICKED = False
                                                cranio_idx = 0
                                                for cranio in craniotomies:
                                                        pt_idx = 0
                                                        for point in cranio:
                                                                if pt_idx< len(cranio) - 1:  # Line between points in cranio (not including line between last and first point)
                                                                        dist = dist_from_pt_to_line((cur_x,cur_y),(cranio[pt_idx],cranio[pt_idx + 1]))   #(p1 = point,  line  = (p1,p2)
                                                                else: # Line between last and first point
                                                                        dist = dist_from_pt_to_line((cur_x,cur_y),(cranio[pt_idx],cranio[0]))                 #(p1 = point,  line  = (pn,p0)
                                                                
                                                                if dist <= drill_radius:  # POINT IS TOUCHING LINE BETWEEN TWO POINTS, ADD A POINT (note: measures are in pixels)
                                                                        print("dist = ",dist, ", Craniotomy: ", cranio_idx, ", pt_idx = ",pt_idx)
                                                                        cranio.insert( pt_idx+1,(cur_x,cur_y))
                                                                        LINE_CLICKED = True
                                                                        break
                                                                   
                                                                pt_idx +=1
                                                                
                                                        if LINE_CLICKED: break
                                                        cranio_idx +=1

                                        # For PARTIAL Cranios ADD POINTS
                                        if not PATH_COMPLETE: 
                                                if len(cranio_points)-1 >=2:  # Must have 3 or more points for complete path
                                                        # If 1st point is close to last point, CLOSE PATH
                                                        if collide_point(cranio_points[0],  cur_x,cur_y,  drill_radius):
                                                                    PATH_COMPLETE =True

                                                                    craniotomies.append(cranio_points)    # Complete craniotomies
                                                                    cranio_points = []                                  # Start new craniotomy
                                                                    DRILLING_CRANIOTOMY = False
                                                                    # make last point is equal to first
                                                                    ####################################'
                                                                    # MUST ADD LAST POINT EQUAL TO FIRST FOR ROBOT TO COMPLETE PATH
                                                                    #cur_x = cranio_points[0][0]
                                                                    #cur_y = cranio_points[0][1]
                                                                    #cranio_points.append((cur_x,cur_y))

                                                if not LINE_CLICKED and not PATH_COMPLETE: # len(cranio_points)-1 < 2:
                                                        # add cranio_points to list
                                                        cranio_points.append((cur_x,cur_y))
                                        

                        if DRILLING_SCREW_HOLES:
                             if cur_y > skull_y:  # Prevents drilling above skull graphic
                                 DRILLING_CRANIOTOMY = False
                                 screw_holes.append((cur_x,cur_y))

                         

                # MOVE POINTS: COMBO of SHIFT or CNTR# Screen mm, not real mmL KEYS with Left mouse press OR MIDDLE MOUSE BUTTON press      
                elif (SHIFT_KEY_PRESSED and event.button == 1) or event.button == 2 :
                        RIGHT_MOUSE_DOWN = False
                        LEFT_MOUSE_DOWN = False
                        MID_MOUSE_DOWN = True
                        POINT_IDENTIFIED = False
                        MOVE_POINT  =False
                        MOVE_EXISTING_CRANIO_PT =False
                        MOVE_SCREW_HOLE =False
                        print("MIDDLE BUTTON")
                        print("DRILLING_CRANIOTOMY = ", DRILLING_CRANIOTOMY,  "\nDRILLING_CRANIOTOMY = ", DRILLING_CRANIOTOMY)

 
                        #if DRILLING_CRANIOTOMY:
                        idx = 0
                        for p in range(len(cranio_points)):
                            if collide_point(cranio_points[p],  cur_x,cur_y,  drill_radius):
                                    MOVE_POINT = True
                                    #EXISTING_CRANIOTOMY = False
                                    cur_point_idx = idx
                                    break
                            idx+=1

                        cranio_idx = 0
                        for cranio in craniotomies:
                                pt_idx = 0
                                for p in range(len(cranio)):
                                     if collide_point(cranio[p],  cur_x,cur_y,  drill_radius):
                                            MOVE_EXISTING_CRANIO_PT = True
                                            #EXISTING_CRANIOTOMY = True
                                            cur_cranio_idx = cranio_idx
                                            cur_point_in_cranio_idx = pt_idx
                                            break
                                     pt_idx+=1
                                cranio_idx += 1                                     
                           
                        #if DRILLING_SCREW_HOLES:
                        idx = 0
                        for h in range(len(screw_holes) ):
                            if collide_point(screw_holes[h],  cur_x,cur_y,  drill_radius):
                                    MOVE_SCREW_HOLE = True
                                    cur_hole_idx = idx
                                    break
                            idx+=1

                            
                # RIGHT MOUSE BUTTON:  DELETE points       
                elif event.button == 3:
                    RIGHT_MOUSE_DOWN = True
                    LEFT_MOUSE_DOWN = False
                    MID_MOUSE_DOWN = False

                    # PARTIAL CRANIOS
                    for p in range(len(cranio_points) ):
                        if collide_point(cranio_points[p],  cur_x,cur_y,  drill_radius):
                                cranio_points.pop(p) #Remove point
                                #cranio_points.pop #Remove closure point (last point)
                                PATH_COMPLETE = False
                                break

                    # FULL CRANIOS
                    cranio_idx = 0
                    for cranio in craniotomies:
                        for p in range(len(cranio) ):
                            if collide_point(cranio[p],  cur_x,cur_y,  drill_radius):
                                    cranio.pop(p) #Remove point
                                    if len(cranio) <=2:  # NOTE: a single point is no longer a complete path
                                          print("cranio: ", cranio)
                                          PATH_COMPLETE = False
                                          # Start a new path series with remaining points
                                          cranio_points.append(cranio[0])
                                          cranio_points.append(cranio[1])
                                          # Deltete cranio
                                          craniotomies.pop(cranio_idx)
                                    break
                        cranio_idx +=1

                        
                    # HOLES
                    for h in range(len(screw_holes) ):
                        if collide_point(screw_holes[h],  cur_x,cur_y,  drill_radius):
                                screw_holes.pop(h) #Remove point
                                break


            elif (event.type == pygame.MOUSEBUTTONUP ):#Mouse UN-Clicked
                    LEFT_MOUSE_DOWN = False
                    RIGHT_MOUSE_DOWN = False
                    MID_MOUSE_DOWN = False
                    MOVE_POINT  =False
                    MOVE_POINT  =False
                    MOVE_EXISTING_CRANIO_PT =False
                    MOVE_SCREW_HOLE =False                   
                    #SHIFT_KEY_PRESSED = False
                    cur_x = 0
                    cur_y = 0
                    for button in buttons: # Check for collision with EXISTING buttons
                               button.UP_DN = "UP"
                               button.face_color = (150,150,150),
                    print("BUTTONS UP")

        ########################
        # REDRAW GUI ELEMENTS
        ########################
        myscreen.fill(pink4)
        myscreen.blit(TNElogo,(600,5))
        
        skull_x, skull_y = 130,150
        if RATS:
            myscreen.blit(rats_skull_graphic,(130,150))  # Top left corner in pixels
        if MICE:
            myscreen.blit(mice_skull_graphic,(125,163))  # Top left corner in pixels

        bregma = (350,355) # on screen
        
       # DRAW mm GRID
        color = (200,100,100,50)
        
        for i in range (16):
            #Horizontal below bregma
            pygame.draw.line(myscreen,color,(160, bregma[1]+i*scale),(545, bregma[1]+i*scale),1)

        for i in range (9):
            # Horizontal Above Bregma
            pygame.draw.line(myscreen,color,(160,bregma[1]-i*scale),(545,bregma[1]-i*scale),1)
            #Vertical
            pygame.draw.line(myscreen,color,(bregma[0]+i*scale,155),(bregma[0]+i*scale,740),1)
            pygame.draw.line(myscreen,color,(bregma[0]-i*scale,155),(bregma[0]-i*scale,740),1)

        # Through Bregma    
        pygame.draw.line(myscreen,red,(160,bregma[1]),(545,bregma[1]),3)
        pygame.draw.line(myscreen,red,(bregma[0],155),(bregma[0],740),3)


        # DRAW ALL COMPLETE CARNIOTOMIES
        lines = []
        for cranio in craniotomies:
                p =0
                for point in cranio:
                        circ = pygame.draw.circle(myscreen, blue, point, drill_radius,0)
                        if p > 0:
                            # Draw line between points
                            pygame.draw.line(myscreen,blue,(prev_point),(point),3)
                            lines.append((prev_point,point)) # note: lines = (ptx,pty)
                        else:
                            first_point = point
                            #print("first_point: ",first_point)
                        prev_point = point
                        p+=1
                #print("last_point: ",prev_point)
                # line between 1st and last point
                pygame.draw.line(myscreen,blue,(prev_point),(first_point),3)
                lines.append((prev_point,first_point)) # note: lines = rect(ptx,pty,wd,ht)
                #print("lines: ",lines)
            
        #DRAW CRANIOTOMIES IN PROGRESS
        p =0
        for point in cranio_points:
                if PATH_COMPLETE:
                        path_color = blue
                        path_width = 3
                else:
                        path_color = red
                        path_width = 1
                    
                circ = pygame.draw.circle(myscreen, path_color, point, drill_radius,0)

                if p > 0:
                    # Draw line between points
                    pygame.draw.line(myscreen,path_color,(prev_point),(point),path_width)
                    if PATH_COMPLETE:
                            # Draw line between ist and last point
                            pygame.draw.line(myscreen,path_color,(cranio_points[0]),(cranio_points[len(cranio_points)-1]),path_width)

                prev_point = point
                p+=1

                        
        # DRAW DRILL HOLES
        for hole in screw_holes:
                circ = pygame.draw.circle(myscreen, (0,0,255), hole, drill_radius,2) # BLUE
                pygame.draw.line(myscreen,(0,0,255),(hole[0],hole[1] - 15),(hole[0], hole[1] + 15),1)
                pygame.draw.line(myscreen,(0,0,255),(hole[0] -15 ,hole[1]),(hole[0]+15, hole[1]),1)
                
        if MOVE_EXISTING_CRANIO_PT :
                    pt = craniotomies[cur_cranio_idx][cur_point_in_cranio_idx]
                    circ = pygame.draw.circle(myscreen, (0,255,0), pt, 2*drill_radius,0) # GREEN
                    pygame.draw.line(myscreen,(0,0,255),(pt[0],pt[1] - 25),(pt[0], pt[1] + 25),1)
                    pygame.draw.line(myscreen,(0,0,255),(pt[0] -25 ,pt[1]),(pt[0]+25, pt[1]),1)

        elif MOVE_POINT:
                    pt = cranio_points[cur_point_idx]
                    circ = pygame.draw.circle(myscreen, (0,255,0), pt, 2*drill_radius,0) # GREEN
                    pygame.draw.line(myscreen,(0,0,255),(pt[0],pt[1] - 25),(pt[0], pt[1] + 25),1)
                    pygame.draw.line(myscreen,(0,0,255),(pt[0] -25 ,pt[1]),(pt[0]+25, pt[1]),1)
                    
        elif MOVE_SCREW_HOLE:
                    scrw_hole = screw_holes[cur_hole_idx]
                    circ = pygame.draw.circle(myscreen, (255,255,0),scrw_hole, 2*drill_radius,0)  # GREEN
                    pygame.draw.line(myscreen,(0,0,255),(scrw_hole[0],scrw_hole[1] - 25),(scrw_hole[0], scrw_hole[1] + 25),1)
                    pygame.draw.line(myscreen,(0,0,255),(scrw_hole[0] - 25 ,scrw_hole[1]),(scrw_hole[0] + 25, scrw_hole[1]),1)                    

        #DRAW LABELS
        for lbl in labels: # Last go on top
            if  "Relocating" in lbl.text  and ( MOVE_POINT or MOVE_SCREW_HOLE or  MOVE_EXISTING_CRANIO_PT):
                    lbl.text_color = (0,0,255)
            elif DRILLING_CRANIOTOMY and "Cutting" in lbl.text:
                     lbl.text_color = (0,0,255)
            elif DRILLING_SCREW_HOLES and "Drilling" in lbl.text:
                     lbl.text_color = (0,0,255)
            elif   "Mice" in lbl.text:      
                    lbl.text_color = (150,150,150) # MICE Not implementsd yet
            else:
                    lbl.text_color = (0,0,0)
            lbl.draw()
            
        #Draw Buttons
        for button in buttons:
            button.draw()

        #Draw RADIO Buttons
        for button in radio_buttons:
            button.draw()

        # UPDATE SCREEN
        pygame.display.flip()

        

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

try:
    DrawCraniotomy() 
finally:
    print('DONE!')











