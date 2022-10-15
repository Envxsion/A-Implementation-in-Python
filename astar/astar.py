from string import whitespace
import pygame 
import math
from queue import PriorityQueue

win_width = 1000
win_height = 1000
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("A* Path Finding Algo")

#predefined colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Nodes:
    def __init__(self, row, col, win_width, total_rows):
        self.row = row
        self.col = col
        
        #multiply row and col by width to get the x and y coordinates of the nodes
        self.win_width = win_width
        self.x = row * win_width
        self.y = col * win_width
        self.total_rows = total_rows
        
        self.color = WHITE #default color of the nodes
        self.neighbors = [] #list of neighbors 
    
    def get_pos(self):
        return self.row, self.col
    
    #CHECKS TO RETURN TRUE OR FALSE BASED ON THE COLOR OF THE NODES -----------------------------   
    
    def checked(self): #if the node has been checked by algo, it will be colored red
        return self.color == RED
    
    def available(self): #if the node has not been checked by algo, it will be colored purple 
        return self.color == PURPLE
    
    def barrier(self):  #if the node is a barrier, it will be colored black
        return self.color == BLACK
    
    def start(self): #if the node is the start node, it will be colored orange
        return self.color == ORANGE
    
    def end(self): #if the node is the end node, it will be colored turquoise
        return self.color == TURQUOISE
        
    #ACTUALLY CHANGE THE COLORS -----------------------------------------------------------------   
    
    def set_checked(self): #set the node to checked state
        self.color = RED
    
    def set_available(self): #set the node to available state
        self.color = PURPLE
    
    def set_barrier(self):  #set the node to barrier state
        self.color = BLACK
    
    def set_start(self): #set the node to start state
        self.color = ORANGE
    
    def set_end(self): #set the node to end state
        self.color = TURQUOISE
    
    def set_path(self): #set the node to corrent path color
        self.color = GREEN
    
    def reset(self): #if the node is reset, it will be colored white
        self.color = WHITE
        
    def draw(self, window):
        #pass in window, color, x & y coords of the top left corners of the node, and the width and height of the node
        #remember the top left of the window is 0,0 while the bottom right is your window width and height (1000,1000)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.win_width, self.win_width)) 
        
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier(): #if the node is not the bottom row and the node below it is not a barrier
            self.neighbors.append(grid[self.row + 1][self.col]) #add the node below to the list of neighbors
            
        if self.row > 0 and not grid[self.row - 1][self.col].barrier(): #if the node is not the top row and the node above it is not a barrier
            self.neighbors.append(grid[self.row - 1][self.col]) 
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].barrier(): #if the node is not the right most column and the node to the right is not a barrier
            self.neighbors.append(grid[self.row][self.col+1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].barrier(): #if the node is not the left most column and the node to the left is not a barrier
            self.neighbors.append(grid[self.row][self.col - 1]) 
    
    def __lt__(self, other): #here its taking in a node (self) and another node (other) and saying that the other node is always greater than the self node
        #special method that describes the less-than operator in python
        return False


#heuristic function to calculate the distance between two points. This function uses manhattan distance to return the "L" distance between two points as we can't move diagonally    
def heuristic(p1, p2): 
    #p1 and p2 are tuples of the form (x,y)
    x1, y1 = p1
    x2, y2 = p2 
    
    #manhattan distance
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from: #while the current node is in the came_from dictionary
        current = came_from[current] #set the current node to the node that came before it
        current.set_path() #set the current node to the path color
        draw() 

def algo(draw, grid, start, end):
    count = 0 #count is the number of the node in the order in which it was added. If 2 nodes of the same f score are added, the one with the lower count will be added first
    
    open_set = PriorityQueue() #gets smallest element in the queue
    open_set.put((0, count, start)) #put the start node in the priority queue | put is another way of saying append
    
    #this dictionary will hold the node that came before the current nodes
    came_from = {} 
    
    #this dictionary will hold the g score of each node. The g score is the distance from the start node to the current node.
    g_score = {node: float("inf") for row in grid for node in row}  #float("inf") is a python function that returns infinity
    g_score[start] = 0 #the g score of the start node is 0 because it is the start node
    f_score = {node: float("inf") for row in grid for node in row}  
    f_score[start] = heuristic(start.get_pos(), end.get_pos()) #the f score of the start node is the distance from the start node to the end node (diagonally)
    
    open_set_hash = {start} #this is a set that will hold the nodes that are in the priority queue  
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #make sure you can quit while algo is running
                pygame.quit()
                
        current = open_set.get()[2] #get the node with the lowest f score from the priority queue (index 2 is used as the first index is the f score, the second is the count and the third is the node)
        open_set_hash.remove(current) #sync hash with priority queue
        
        if current == end:
            reconstruct_path(came_from, current, draw)
            start.set_start()
            end.set_end()
            return True
        
        for neighbour in current.neighbors:
            temp_g_score = g_score[current] + 1 #the g score of the neighbor is the g score of the current node + 1
            
            if temp_g_score < g_score[neighbour]: #if the g score of the neighbor is less than the g score of the neighbor
                came_from[neighbour] = current #store the current node 
                g_score[neighbour] = temp_g_score #update the g score of the neighbor
                f_score[neighbour] = temp_g_score + heuristic(neighbour.get_pos(), end.get_pos()) #update the f score of the neighbor
                
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour)) #add the neighbor to the priority queue
                    open_set_hash.add(neighbour) #add the neighbor to the hash
                    neighbour.set_available() #set the neighbor to the open state 
                    
        draw()
        
        if current != start:
            current.set_checked()
            
    return False #didn't find path
                
        
#------------------------------------------------------------------------------
def make_grid (rows, win_width): #this function creates the grid of nodes
    grid = []
    n_width = win_width // rows #this is the width of each node in the grid
    
    for i in range(rows):
        grid.append([]) #this is a 2D array just like the one in numpt
        
        for j in range(rows):
            node = Nodes(i, j, n_width, rows) #pass in the grid row, grid col, width of node, and total rows
            grid[i].append(node)
    
    return grid

def draw_grid_lines(window, rows, win_width): #this function draws the grid lines
    n_width = win_width // rows #this is the width of each node in the grid
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * n_width), (win_width, i * n_width)) #col number * width of node
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * n_width, 0), (j * n_width, win_width)) #col number * width of node
            
def draw(window, grid, rows, win_width): #this function draws everything in the grid
    window.fill(WHITE)
    for row in grid:
        for nodes in row:
            nodes.draw(window)
    
    draw_grid_lines(window, rows, win_width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, win_width): #this function gets the position of the mouse click
    n_width = win_width // rows
    y, x = pos
    
    row = y // n_width
    col = x // n_width
    
    return row, col
#------------------------------------------------------------------------------

def main(window, win_width): 
    rows = 50 #more rows = more cubes = more nodes = more time to run
    grid = make_grid(rows, win_width)
    
    start = None #start node
    end = None #end node
    
    run = True #loop running
    while run:
        draw(window, grid, rows, win_width)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() #get the position of the mouse
            row, col = get_clicked_pos(pos, rows, win_width) #get the row and col of the node that was clicked
            node = grid[row][col] #get the node that was clicked
            
            if event.type == pygame.QUIT:
                run = False #break loop if user clicks the x button
                
            if pygame.mouse.get_pressed()[0]: #left click
                if not start and node != end: #if start is not set
                    start = node
                    start.set_start()
                    
                elif not end and node != start: #if end is not set
                    end = node
                    end.set_end()
                    
                elif node != start and node != end:
                    node.set_barrier()
                    
            if pygame.mouse.get_pressed()[2]: #right click
                node.reset()
                if node == start:
                    start = None #reset start
                elif node == end:
                    end = None #reset end
                    
            if event.type == pygame.KEYDOWN: #if key is pressed
                if event.key == pygame.K_SPACE and start and end: #if space is pressed satrt and end nodes are set
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid) #find neighbors of each node
                            
                    #lambda is a function that is not defined until it is called
                    #draw is in the function "lambda", and this new anonymous function is passed into the algorithm (another function) as its argument
                    algo(lambda: draw(window, grid, rows, win_width), grid, start, end) 
                    
                if event.key == pygame.K_c: #if c is pressed clear everything
                    start = None
                    end = None
                    grid = make_grid(rows, win_width)
    pygame.quit()
main(window, win_width)
