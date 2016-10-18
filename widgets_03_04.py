
from numpy import *
from tkinter import *
from math import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

class cl_widgets:

    def __init__(self, ob_root_window, ob_world=[]):
        self.ob_root_window = ob_root_window
        self.ob_world = ob_world
        self.ob_loadfile_frame = cl_loadfile_frame(ob_root_window, ob_world)
        self.ob_loadfile_frame.frame.pack(side=TOP)
        self.ob_rotate_frame = cl_rotate_frame(ob_root_window, ob_world)
        self.ob_scale_frame = cl_scale_frame(ob_root_window, ob_world)
        self.ob_translate_frame = cl_translate_frame(ob_root_window, ob_world)
        self.ob_fly_frame = cl_fly_frame(ob_root_window, ob_world)
        self.ob_canvas_frame = cl_canvas_frame(ob_root_window)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)


class cl_canvas_frame:

    def __init__(self, master):
        self.canvas = Canvas(width=640, height=480, bg='yellow')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.master = master
        self.canvas.bind('<Configure>', self.canvas_resized_callback)
        self.canvas.bind('<ButtonPress-1>', self.left_mouse_click_callback)
        self.canvas.bind('<Up>', self.up_arrow_pressed_callback)
        self.canvas.bind('<Down>', self.down_arrow_pressed_callback)
        self.canvas.bind('<Right>', self.right_arrow_pressed_callback)
        self.canvas.bind('<Left>', self.left_arrow_pressed_callback)
        self.canvas.bind('<Shift-Up>', self.shift_up_arrow_pressed_callback)
        self.canvas.bind('<Shift-Down>', self.shift_down_arrow_pressed_callback)
        self.canvas.bind('<Shift-Right>', self.shift_right_arrow_pressed_callback)
        self.canvas.bind('<Shift-Left>', self.shift_left_arrow_pressed_callback)

    def up_arrow_pressed_callback(self, event):
        self.canvas.world.rotate_around_line(-4, 1, [0, 0, 0], [1, 0, 0])

    def down_arrow_pressed_callback(self, event):
        self.canvas.world.rotate_around_line(4, 1, [0, 0, 0], [1, 0, 0])

    def right_arrow_pressed_callback(self, event):
        self.canvas.world.rotate_around_line(4, 1, [0, 0, 0], [0, 1, 0])

    def left_arrow_pressed_callback(self, event):
        self.canvas.world.rotate_around_line(-4, 1, [0, 0, 0], [0, 1, 0])

    def shift_up_arrow_pressed_callback(self, event):
        self.canvas.world.translate(0, 0.1, 0, 1)

    def shift_down_arrow_pressed_callback(self, event):
        self.canvas.world.translate(0, -0.1, 0, 1)

    def shift_right_arrow_pressed_callback(self, event):
        self.canvas.world.translate(0.1, 0, 0, 1)

    def shift_left_arrow_pressed_callback(self, event):
        self.canvas.world.translate(-0.1, 0, 0, 1)

    def left_mouse_click_callback(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.focus_set()

    def left_mouse_release_callback(self, event):
        self.x = None
        self.y = None

    def left_mouse_down_motion_callback(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        if abs(deltax) > 10:
            deltax = sign(deltax) * 10
        if abs(deltay) > 10:
            deltay = sign(deltay) * 10
        angle_deg = sqrt(deltax * deltax + deltay * deltay)
        self.canvas.world.rotate_around_line(angle_deg, 1, [0, 0, 0], [deltay, deltax, 0])
        self.x = event.x
        self.y = event.y

    def right_mouse_click_callback(self, event):
        self.x = event.x
        self.y = event.y

    def right_mouse_release_callback(self, event):
        self.x = None
        self.y = None

    def right_mouse_down_motion_callback(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        if abs(deltay) > 10:
            deltay = sign(deltay) * 10
        if deltay > 0:
            scaleFactor = 1.0 - float(deltay) / 20.0
        else:
            scaleFactor = 1.0 - float(deltay) / 10.0
        self.canvas.world.scale(scaleFactor, scaleFactor, scaleFactor, 1)
        self.x = event.x
        self.y = event.y

    def canvas_resized_callback(self, event):
        self.canvas.config(width=event.width - 4, height=event.height - 4)
        self.canvas.pack()
        self.canvas.world.take_pictures()


class cl_loadfile_frame:

    def __init__(self, master, world):
        self.frame = Frame(master)
        self.frame.pack(side=TOP)
        self.var_filename = StringVar()
        self.var_filename.set('')
        self.ask_filename = Label(self.frame, text='Filename: ')
        self.ask_filename.pack(side=LEFT)
        self.filename = Entry(self.frame, textvariable=self.var_filename)
        self.filename.pack(side=LEFT)
        self.button = Button(self.frame, text='Browse', fg='blue', command=self.browse_file)
        self.button.pack(side=LEFT)
        self.button = Button(self.frame, text='Load', fg='red', command=lambda : world.load_file(self.var_filename.get()))
        self.button.pack(side=LEFT)

    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[('allfiles', '*'), ('pythonfiles', '*.txt')]))

    def file_load(self):
        filename = self.var_filename.get()
        self.My_3D_Object, self.My_Camera = file_to_object(filename)
        self.My_3D_World = world()
        self.My_3D_World.append(self.My_3D_Object)
        self.cameras_name = self.world.get_camera_list()
        self.camera_var = StringVar()
        self.camera_menu = OptionMenu(self, self.camera_var, *self.cameras_name)
        self.camera_menu.configure(state=NORMAL)
        self.camera_menu.pack(side=LEFT)
        self.frame.My_Camera.show(self.myCanvas, self.My_3D_World)
        self.frame.myCanvas.update_idletasks()


class cl_scale_frame:

    def __init__(self, master, world):
        frame = Frame(master)
        frame.pack(side=TOP)
        self.label_axis = Label(frame, text='Scale Ratio:', relief=FLAT)
        self.label_axis.pack(side=LEFT)
        self.var_zoom_mode = IntVar()
        self.var_zoom_mode.set(0)
        R1 = Radiobutton(frame, text='All', variable=self.var_zoom_mode, value=0, command=self.ZoomMode)
        R1.pack(anchor=W, side=LEFT)
        self.world = world
        self.zoom_factor_all = StringVar()
        Range = ['0.25',
         '0.5',
         '0.75',
         '1',
         '1.25',
         '1.5',
         '1.75',
         '2',
         '2.25',
         '2.5',
         '2.75',
         '3',
         '3.25',
         '3.5',
         '3.75',
         '4']
        self.zoomfactor_all = Spinbox(frame, values=Range, width=4, textvariable=self.zoom_factor_all, command=self.ZoomMode)
        self.zoomfactor_all.pack(side=LEFT)
        self.zoom_factor_all.set('1')
        R2 = Radiobutton(frame, text='[Sx,Sy,Sz]', variable=self.var_zoom_mode, value=1, command=self.ZoomMode)
        R2.pack(anchor=W, side=LEFT)
        self.zoom_factor_xyz = StringVar()
        self.zoomfactor_xyz = Entry(frame, textvariable=self.zoom_factor_xyz, width=10, state=DISABLED)
        self.zoomfactor_xyz.pack(side=LEFT)
        self.zoom_factor_xyz.set('[1,1,1]')
        self.label_scale_ref_point = Label(frame, text='Ref. Point:', relief=FLAT)
        self.label_scale_ref_point.pack(side=LEFT)
        self.scale_ref_xyz = StringVar()
        self.scale_ref_box = Entry(frame, textvariable=self.scale_ref_xyz, width=10)
        self.scale_ref_box.pack(side=LEFT)
        self.scale_ref_xyz.set('[0.0,0.0,0.0]')
        self.label_steps = Label(frame, text='Steps', relief=FLAT)
        self.label_steps.pack(side=LEFT)
        self.var_steps = StringVar()
        self.var_steps.set('4')
        self.spinbox_steps = Spinbox(frame, from_=0, to=10, width=3, textvariable=self.var_steps, command=self.Steps)
        self.spinbox_steps.pack(side=LEFT)
        self.button = Button(frame, text='Scale', fg='blue', command=self.scale)
        self.button.pack(side=LEFT)

    def Steps(self):
        print('Step size ', self.var_steps.get(), ' is selected!')

    def ZoomMode(self):
        if self.var_zoom_mode.get() == 0:
            self.zoomfactor_xyz.configure(state=DISABLED)
            self.zoomfactor_all.configure(state=NORMAL)
            Ratio = float(self.zoom_factor_all.get())
            print('Scale Ratio = ', Ratio, ' is selected for all dimensions!')
            self.zoom_ratio = [Ratio, Ratio, Ratio]
        if self.var_zoom_mode.get() == 1:
            self.zoomfactor_xyz.configure(state=NORMAL)
            self.zoomfactor_all.configure(state=DISABLED)
            print('Scale Ratio = ', self.zoom_factor_xyz.get(), ' is selected!')
            InputString = self.zoom_factor_xyz.get().strip('[]')
            self.zoom_ratio = InputString.split(',')

    def scale(self):
        self.ZoomMode()
        steps = int(self.spinbox_steps.get())
        sx, sy, sz = self.zoom_ratio
        P = self.scale_ref_xyz.get().strip('[]')
        P = P.split(',')
        P = [float(P[0]), float(P[1]), float(P[2])]
        self.world.scale_around_a_point(sx, sy, sz, steps, P)


class cl_translate_frame:

    def __init__(self, master, world):
        self.world = world
        frame = Frame(master)
        frame.pack(side=TOP)
        self.label_axis = Label(frame, text='Translation ([dx, dy, dz]):', relief=FLAT)
        self.label_axis.pack(side=LEFT)
        self.translation_xyz = StringVar()
        self.translation_box = Entry(frame, textvariable=self.translation_xyz, width=10)
        self.translation_box.pack(side=LEFT)
        self.translation_xyz.set('[10,10,10]')
        self.label_steps = Label(frame, text='Steps', relief=FLAT)
        self.label_steps.pack(side=LEFT)
        self.var_steps = StringVar()
        self.var_steps.set('4')
        self.spinbox_steps = Spinbox(frame, from_=0, to=10, width=3, textvariable=self.var_steps, command=self.Steps)
        self.spinbox_steps.pack(side=LEFT)
        self.button = Button(frame, text='Translate', fg='blue', command=self.translate)
        self.button.pack(side=LEFT)

    def Steps(self):
        print('Step size ', self.var_steps.get(), ' is selected!')

    def translate(self):
        print('Translation Ratio = ', self.translation_box.get(), ' is selected!')
        InputString = self.translation_box.get().strip('[]')
        self.translation_values = InputString.split(',')
        steps = int(self.spinbox_steps.get())
        sx, sy, sz = self.translation_values
        self.world.translate(sx, sy, sz, steps)


class cl_fly_frame:

    def __init__(self, master, world):
        self.world = world
        self.frame = Frame(master)
        self.frame.pack(side=TOP)
        self.button = Button(self.frame, text='Fly Camera...', fg='blue', command=self.fly_window)
        self.button.pack(side=LEFT)

    def Steps(self):
        print('Step size ', self.var_steps.get(), ' is selected!')

    def fly_window(self):
        self.top = Toplevel()
        self.top.title('Select Camera')
        self.cameras_name = self.world.get_camera_list()
        self.camera_var = StringVar()
        if len(self.cameras_name):
            self.camera_var.set(self.cameras_name[0])
            self.camera_number_to_fly = 0
        else:
            self.camera_var.set('load file first!')
        self.label_camera = Label(self.top, text='Select Camera to Fly:', relief=FLAT)
        self.label_camera.pack(side=LEFT)
        camera_menu = OptionMenu(self.top, self.camera_var, command=self.combo_selected, *self.cameras_name)
        camera_menu.pack(side=LEFT)
        self.top.label_fly_1 = Label(self.top, text='Current VRP([x,y,z]):', relief=FLAT)
        self.top.label_fly_1.pack(side=LEFT)
        self.top.fly_1 = StringVar()
        self.top.fly_1_box = Entry(self.top, textvariable=self.top.fly_1, width=10)
        self.top.fly_1_box.pack(side=LEFT)
        self.top.fly_1.set('[0,0,0]')
        self.top.label_fly_2 = Label(self.top, text='VRP 2([x,y,z]):', relief=FLAT)
        self.top.label_fly_2.pack(side=LEFT)
        self.top.fly_2 = StringVar()
        self.top.fly_2_box = Entry(self.top, textvariable=self.top.fly_2, width=10)
        self.top.fly_2_box.pack(side=LEFT)
        self.top.fly_2.set('[1,1,1]')
        self.top.label_steps = Label(self.top, text='Steps', relief=FLAT)
        self.top.label_steps.pack(side=LEFT)
        self.top.var_steps = StringVar()
        self.top.var_steps.set('10')
        self.top.spinbox_steps = Spinbox(self.top, from_=0, to=10, width=3, textvariable=self.top.var_steps, command=self.Steps)
        self.top.spinbox_steps.pack(side=LEFT)
        camera_button = Button(self.top, text='Fly', fg='blue', width=10, command=self.fly)
        camera_button.pack()

    def combo_selected(self, q):
        for camera_count in range(0, len(self.world.cameras)):
            if self.camera_var.get() == self.world.cameras[camera_count].camera_name:
                break
                continue

        self.camera_number_to_fly = camera_count
        VRP = self.world.cameras[camera_count].vrp
        self.top.fly_1.set(VRP)

    def fly(self):
        InputString = self.top.fly_1_box.get().strip('[]')
        self.vrp1_values = InputString.split(',')
        x1, y1, z1 = self.vrp1_values
        InputString = self.top.fly_2_box.get().strip('[]')
        self.vrp2_values = InputString.split(',')
        x2, y2, z2 = self.vrp2_values
        self.x1, self.y1, self.z1 = float(x1), float(y1), float(z1)
        self.x2, self.y2, self.z2 = float(x2), float(y2), float(z2)
        self.steps = int(self.top.spinbox_steps.get())
        self.world.fly(self.camera_number_to_fly, self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.steps)
        self.top.fly_2.set(self.top.fly_1_box.get())
        self.top.fly_1.set(InputString)


class cl_statusBar_frame:

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text='')
        self.label.update_idletasks()


class cl_rotate_frame:

    def __init__(self, master, world):
        frame = Frame(master)
        frame.pack(side=TOP)
        self.label_axis = Label(frame, text='Rotation Axis:', relief=FLAT)
        self.label_axis.pack(side=LEFT)
        self.world = world
        self.var_rotation_axis = StringVar()
        self.var_rotation_axis.set('z')
        R1 = Radiobutton(frame, text='X', variable=self.var_rotation_axis, value='x', command=self.GetAxis)
        R1.pack(anchor=W, side=LEFT)
        R2 = Radiobutton(frame, text='Y', variable=self.var_rotation_axis, value='y', command=self.GetAxis)
        R2.pack(anchor=W, side=LEFT)
        R3 = Radiobutton(frame, text='Z', variable=self.var_rotation_axis, value='z', command=self.GetAxis)
        R3.pack(anchor=W, side=LEFT)
        R4 = Radiobutton(frame, text='Line AB', variable=self.var_rotation_axis, value='line', command=self.GetAxis)
        R4.pack(anchor=W, side=LEFT)
        self.label_A = Label(frame, text='A:', relief=FLAT)
        self.label_A.pack(side=LEFT)
        self.var_A = StringVar()
        self.Point_A = Entry(frame, textvariable=self.var_A, width=10, state=DISABLED)
        self.Point_A.pack(side=LEFT)
        self.var_A.set('[0.0,0.0,0.0]')
        self.label_B = Label(frame, text='B:', relief=FLAT)
        self.label_B.pack(side=LEFT)
        self.var_B = StringVar()
        self.Point_B = Entry(frame, textvariable=self.var_B, width=10, state=DISABLED)
        self.Point_B.pack(side=LEFT)
        self.var_B.set('[1.0,1.0,1.0]')
        self.label_degree = Label(frame, text='Degree:', relief=FLAT)
        self.label_degree.pack(side=LEFT)
        self.var_degree = StringVar()
        self.spinbox_degree = Spinbox(frame, values=range(0, 360, 10), width=3, textvariable=self.var_degree, command=self.Degrees)
        self.spinbox_degree.pack(side=LEFT)
        self.var_degree.set('90')
        self.label_steps = Label(frame, text='Steps:', relief=FLAT)
        self.label_steps.pack(side=LEFT)
        self.var_steps = StringVar()
        self.var_steps.set('5')
        self.spinbox_steps = Spinbox(frame, from_=0, to=10, width=3, textvariable=self.var_steps, command=self.Steps)
        self.spinbox_steps.pack(side=LEFT)
        self.button = Button(frame, text='Rotate', fg='blue', command=self.rotate)
        self.button.pack(side=LEFT)

    def Degrees(self):
        print('Degree ', self.var_degree.get(), ' is selected!')

    def Steps(self):
        print('Step size ', self.var_steps.get(), ' is selected!')

    def GetAxis(self):
        selection = 'Rotation Axis ' + str(self.var_rotation_axis.get()) + ' is selected!'
        print(selection)
        if str(self.var_rotation_axis.get()) == 'line':
            self.Point_A.configure(state=NORMAL)
            self.Point_B.configure(state=NORMAL)
        else:
            self.Point_A.configure(state=DISABLED)
            self.Point_B.configure(state=DISABLED)

    def rotate(self):
        angle_d = float(self.spinbox_degree.get())
        steps = int(self.spinbox_steps.get())
        if not str(self.var_rotation_axis.get()) == 'line':
            self.world.rotate_around_axis(angle_d, steps, str(self.var_rotation_axis.get()))
        else:
            A = self.var_A.get().strip('[]')
            A = A.split(',')
            A = [float(A[0]), float(A[1]), float(A[2])]
            B = self.var_B.get().strip('[]')
            B = B.split(',')
            B = [float(B[0]), float(B[1]), float(B[2])]
            self.world.rotate_around_line(angle_d, steps, A, B)


def close_window_callback(root):
    if messagebox.askokcancel('Quit', 'Do you really wish to quit?'):
        root.destroy()


def menu_callback():
    print('called the menu callback!')


def menu_help_callback():
    print('called the help menu callback!')


def toolbar_callback():
    print('called the toolbar callback!')

