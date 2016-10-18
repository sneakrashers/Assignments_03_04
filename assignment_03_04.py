from tkinter import *
from widgets_03_04 import *
from graphic_03_04 import *

ob_root_window = Tk()
ob_root_window.protocol("WM_DELETE_WINDOW", lambda root_window=ob_root_window: close_window_callback(root_window))
#ob_root_window.resizable(0,0)
ob_world=cl_world()
cl_widgets(ob_root_window,ob_world)
ob_root_window.mainloop()
