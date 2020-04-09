# craniobot
SOFTWARE INSTALATION GUIDE
1.	Install Python 3.7 or higher.   I prefer to install it as stand alone. 
    a.	During installation, choose Custom installation.  Them place your Python in  new folder.  I created one called      
        c:\python3.8.   
    b.	Be sure to Install 64 bit version if your computer is 64 bit
    c.	Be sure to add python to system path when asked.
2.	Install pygame.    
    a.	Type cmd in windows search bar at bottom left of screen 
    b.	In the pop-up command window, type: cd .. Enter, then cd .. Enter (yes, do it twice)
    c.	Then cd c:\python3.8 (or whatever directory you used above)
    d.	Then type:  pip install pygame
3.	Install numpy.      Using CMD prompt as above in 2,  type: pip install numpy
4.	Install Thorlabs-apt.      Using CMD prompt as above, type: pip install Thorlabs-apt
5.	Install ThorLabs:  https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285
    a.	 Goto Kinessis Software tab, and press the Softwate Download button.  
    b.	choose 64 bit if your computer is 64 bit. 
6.	Go to Github and clone the Thorlabs_apt depository.   See https://github.com/qpit/thorlabs_apt
    a.	In the download folder, extact all of the download.
    b.	Then run the setup.py program using install as the only argument. 
    c.	That is, type: python setup.py install
7.	Copy G:\Shared drives\TNEL - UMN\Project related material\craniobot\APT.dll into the Windows\System32 directory
8.	Copy entire craniobot directory to your desktop.  see G:\Shared drives\TNEL - UMN\Project related material\craniobot
9.	Now you should be ready to use the craniobot application.
NOTE:  Be sure to exit Craniobot using Windows exit “X” on top right of window.  If not, all motors will be locked out (that is, already in use). To fix this problem, run Thorlabs Kinesis software.  Load all three motors.  When all three alre loaded, unload all, then run Carniobot again.

RUNNING THE CRANIOBOT:
All Craniobot software is on this GITHUB.
To start run CaniobotGUI.py
All the commands you need to run the Caniobot are iconified on the screen.
1.	Using the trident stereotaxic leveling tool, be sure the rodent skull is level.
2.	Select Species.  Currently only Rats or Mice are available.
3.	Align the Craniobot with the stereotaxic equipment.   
    This is done by pushing the Craniobot snuggly against the right side of the stereotaxic equipment.   
    Secure it in place.  Taping it down to the table works fine for me.
    Remember the robot only has a 2.5 cm range of motion along each axis.  
    It is therefore desirable that the tip of the drill is roughly at the bregma when the robot  X,Y,Z is at 
    approximately (12.5 ,  12.5, 12.5).  Though X,Y,Z = 10, 10, 10 is perfectly adequate for most surgeries.   
    Best Practice:  Home the robot.  The use the XYZ buttons to move the robot to approximately X,Y,Z = 10, 10 , 10.  
    Move the entire robot assembly so that the drill is just above the Bregma.   
    Note:  The drill bit most likely can NOT be inserted entirely into the drill, rather let it stick out about 3 cm so 
    that it just touches the skull when Z is approximately 10 to 20 cm.
4.	When the robot assembly is aligned to the stereotaxic equipment and the robot is approximately in the middle of its 
    working volume (~10, ~10, ~ 10), use the XYZ move buttons to touch the drill precisely to the Bregma.    
    Then press the SELECT BREGMA button.   You should see a red circle and cross-hairs over the bregma graphic.    
5.	Select an Existing Craniotomy or Create New Craniotomy Path.  
    Any pre-existing craniotomy path can be edited using the Craniotomy Designer stand alone application by pressing the 
    Create New Craniotomy Path button.
6.	Be sure drill is ON and  going in the FWD direction.
7.	CRANIOTOMY: Press Craniotomy button.   One pass of the entire craniotomy path depicted in the screen graphics will be 
    reproduced by the robot.   
8.	Repeat Step 5.  On each pass, the drill will cut the path 0.1 mm deeper.  
    Repeat until through skull (approximately 10 passes).    NOTE:  The craniobot assumes that the rodent skull is level.
9.	SCREW HOLES: Next press Next Hole Button to create screw holes. When the drill stops, used the Z axis motion control 
    button to go deeper if necessary.  When drilled to the depth you desire, press the Next Hole button to go to the next 
    hole location
    
    Using the CraniotomyDesigner:
The Craniotomy Designer is a separate, but fully integrated module that is used to design craniotomy paths for the Craniobot.    It can be run as a stand-alone software, or called from the CraniobotGUI application.  The GUI should be self explanatory.  Click on the button icons to load an existing craniotomy path, create simple circular craniotomies, created complex arbitrary craniotomies, add screw-hole locations, save or clear the screen.  As soon as the mouse is dragged over the window, the cursor location (in skull coordinates) appear next to it.  

Making a circular craniotomy: When the circular craniotomy button is pressed, user input boxes appear on the left of the skull graphic.  Click on the box, its outline will turn red, then type the desired values for the radius, and the X and Y offsets from the Bregma.  As soon as the last value is entered, a path for the robot to follow will appear on the screen.   To add a point, simply select the create craniotomy button, then simply click anywhere on a blue line.  Another point will be added.  To delete a point, left click on any point and it will disappear.   To Move an existing point, hold down the shift key while left clicking on a point, then move it to anywhere on the screen.  
Making a craniotomy with an arbitrary path:  To create an arbitrary path, simply click on the Create Craniotomy Button.  Using the left mouse button, place points (in red) on the skull graphic.  Multiple points will constitute a path along the X and Y axes for the robot to follow.  When the path is complete, the resulting closed path will turn blue.  Move points by simultaneously holding down the SHIFT key and left clicking on a point.  Add points by clicking anywhere on an existing line. 
Adding Screw Holes:  Simply click on the Add Screw Holes button, then left click the mouse on any point on the skull.  The robot will go to that point and drill along the Z-axis.   
FINISHING IT UP:  When happy with your design, simply press the Save button.  All craniotomy patterns are stored in the CRANIOTOMY DESIGNS folder.  Now simply run the craniotomy robot, and load your desired path.

