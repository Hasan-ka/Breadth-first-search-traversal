import directory.GUI as GUI
from tkinter import mainloop




def main():
    #this create and place the window and tools used
    window = GUI.create_win(400,600,"Breadth First Search + Best Path")
    tool = GUI.create_tools(window)
    GUI.place_tools(tool)

    #buttons Next and Clear
    GUI.nextbtn.bind("<Button-1>", GUI.Next)
    GUI.resetbtn.bind("<Button-1>", GUI.reset)

    #the canvas is used to draw on it so the use define the map of the traversal
    if GUI.current_step != 3:
        GUI.drawing_board.bind('<B1-Motion>', GUI.draw_wall)
        GUI.drawing_board.bind('<Button-1>', GUI.draw_dot)

    mainloop()



main()
    