from tkinter import filedialog
from tkinter import *
import os

def load_design(cwd,scale,bregma):
     screw_holes = []
     craniotomies=[]
     root = Tk()
     craniodir = os.path.join(cwd,"CRANIOTOMY_DESIGNS")
     print(craniodir)
     craniopath = filedialog.askopenfile(initialdir = craniodir, title = "Select file", defaultextension='.txt', filetypes = (('Text files', '*.txt'),('All files', '*.*')))
     print ("Craniopath: ",craniopath)
     craniofile = craniopath.name
     print ("Chosen File: ",craniofile )
     
     if craniofile  is None:
              print("RETURNING EMPTY")
     else:
             print("bregma: ",bregma)
             f= open(craniofile, "r")
             for ln in f:
                        print(ln)
                        # Load Craniotomies:
                        if "[TARGET]" in ln:
                             LOADING_CRANIOS =False
                             LOADING_SCREW_HOLES = False
                             TARGET = True                    
                        if "[CRANIOTOMIES]" in ln:
                             LOADING_CRANIOS =True
                             LOADING_SCREW_HOLES = False
                             TARGET = False
                             craniotomies_scrn = []
                             craniotomies_rat = []

                        elif "[SCREW HOLES]" in ln:
                             LOADING_SCREW_HOLES = True
                             LOADING_CRANIOS = False
                             TARGET = False
                             screw_holes_scrn =[]
                             screw_holes_rat =[]

                        elif TARGET:
                             upper_ln = ln.upper()
                             if "RAT" in upper_ln:
                                  RODENT = "RATS"

                             if "MICE" in upper_ln or "MOUSE" in upper_ln:
                                  RODENT = "MICE"
                       
                        elif LOADING_CRANIOS:
                            print("CRANIOTOMIES")
                            points_scrn = []
                            points_rat = []
                            points = []
                            # One craniotomy per line
                            pts = ln.split(';')
                            #print("points: ",pts)
                            try:
                                for p in pts:
                                          for c in '[()]': #Remove parenthesis from rewards
                                                p = p.replace(c, "")
                                          print("point: ",p)
                                          xy = p.split(",")
                                          x = int(float(xy[0]))
                                          y = int(float(xy[1]))
                                          points_rat.append((x,y))

                                          x = int(float(xy[0])*scale)+bregma[0]
                                          y = int(float(xy[1])*scale)+bregma[1]
                                          points_scrn.append((x,y))
                                #print(points)
                                craniotomies_scrn.append(points_scrn)
                                craniotomies_rat.append(points_rat)                             
                            except:
                                 print("ERROR LOADING CRANIOTOMIES")
                            print("CRANIO",craniotomies_rat,"\n")
                                 
                        elif LOADING_SCREW_HOLES:
                            print("SCREWHOLES")
                            pts = ln.split(';')
                            try:
                                for p in pts:
                                     for c in '()': #Remove parenthesis from rewards
                                           p = p.replace(c, "")
                                     print("point: ",p)
                                     xy = p.split(",")
                                     x = int(float(xy[0]))
                                     y = int(float(xy[1]))
                                     screw_holes_rat.append((x,y))
                                     x = int(float(xy[0])*scale)+bregma[0]
                                     y = int(float(xy[1])*scale)+bregma[1]
                                     screw_holes_scrn.append((x,y))
                            
                            except:
                                 print("ERROR LOADING DRILL HOLES")
             f.close()
             root.destroy()
             return RODENT, screw_holes_scrn, screw_holes_rat, craniotomies_scrn, craniotomies_rat

          
def save_design(cwd,RODENT, scale,bregma,craniotomies,screw_holes):
           craniodir = os.path.join(cwd,"CRANIOTOMY_DESIGNS")
           print(craniodir)
           root = Tk()
           craniopath = filedialog.asksaveasfile(initialdir = craniodir, title = "Save file", defaultextension='.txt', filetypes = (('Text files', '*.txt'),('All files', '*.*')))
           print ("Craniopath: ",craniopath)
           craniofile = craniopath.name
           print ("Chosen File: ",craniofile )
           if craniofile  is None:
                print("RETURNING EMPTY")
                     
           else:
               print("bregma: ",bregma)
               with open(craniofile, "w") as f:
                          # save Craniotomies
                          f.write("[TARGET]\n")
                          if "RATS" in RODENT:
                               f.write("RATS\n")
                          elif "MICE" in RODENT:
                               f.write("MICE\n")
                          f.write("[CRANIOTOMIES]\n")
                          mystring = ""
                          idx = 0
                          for c in craniotomies:
                              #mystring = mystring + "["
                              #print("Crainotomy: ",c)
                              for pt in c:
                                      #print("Point: ",pt)
                                      x = round((pt[0] - bregma [0]) / scale, 2)
                                      y = round((pt[1] - bregma [1]) / scale, 2)                                                                  
                                      mystring +=  "(" + str(x)+"," + str(y) + ");"
                              mystring=mystring[:-1]     # Remove comma
                              mystring=mystring +"]\n" # close bracket, add new line
                              print("        ",idx, mystring)
                              idx+=1
                              
                          mystring=mystring[:-2]     # Remove new line and final comma
                          print("mystring: ",mystring)
                          mystring=mystring +"\n"   #add new line
                          
                          f.write(mystring)

                          # save drill holes
                          f.write("[SCREW HOLES]\n")
                          mystring = ""
                          for h in screw_holes:
                                   #print("hole: ",h)
                                   x = round((h[0] - bregma [0]) / scale, 2)
                                   y = round((h[1] - bregma [1]) / scale, 2)
                                   mystring +=  "(" + str(x)+"," + str(y) + ");"
                          mystring=mystring[:-1]   # Remove final comma
                          mystring=mystring +"\n" # add new line
                          f.write(mystring)

           f.close()
           root.destroy()
           print("DONE WRITING?")



