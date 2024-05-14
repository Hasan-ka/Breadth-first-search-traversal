import directory.Bestpath as Bestpath
from tkinter import Tk, Canvas, Label, Button
import time

#this array is used to store every dot drawn on "drawing_board" so we could delete every individual drawn dot when we use "resetbtn"
dots = []

#used for knowing current step also used by "drawing_color" to determine what color should be used
current_step = 0

#cube == dot size also used to know rows and colu //// row-colu = cube / width-height
cubes = 10

#this make sure green and red point isn't placed twice used by draw_dot(event) and define_point(color,x,y)
point_placed = False




def create_win(Width,Height,Title):
    """
    return: Window
    """
    window = Tk()
    window.geometry(str(Width) + "x" + str(Height))
    window.minsize(Width,Height)
    window.maxsize(Width,Height)
    window.title(Title)

    return window

def create_tools(window):
    """
    return: example -> buttons, lables, canvas
    """
    global drawing_board
    global statuslbl
    global nextbtn
    global resetbtn
    
    drawing_board = Canvas(window, width=400, height=400, bg="white")
    statuslbl = Label(text="Draw Walls", width=400, height=2,font=("Rubik", 20, "bold"))
    nextbtn = Button(text="Next", width=400, height=2,font=("Rubik", 18, ""))
    resetbtn = Button(text="Clear", width=400, height=2,font=("Rubik", 18, ""))

    return drawing_board, statuslbl, nextbtn, resetbtn

def place_tools(tools):
    """place tools in order.
    for T in (create_tools):
    
    T.pack()"""
    tools_array = tools
    for T in (tools_array):
        T.pack()        
    pass




def drawing_color(current_pos):
    """what dot color should be drawn /// white is just place holder SHOULDN'T be drawn
    param: current_step
    return: color"""
    dire_color = {
        0 : "black",
        1 : "green",
        2 : "red",
        3 : "white"
    }
    return str(dire_color[current_pos])

def drawable(did_it,color):
    """this make sure that only black dot should be drawn multiple times /// if color == white means no drawing
    param: did_it_drawn, color
    return: bool(able)"""
    if color == "black":
        able = True
    elif color == "white":
        able = False
    elif not bool(did_it):
        able = True
    else:
        able = False
    return able

def is_point_placed(did_it):
    """make sure green & red points isn't placed twice used by draw_dot(event) and define_point(color,x,y)"""
    global point_placed
    point_placed = bool(did_it)
    pass

def what_current_step(number):
    """
    0 == drawing walls,
    1 == draw starting point dot,
    2 == draw destination point dot,
    3 == finish (do nothing),
    """
    global current_step
    current_step = int(number)
    pass

def define_point(color,x,y):
    """define starting & destination point and make sure either of points isn't placed twice this also input black dot to walls(allowed) array

    if color == green
        Starting_point, is_point_placed
    elif color == red
        Destination_point, is_point_placed
    else:
        input_allowed_array(black)"""
    global Starting_point
    global Destination_point
    if color == "green":
        Starting_point = int(x/cubes),int(y/cubes)
        is_point_placed(False)
    elif color == "red":
        Destination_point = int(x/cubes),int(y/cubes)
        is_point_placed(False)
        Bestpath.input_allowed_array(x,y,cubes,False)
    else:
        Bestpath.input_allowed_array(x,y,cubes,True)




#this let the user draw in the GUI that the going to avoid
def draw_wall(event):
    """this draw walls should only black use it so if current_step != 0 (wall step) it shouldn't work"""
    mx = event.x
    my = event.y

    for i in range(0, 400, cubes):
        for u in range(0, 400, cubes):
            if i <= mx and (i + cubes) > mx and u <= my and (u + cubes) > my and current_step == 0:
                dots.append(drawing_board.create_rectangle((i,u,i+cubes,u+cubes), fill="black"))
                Bestpath.input_allowed_array(i,u,cubes,True)

#this draw and make sure that green and red dots only drawn once the rule exlude black dot could be drawn multiple times
def draw_dot(event):
    mx = event.x
    my = event.y

    color = drawing_color(current_step)
    placeable = drawable(point_placed,color)

    for i in range(0, 400, cubes):
        for u in range(0, 400, cubes):
            if i <= mx and (i + cubes) > mx and u <= my and (u + cubes) > my and placeable:
                dots.append(drawing_board.create_rectangle((i,u,i+cubes,u+cubes), fill=color, outline=color))
                define_point(color,i,u)
                is_point_placed(True)

def drawing_visited(x,y):
    """draw visited links"""
    for i in range(0, 400, cubes):
            for u in range(0, 400, cubes):
                if i == (x * 10) and u == (y * 10) and Destination_point != (x,y):
                    time.sleep(0.001)
                    dots.append(drawing_board.create_rectangle((i,u,i+cubes,u+cubes), fill="grey81", outline="grey81"))
                    drawing_board.update_idletasks()

def bp_drawing(bp_stack):
    """draw blue line from start to finish (best path) from best_path_stack you got from (best_path) function"""
    stack_size = bp_stack.qsize()
    bp_stack.get()
    while bp_stack.qsize() > 1:
        curr_stack = bp_stack.get()
        for i in range(0, 400, cubes):
            for u in range(0, 400, cubes):
                if i == (curr_stack[0] * 10) and u == (curr_stack[1] * 10):
                    time.sleep(0.008)
                    dots.append(drawing_board.create_rectangle((i,u,i+cubes,u+cubes), fill="blue", outline="blue"))
                    drawing_board.update_idletasks()
    return stack_size




def result(stack_size):
    """
    if true 
        lable = completed
    if false
        lable = unreachable
    """
    if stack_size > 1:
        statuslbl.config(text="Completed", fg="green")
    else:
        statuslbl.config(text="Unreachable", fg="red")




#Clear button               
def reset(event):
    for dot in dots:
        drawing_board.delete(dot)
    dots.clear()

    Bestpath.clear_allowed_array()

    statuslbl.config(text="Draw Walls", fg="black")
    nextbtn.config(text="Next")

    is_point_placed(False)
    what_current_step(0)

#Next button
def Next(event):
    if current_step == 0:
        statuslbl.config(text="Set Starting Point")
        is_point_placed(False)
        what_current_step(1)
    elif current_step == 1 and point_placed == True:
        statuslbl.config(text="Set Ending Point")
        nextbtn.config(text="Start Traversing")
        is_point_placed(False)
        what_current_step(2)
    elif current_step == 2 and point_placed == True:
        statuslbl.config(text="Traversing...")
        best_path_stack = Bestpath.best_path(Destination_point[0],Destination_point[1],Starting_point[0],Starting_point[1])
        stack_size = bp_drawing(best_path_stack)
        result(stack_size)
        what_current_step(3)

