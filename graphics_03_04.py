
from numpy import *
from math import *
from tkinter import *

class cl_world:

    def __init__(self, objects=[], cameras=[], canvases=[]):
        self.objects = objects
        self.cameras = cameras
        self.canvases = canvases
        self.number_of_edges = 0
        self.number_of_vertices = 0
        self.number_of_faces = 0
        self.new_objects_are_loaded_flag = False

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self
        self.load_cameras_file()

    def add_camera(self, camera_name, projection_type, vrp, vpn, vup, prp, w, s, canvas):
        self.cameras.append(cl_camera(camera_name, projection_type, vrp, vpn, vup, prp, w, s, canvas))
        self.cameras[-1].world = self

    def del_cameras(self):
        self.cameras = []

    def del_objects(self):
        self.objects = []

    def load_file(self, filename):
        fid = open(filename, 'r')
        lines = fid.readlines()
        fid.close()
        vertices = []
        faces = []
        number_of_edges = 0
        for line in lines:
            line = line.split()
            if line == []:
                continue
            if line[0] == 'v':
                vertices.append([float(line[1]),
                 float(line[2]),
                 float(line[3]),
                 1])
            if line[0] == 'f':
                number_of_edges = number_of_edges + len(line) - 1
                temp_list = []
                for k in range(1, len(line)):
                    temp_list.append(int(line[k]) - 1)

                faces.append(temp_list)
                continue

        vertices = array(vertices)
        self.number_of_vertices = len(vertices)
        faces = array(faces)
        self.number_of_edges = number_of_edges
        self.number_of_faces = len(faces)
        self.del_objects()
        self.objects.append(cl_object_3D(vertices.transpose(), faces.transpose()))
        self.new_objects_are_loaded_flag = True
        self.take_pictures()
        self.new_objects_are_loaded_flag = False

    def get_camera_list(self):
        out = []
        for camera in self.cameras:
            out.append(camera.camera_name)

        return out

    def load_cameras_file(self):
        fid = open('cameras.txt', 'r')
        lines = fid.readlines()
        fid.close()
        previous_camera_exist_flag = False
        self.del_cameras()
        for line in lines:
            line = line.split()
            if line == []:
                continue
            if line[0] == 'c':
                if previous_camera_exist_flag:
                    self.add_camera(camera_name, projection_type, vrp, vpn, vup, prp, window_3d, viewport, self.canvases[0])
                previous_camera_exist_flag = True
                projection_type = 'parallel'
                vrp = [0, 0, 0]
                vpn = [0, 0, 1]
                vup = [0, 1, 0]
                prp = [0, 0, 1]
                window_3d = [-1,
                 1,
                 -1,
                 1,
                 -1,
                 1]
                viewport = [0.1,
                 0.1,
                 0.4,
                 0.4]
            if line[0] == 'w':
                window_3d = [float(line[1]),
                 float(line[2]),
                 float(line[3]),
                 float(line[4]),
                 float(line[5]),
                 float(line[6])]
            if line[0] == 's':
                viewport = [float(line[1]),
                 float(line[2]),
                 float(line[3]),
                 float(line[4])]
            if line[0] == 'r':
                vrp = [float(line[1]), float(line[2]), float(line[3])]
            if line[0] == 'n':
                vpn = [float(line[1]), float(line[2]), float(line[3])]
            if line[0] == 'u':
                vup = [float(line[1]), float(line[2]), float(line[3])]
            if line[0] == 'p':
                prp = [float(line[1]), float(line[2]), float(line[3])]
            if line[0] == 'i':
                camera_name = ' '.join(line[1:])
            if line[0] == 't':
                projection_type = line[1].lower()
                continue

        if previous_camera_exist_flag:
            self.add_camera(camera_name, projection_type, vrp, vpn, vup, prp, window_3d, viewport, self.canvases[0])
        self.take_pictures()

    def take_pictures(self):
        for camera_index in range(0, len(self.cameras)):
            if self.cameras[camera_index]:
                self.cameras[camera_index].take_picture()
                continue

    def fly(self, camera_number_to_fly, x1, y1, z1, x2, y2, z2, steps):
        delta_x = (x2 - x1) / steps
        delta_y = (y2 - y1) / steps
        delta_z = (z2 - z1) / steps
        if self.cameras:
            current_camera = self.cameras[camera_number_to_fly]
            for step_idx in range(0, steps + 1):
                current_camera.vrp = [x1 + step_idx * delta_x, y1 + step_idx * delta_y, z1 + step_idx * delta_z]
                self.take_pictures()

    def rotate_around_line(self, angle_d, steps, A, B):
        degreeInEachStep = float(angle_d) / float(steps)
        for object_3d in self.objects:
            if object_3d:
                for k in range(1, steps + 1):
                    object_3d.rotate_around_line(degreeInEachStep, A, B)
                    self.take_pictures()

    def rotate_around_axis(self, angle_d, steps, axis):
        degreeInEachStep = float(angle_d) / float(steps)
        for object_3d in self.objects:
            if object_3d:
                for k in range(1, steps + 1):
                    object_3d.rotate_around_axis(degreeInEachStep, axis)
                    self.take_pictures()

    def scale_around_a_point(self, sx, sy, sz, steps, P):
        xscaleInEachStep = exp(log(float(sx)) / float(steps))
        yscaleInEachStep = exp(log(float(sy)) / float(steps))
        zscaleInEachStep = exp(log(float(sz)) / float(steps))
        for object_3d in self.objects:
            if object_3d:
                for k in range(1, steps + 1):
                    object_3d.scale_around_a_point(xscaleInEachStep, yscaleInEachStep, zscaleInEachStep, P)
                    self.take_pictures()

    def translate(self, dx, dy, dz, steps):
        dxInEachStep = float(dx) / float(steps)
        dyInEachStep = float(dy) / float(steps)
        dzInEachStep = float(dz) / float(steps)
        for object_3d in self.objects:
            if object_3d:
                for k in range(1, steps + 1):
                    object_3d.translate(dxInEachStep, dyInEachStep, dzInEachStep)
                    self.take_pictures()


class cl_camera:

    def __init__(self, camera_name, projection_type, vrp, vpn, vup, prp, w, s, canvas):
        self.camera_name = camera_name
        self.w = w
        self.s = s
        self.vrp = vrp
        self.vpn = vpn
        self.vup = vup
        self.prp = prp
        self.umin, self.umax, self.vmin, self.vmax, self.nmin, self.nmax = self.w
        self.xmin, self.ymin, self.xmax, self.ymax = self.s
        self.projection_type = projection_type
        self.canvas = canvas
        self.temp = ''
        self.viewport = False
        self.text = False
        self.line_handles = []
        self.u_axis = cross(array(self.vpn), array(self.vup))

    def add_world(self, world):
        self.world = world

    def composite_parallel(self):
        T1 = array([[1,
          0,
          0,
          -float(self.vrp[0])],
         [0,
          1,
          0,
          -float(self.vrp[1])],
         [0,
          0,
          1,
          -float(self.vrp[2])],
         [0,
          0,
          0,
          1]])
        a, b, c = self.vpn
        temp_denom = sqrt(b * b + c * c)
        if temp_denom == 0:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              c / temp_denom,
              -b / temp_denom,
              0],
             [0,
              b / temp_denom,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        a, b, c, d = Rx.dot(array([a,
         b,
         c,
         1]))
        temp_denom = sqrt(a * a + c * c)
        if temp_denom == 0:
            Ry = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Ry = array([[c / temp_denom,
              0,
              -a / temp_denom,
              0],
             [0,
              1,
              0,
              0],
             [a / temp_denom,
              0,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        a, b, c = self.vup
        a, b, c, d = Ry.dot(Rx.dot(array([a,
         b,
         c,
         1])))
        temp_denom = sqrt(a * a + b * b)
        if temp_denom == 0:
            Rz = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Rz = array([[b / temp_denom,
              -a / temp_denom,
              0,
              0],
             [a / temp_denom,
              b / temp_denom,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        if self.prp[2] == 0:
            Sh = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Sh = array([[1,
              0,
              -(self.prp[0] - (self.umin + self.umax) / 2) / self.prp[2],
              0],
             [0,
              1,
              -(self.prp[1] - (self.vmin + self.vmax) / 2) / self.prp[2],
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        T2 = array([[1,
          0,
          0,
          -min(self.umin, self.umax)],
         [0,
          1,
          0,
          -min(self.vmin, self.vmax)],
         [0,
          0,
          1,
          -min(self.nmin, self.nmax)],
         [0,
          0,
          0,
          1]])
        S = array([[1 / abs(self.umax - self.umin),
          0,
          0,
          0],
         [0,
          1 / abs(self.vmax - self.vmin),
          0,
          0],
         [0,
          0,
          1 / abs(self.nmax - self.nmin),
          0],
         [0,
          0,
          0,
          1]])
        C = S.dot(T2.dot(Sh.dot(Rz.dot(Ry.dot(Rx.dot(T1))))))
        return C

    def composite_perspective(self):
        T1 = array([[1,
          0,
          0,
          -float(self.vrp[0])],
         [0,
          1,
          0,
          -float(self.vrp[1])],
         [0,
          0,
          1,
          -float(self.vrp[2])],
         [0,
          0,
          0,
          1]])
        a, b, c = self.vpn
        temp_denom = sqrt(b * b + c * c)
        if temp_denom == 0:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              c / temp_denom,
              -b / temp_denom,
              0],
             [0,
              b / temp_denom,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        a, b, c, d = Rx.dot(array([a,
         b,
         c,
         1]))
        temp_denom = sqrt(a * a + c * c)
        if temp_denom == 0:
            Ry = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Ry = array([[c / temp_denom,
              0,
              -a / temp_denom,
              0],
             [0,
              1,
              0,
              0],
             [a / temp_denom,
              0,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        a, b, c = self.vup
        a, b, c, d = Ry.dot(Rx.dot(array([a,
         b,
         c,
         1])))
        temp_denom = sqrt(a * a + b * b)
        if temp_denom == 0:
            Rz = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Rz = array([[b / temp_denom,
              -a / temp_denom,
              0,
              0],
             [a / temp_denom,
              b / temp_denom,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        T2 = array([[1,
          0,
          0,
          -self.prp[0]],
         [0,
          1,
          0,
          -self.prp[1]],
         [0,
          0,
          1,
          -self.prp[2]],
         [0,
          0,
          0,
          1]])
        if self.prp[2] == 0:
            Sh = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Sh = array([[1,
              0,
              -(self.prp[0] - (self.umin + self.umax) / 2) / self.prp[2],
              0],
             [0,
              1,
              -(self.prp[1] - (self.vmin + self.vmax) / 2) / self.prp[2],
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        if (-self.prp[2] + self.nmax) * (-self.prp[2] + self.nmin) < 0:
            print('Error: two sided volume')
            C = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
            return (C, 0.5)
        if abs(-self.prp[2] + self.nmax) > abs(-self.prp[2] + self.nmin):
            S = array([[2 * abs(-self.prp[2]) / (abs(self.umax - self.umin) * (-self.prp[2] + self.nmax)),
              0,
              0,
              0],
             [0,
              2 * abs(-self.prp[2]) / (abs(self.vmax - self.vmin) * (-self.prp[2] + self.nmax)),
              0,
              0],
             [0,
              0,
              1 / (-self.prp[2] + self.nmax),
              0],
             [0,
              0,
              0,
              1]])
            zmin = (-self.prp[2] + self.nmin) / (-self.prp[2] + self.nmax)
        else:
            S = array([[2 * abs(-self.prp[2]) / (abs(self.umax - self.umin) * (-self.prp[2] + self.nmin)),
              0,
              0,
              0],
             [0,
              2 * abs(-self.prp[2]) / (abs(self.vmax - self.vmin) * (-self.prp[2] + self.nmin)),
              0,
              0],
             [0,
              0,
              1 / (-self.prp[2] + self.nmin),
              0],
             [0,
              0,
              0,
              1]])
            zmin = (-self.prp[2] + self.nmax) / (-self.prp[2] + self.nmin)
        C = S.dot(Sh.dot(T2.dot(Rz.dot(Ry.dot(Rx.dot(T1))))))
        return (C, zmin)

    def window2viewport_parallel(self, p):
        x = int(p[0] * (self.viewportRight - self.viewportLeft) + self.viewportLeft)
        y = int(self.viewportBottom - p[1] * (self.viewportBottom - self.viewportTop))
        return [x, y]

    def window2viewport_perspective(self, p):
        x = int((1 + p[0]) * ((self.viewportRight - self.viewportLeft) / 2) + self.viewportLeft)
        y = int(self.viewportBottom - (1 + p[1]) * ((self.viewportBottom - self.viewportTop) / 2))
        return [x, y]

    def take_picture(self):
        self.viewportLeft = int(self.xmin * (int(self.canvas.cget('width')) - 4))
        self.viewportTop = int(self.ymin * (int(self.canvas.cget('height')) - 4))
        self.viewportRight = int(self.xmax * (int(self.canvas.cget('width')) - 4))
        self.viewportBottom = int(self.ymax * (int(self.canvas.cget('height')) - 4))
        if self.viewport:
            self.canvas.coords(self.viewport, self.viewportLeft, self.viewportTop, self.viewportRight, self.viewportBottom)
            self.canvas.coords(self.text, self.viewportLeft, self.viewportTop)
            self.canvas.coords(self.temp_text, self.viewportRight, self.viewportTop)
            self.canvas.tag_bind(self.viewport, '<ButtonPress-1>', self.left_mouse_click_callback)
            self.canvas.tag_bind(self.viewport, '<ButtonRelease-1>', self.left_mouse_release_callback)
            self.canvas.tag_bind(self.viewport, '<B1-Motion>', self.left_mouse_down_motion_callback)
            self.canvas.tag_bind(self.viewport, '<ButtonPress-3>', self.right_mouse_click_callback)
            self.canvas.tag_bind(self.viewport, '<ButtonRelease-3>', self.right_mouse_release_callback)
            self.canvas.tag_bind(self.viewport, '<B3-Motion>', self.right_mouse_down_motion_callback)
        else:
            self.viewport = self.canvas.create_rectangle(self.viewportLeft, self.viewportTop, self.viewportRight, self.viewportBottom, fill='white')
            self.text = self.canvas.create_text(self.viewportLeft, self.viewportTop, text=self.camera_name, anchor=NW)
            self.temp_text = self.canvas.create_text(self.viewportRight, self.viewportTop, text='', anchor=NE)
        if self.world.new_objects_are_loaded_flag:
            if len(self.line_handles):
                for k in range(0, len(self.line_handles)):
                    self.canvas.delete(self.line_handles[k])

                self.line_handles = []
            for k in range(0, self.world.number_of_edges):
                self.line_handles.append(self.canvas.create_line(0, 0, 0, 0, state='disabled'))
                self.canvas.tag_bind(self.line_handles[-1], '<ButtonPress-1>', self.left_mouse_click_callback)
                self.canvas.tag_bind(self.line_handles[-1], '<ButtonRelease-1>', self.left_mouse_release_callback)
                self.canvas.tag_bind(self.line_handles[-1], '<B1-Motion>', self.left_mouse_down_motion_callback)
                self.canvas.tag_bind(self.line_handles[-1], '<ButtonPress-3>', self.right_mouse_click_callback)
                self.canvas.tag_bind(self.line_handles[-1], '<ButtonRelease-3>', self.right_mouse_release_callback)
                self.canvas.tag_bind(self.line_handles[-1], '<B3-Motion>', self.right_mouse_down_motion_callback)

        if self.projection_type == 'perspective':
            C, zmin = self.composite_perspective()
            if zmin <= 0:
                print('zmin is less than or equal to zero.  zmin=', zmin)
                return
        else:
            C = self.composite_parallel()
        for item in self.world.objects:
            edge_number = -1
            Faces = item.faces.transpose()
            Vertices = item.vertices.transpose()
            for face in Faces:
                for Vertice_idx in range(0, len(face)):
                    v0 = C.dot(Vertices[face[Vertice_idx]])
                    if Vertice_idx == len(face) - 1:
                        v1 = C.dot(Vertices[face[0]])
                    else:
                        v1 = C.dot(Vertices[face[Vertice_idx + 1]])
                    edge_number = edge_number + 1
                    if self.projection_type == 'perspective':
                        points = clip_perspective(v0, v1, zmin)
                        if points:
                            A = self.window2viewport_perspective([points[0][0] / points[0][2], points[0][1] / points[0][2]])
                            B = self.window2viewport_perspective([points[1][0] / points[1][2], points[1][1] / points[1][2]])
                            self.canvas.coords(self.line_handles[edge_number], A[0], A[1], B[0], B[1])
                            self.canvas.itemconfigure(self.line_handles[edge_number], state='normal')
                        else:
                            self.canvas.itemconfigure(self.line_handles[edge_number], state='hidden')
                    else:
                        points = clip_parallel(v0, v1)
                        if points:
                            A = self.window2viewport_parallel(points[0][:-1])
                            B = self.window2viewport_parallel(points[1][:-1])
                            self.canvas.coords(self.line_handles[edge_number], A[0], A[1], B[0], B[1])
                            self.canvas.itemconfigure(self.line_handles[edge_number], state='normal')
                        else:
                            self.canvas.itemconfigure(self.line_handles[edge_number], state='hidden')

        self.canvas.update_idletasks()

    def left_mouse_click_callback(self, event):
        self.canvas.itemconfigure(self.viewport, fill='#0f0')
        self.canvas.itemconfigure(self.temp_text, text='Move VRP')
        self.x = event.x
        self.y = event.y

    def left_mouse_release_callback(self, event):
        self.x = None
        self.y = None
        self.canvas.itemconfigure(self.viewport, fill='white')
        self.canvas.itemconfigure(self.temp_text, text='')

    def left_mouse_down_motion_callback(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.vrp[0] = self.vrp[0] + deltax * 0.01 * self.u_axis[0]
        self.vrp[1] = self.vrp[1] + deltax * 0.01 * self.u_axis[1]
        self.vrp[2] = self.vrp[2] + deltax * 0.01 * self.u_axis[2]
        self.vrp[0] = self.vrp[0] + deltay * 0.01 * self.vup[0]
        self.vrp[1] = self.vrp[1] + deltay * 0.01 * self.vup[1]
        self.vrp[2] = self.vrp[2] + deltay * 0.01 * self.vup[2]
        self.x = event.x
        self.y = event.y
        self.take_picture()

    def right_mouse_click_callback(self, event):
        self.canvas.itemconfigure(self.viewport, fill='#0ff')
        self.canvas.itemconfigure(self.temp_text, text='Change PRPz')
        self.x = event.x
        self.y = event.y

    def right_mouse_release_callback(self, event):
        self.x = None
        self.canvas.itemconfigure(self.viewport, fill='white')
        self.canvas.itemconfigure(self.temp_text, text='')

    def right_mouse_down_motion_callback(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.prp[2] = self.prp[2] - deltay * 0.01
        self.x = event.x
        self.y = event.y
        self.take_picture()


def clip_parallel(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]
    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]
    RIGHT = 32
    LEFT = 16
    TOP = 8
    BOTTOM = 4
    FAR = 2
    NEAR = 1
    input_point_1_outcode = assign_parallel_outcode(x1, y1, z1)
    input_point_2_outcode = assign_parallel_outcode(x2, y2, z2)
    while 1:
        if input_point_1_outcode & input_point_2_outcode:
            return []
        if not input_point_1_outcode | input_point_2_outcode:
            return [[x1, y1, z1], [x2, y2, z2]]
        if input_point_1_outcode:
            outcode = input_point_1_outcode
        else:
            outcode = input_point_2_outcode
        if outcode & RIGHT:
            x = 1
            y = (y2 - y1) * (1 - x1) / (x2 - x1) + y1
            z = (z2 - z1) * (1 - x1) / (x2 - x1) + z1
        elif outcode & LEFT:
            x = 0
            y = (y2 - y1) * -x1 / (x2 - x1) + y1
            z = (z2 - z1) * -x1 / (x2 - x1) + z1
        elif outcode & TOP:
            x = (x2 - x1) * (1 - y1) / (y2 - y1) + x1
            y = 1
            z = (z2 - z1) * (1 - y1) / (y2 - y1) + z1
        elif outcode & BOTTOM:
            x = (x2 - x1) * -y1 / (y2 - y1) + x1
            y = 0
            z = (z2 - z1) * -y1 / (y2 - y1) + z1
        elif outcode & FAR:
            x = (x2 - x1) * (1 - z1) / (z2 - z1) + x1
            y = (y2 - y1) * (1 - z1) / (z2 - z1) + y1
            z = 1
        if outcode & NEAR:
            x = (x2 - x1) * -z1 / (z2 - z1) + x1
            y = (y2 - y1) * -z1 / (z2 - z1) + y1
            z = 0
        if outcode == input_point_1_outcode:
            x1 = x
            y1 = y
            z1 = z
            input_point_1_outcode = assign_parallel_outcode(x1, y1, z1)
        else:
            x2 = x
            y2 = y
            z2 = z
            input_point_2_outcode = assign_parallel_outcode(x2, y2, z2)


def clip_perspective(p1, p2, zmin):
    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]
    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]
    RIGHT = 32
    LEFT = 16
    TOP = 8
    BOTTOM = 4
    FAR = 2
    NEAR = 1
    input_point_1_outcode = assign_perspective_outcode(x1, y1, z1, zmin)
    input_point_2_outcode = assign_perspective_outcode(x2, y2, z2, zmin)
    while 1:
        if input_point_1_outcode & input_point_2_outcode:
            return []
        if not input_point_1_outcode | input_point_2_outcode:
            return [[x1, y1, z1], [x2, y2, z2]]
        if input_point_1_outcode:
            outcode = input_point_1_outcode
        else:
            outcode = input_point_2_outcode
        if outcode & RIGHT:
            x = x1 + (x2 - x1) * (z1 - x1) / (x2 - x1 - (z2 - z1))
            y = y1 + (y2 - y1) * (z1 - x1) / (x2 - x1 - (z2 - z1))
            z = x
        elif outcode & LEFT:
            x = x1 + (x2 - x1) * (-z1 - x1) / (x2 - x1 + (z2 - z1))
            y = y1 + (y2 - y1) * (-z1 - x1) / (x2 - x1 + (z2 - z1))
            z = -x
        elif outcode & TOP:
            x = x1 + (x2 - x1) * (z1 - y1) / (y2 - y1 - (z2 - z1))
            y = y1 + (y2 - y1) * (z1 - y1) / (y2 - y1 - (z2 - z1))
            z = y
        elif outcode & BOTTOM:
            x = x1 + (x2 - x1) * (-z1 - y1) / (y2 - y1 + (z2 - z1))
            y = y1 + (y2 - y1) * (-z1 - y1) / (y2 - y1 + (z2 - z1))
            z = -y
        elif outcode & FAR:
            x = (x2 - x1) * (1 - z1) / (z2 - z1) + x1
            y = (y2 - y1) * (1 - z1) / (z2 - z1) + y1
            z = 1
        if outcode & NEAR:
            x = x1 + (x2 - x1) * (zmin - z1) / (z2 - z1)
            y = y1 + (y2 - y1) * (zmin - z1) / (z2 - z1)
            z = zmin
        if outcode == input_point_1_outcode:
            x1 = x
            y1 = y
            z1 = z
            input_point_1_outcode = assign_perspective_outcode(x1, y1, z1, zmin)
        else:
            x2 = x
            y2 = y
            z2 = z
            input_point_2_outcode = assign_perspective_outcode(x2, y2, z2, zmin)


def assign_parallel_outcode(x, y, z):
    outcode = 0
    if x > 1:
        outcode = 32
    if x < 0:
        outcode = 16
    if y > 1:
        outcode = outcode | 8
    else:
        if y < 0:
            outcode = outcode | 4
        if z > 1:
            outcode = outcode | 2
    if z < 0:
        outcode = outcode | 1
    return outcode


def assign_perspective_outcode(x, y, z, zmin):
    outcode = 0
    if x > z:
        outcode = 32
    if x < -z:
        outcode = 16
    if y > z:
        outcode = outcode | 8
    else:
        if y < -z:
            outcode = outcode | 4
        if z > 1:
            outcode = outcode | 2
    if z < zmin:
        outcode = outcode | 1
    return outcode


class cl_object_2D:

    def __init__(self, vertices, faces):
        self.dimension = 2
        self.vertices = vertices
        self.faces = faces


class cl_object_3D:

    def __init__(self, vertices=[], faces=[]):
        self.vertices = vertices
        self.faces = faces

    def rotate_around_axis(self, angle_d, axis):
        angle_r = angle_d * math.pi / 180
        if axis.lower() == 'z':
            R = array([[cos(angle_r),
              -sin(angle_r),
              0,
              0],
             [sin(angle_r),
              cos(angle_r),
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        if axis.lower() == 'x':
            R = array([[1,
              0,
              0,
              0],
             [0,
              cos(angle_r),
              -sin(angle_r),
              0],
             [0,
              sin(angle_r),
              cos(angle_r),
              0],
             [0,
              0,
              0,
              1]])
        else:
            if axis.lower() == 'y':
                R = array([[cos(angle_r),
                  0,
                  sin(angle_r),
                  0],
                 [0,
                  1,
                  0,
                  0],
                 [-sin(angle_r),
                  0,
                  cos(angle_r),
                  0],
                 [0,
                  0,
                  0,
                  1]])
            else:
                print("Rotation axis must be 'x', 'y' or 'z'")
            self.vertices = R.dot(self.vertices)
        return self

    def rotate_around_line(self, angle_d, A, B):
        angle_r = angle_d * math.pi / 180
        T = array([[1,
          0,
          0,
          -float(A[0])],
         [0,
          1,
          0,
          -float(A[1])],
         [0,
          0,
          1,
          -float(A[2])],
         [0,
          0,
          0,
          1]])
        B = array([[float(B[0])],
         [float(B[1])],
         [float(B[2])],
         [1]])
        (a), (b), (c), (d) = T.dot(B)
        temp_denom = sqrt(b * b + c * c)
        if temp_denom == 0:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Rx = array([[1,
              0,
              0,
              0],
             [0,
              c / temp_denom,
              -b / temp_denom,
              0],
             [0,
              b / temp_denom,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        (a), (b), (c), (d) = Rx.dot([[a],
         [b],
         [c],
         [d]])
        temp_denom = sqrt(a * a + c * c)
        if temp_denom == 0:
            Ry = array([[1,
              0,
              0,
              0],
             [0,
              1,
              0,
              0],
             [0,
              0,
              1,
              0],
             [0,
              0,
              0,
              1]])
        else:
            Ry = array([[c / temp_denom,
              0,
              -a / temp_denom,
              0],
             [0,
              1,
              0,
              0],
             [a / temp_denom,
              0,
              c / temp_denom,
              0],
             [0,
              0,
              0,
              1]])
        (a), (b), (c), (d) = Ry.dot([[a],
         [b],
         [c],
         [d]])
        Rz = array([[cos(angle_r),
          -sin(angle_r),
          0,
          0],
         [sin(angle_r),
          cos(angle_r),
          0,
          0],
         [0,
          0,
          1,
          0],
         [0,
          0,
          0,
          1]])
        T_inv = array([[1,
          0,
          0,
          float(A[0])],
         [0,
          1,
          0,
          float(A[1])],
         [0,
          0,
          1,
          float(A[2])],
         [0,
          0,
          0,
          1]])
        Rx_T = Rx.transpose()
        Ry_T = Ry.transpose()
        M = T_inv.dot(Rx_T.dot(Ry_T.dot(Rz.dot(Ry.dot(Rx.dot(T))))))
        self.vertices = M.dot(self.vertices)

    def scale_around_a_point(self, Sx, Sy, Sz, P):
        T = array([[1,
          0,
          0,
          -float(P[0])],
         [0,
          1,
          0,
          -float(P[1])],
         [0,
          0,
          1,
          -float(P[2])],
         [0,
          0,
          0,
          1]])
        T_inv = array([[1,
          0,
          0,
          float(P[0])],
         [0,
          1,
          0,
          float(P[1])],
         [0,
          0,
          1,
          float(P[2])],
         [0,
          0,
          0,
          1]])
        S = array([[Sx,
          0,
          0,
          0],
         [0,
          Sy,
          0,
          0],
         [0,
          0,
          Sz,
          0],
         [0,
          0,
          0,
          1]])
        M = T_inv.dot(S.dot(T))
        self.vertices = M.dot(self.vertices)
        return self

    def translate(self, Dx, Dy, Dz):
        D = array([[1,
          0,
          0,
          Dx],
         [0,
          1,
          0,
          Dy],
         [0,
          0,
          1,
          Dz],
         [0,
          0,
          0,
          1]])
        self.vertices = D.dot(self.vertices)
        return self

    def composite(self, M):
        self.vertices = M.dot(self.vertices)
        return self

