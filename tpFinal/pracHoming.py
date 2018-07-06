
# Updated Animation Starter Code

from tkinter import *

####################################
# customize these functions
####################################

lst = [2,3,4,5]
lst[]
def formula(x1,x2,x3,t):
    return ((1-t)**2)*x1 + 2*(1-t)*(t)*x2+ (t**2)*x3
   
def createCurve(x3,y3,t=0):
    if t == 110:
        return []

    else:
        x2 = 700 +(x3-700)//2
        y2 = 360-(y3-100)//2

        x = int(formula(700,x2,x3,t/100))
        y = int(formula(360,y2,y3,t/100))
        

        return [[x,y]] + createCurve(x3,y3,t+5)

def init(data):
    data.points = None
    data.i = 0
   

def mousePressed(event, data):
    data.points = createCurve(900,360)
    data.i+= 1
    if data.i == len(data.points):
        data.i = 0
    

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    canvas.create_line(0,360,data.width,360)

    if data.points != None:
        for p in data.points:
            canvas.create_text(p[0],p[1] ,text = "A")
        canvas.create_oval(data.points[data.i][0]-5,data.points[data.i][1]-5,data.points[data.i][0]+5,data.points[data.i][1]+5, fill = "blue")

####################################
# use the run function as-is
####################################

def run(width=800, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200, 500)