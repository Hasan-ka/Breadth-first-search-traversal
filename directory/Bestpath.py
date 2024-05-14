import directory.GUI as GUI
import numpy as np 
from queue import Queue, LifoQueue

#just used for simplicity sake
x = 0
y = 1


#it marks a visited space or a wall that the algorithm going to avoid: True = Not allowed - False = allowed
allowed = np.array([[False for k in range(40)] for j in range(40)], dtype=bool)


#used to calculate the rows and columns in the allowed array to configer xyoffset array automaticlly and we are in bound during the running of the algorithm
r , c = len(allowed), len(allowed[0])



#the algorithm would only check straght paths means NO a diagonal path!
def traversal(start_x,start_y):
    """
    This is used for best_path function
    param: start offset of X,Y
    return: offset array to know what offset has been discover by
    """
    xyoffset = [[None for k in range(c)] for j in range(r)]

    #q used to store offset that about to be visited to discover every path
    to_visit = Queue()

    #xyoffset[sy][sx] must be NONE!!!
    to_visit.put((start_x,start_y))
    allowed[start_y][start_x] = True

    while not to_visit.empty():

        visit = to_visit.get()

        discovery_Yaxis(visit,to_visit,xyoffset)

        discovery_Xaxis(visit,to_visit,xyoffset)
      
    return xyoffset

def discovery_Yaxis(vitting,to_be_visitted,offset):
    """
    This function discover the space in a Y axis from top to bottem of an specific offset
    param: vitting = to_be_visitted.get(), to_be_visitted to store offset that about to be visitted, offset is an array to show what offset space been discover by
    """
    for cy in range(-1, 3, 2):
            if (vitting[y] + cy) >= 0 and (vitting[y] + cy) < r and not allowed[vitting[y] + cy][vitting[x]]:

                to_be_visitted.put((vitting[x],vitting[y] + cy))

                offset[vitting[y] + cy][vitting[x]] = (vitting[x],vitting[y])

                allowed[vitting[y] + cy][vitting[x]] = True

                GUI.drawing_visited(vitting[x],vitting[y] + cy)
    pass

def discovery_Xaxis(vitting,to_be_visitted,offset):
    """
    This function discover the space in a X axis from left to right of an specific offset
    param: vitting = to_be_visitted.get(), to_be_visitted to store offset that about to be visitted, offset is an array to show what offset space been discover by
    """
    for cx in range(-1, 3, 2):
            if (vitting[x] + cx) >= 0 and (vitting[x] + cx) < c and not allowed[vitting[y]][vitting[x] + cx]:

                to_be_visitted.put((vitting[x] + cx,vitting[y]))

                offset[vitting[y]][vitting[x] + cx] = (vitting[x],vitting[y])

                allowed[vitting[y]][vitting[x] + cx] = True

                GUI.drawing_visited(vitting[x] + cx,vitting[y])
    pass
           



def best_path(destination_x,destination_y,starting_x,starting_y):
    """
    param: Destination offset of X,Y
    return: stack of the Best Path from the starting offset to destination offset
    """
    xyoffset = traversal(starting_x,starting_y)

    #stack used to store a map best path
    BP = LifoQueue()

    current = [destination_x,destination_y]

    BP.put((current[x],current[y]))

    #None either means the starting point or unreachable \\\ it would be considered unreachable-
    #if the destination point directlly to None in the offset
    while xyoffset[current[y]][current[x]]:

        next = xyoffset[current[y]][current[x]]

        BP.put((next[x],next[y]))

        current = next

    return BP





def input_allowed_array(xAxis,yAxis,dot_size,condition):
     """
     if true -> allowed[y/size][x/size] = true
     
     if false -> allowed[y/size][x/size] = false
     """
     if condition == True:
        allowed[int(yAxis/dot_size)][int(xAxis/dot_size)] = True
     elif condition == False:
        allowed[int(yAxis/dot_size)][int(xAxis/dot_size)] = False
     pass

def clear_allowed_array():
    """
    for y to 40
        for x to 40
            allowedy[y][x] = false
    """
    for y in range(r):
        for x in range(c):
            allowed[y][x] = False
    pass
