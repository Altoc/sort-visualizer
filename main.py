import os
import logging
import keyboard
import numpy as np
import tkinter
from tkinter import Canvas, Frame, BOTH


# of course there is a create_rectangle function in tkinter
# and of course it doesnt come up in google if you search for squares...
class VisualElement(Frame):
    myShape = 0
    canvas = 0
    # movement variables
    posX = 0
    posY = 0
    relW = 0
    relH = 0
    targetX = 0
    targetY = 0
    speed = 0.01

    def __init__(self, argCanvas):
        super().__init__()
        self.myShape
        self.canvas = argCanvas
        self.initUI(self.canvas)

    def initUI(self, canvas):
        self.master.title("Square")
        self.pack(fill=BOTH, expand=1)

    def setShape(self, x, y, w, h, fillColor, outlineColor):
        self.posX = x
        self.posY = y
        self.relW = w
        self.relH = h
        self.targetX = self.posX
        self.targetY = self.posY
        self.myShape = self.canvas.create_rectangle(self.posX, self.posY, self.posX + self.relW, self.posY + self.relH, fill=fillColor, outline=outlineColor)
        self.canvas.pack(fill=BOTH, expand=1)

    def setMoveTarget(self, argX, argY):
        self.targetX = argX
        self.targetY = argY

    def move(self):
        interpolationX = self.posX + (self.targetX - self.posX) * self.speed
        interpolationY = self.posY + (self.targetY - self.posY) * self.speed
        self.posX = interpolationX
        self.posY = interpolationY
        w = self.posX + self.relW
        h = self.posY + self.relH
        logging.debug("Interpolation: " + str(self.posX) + ", " + str(self.posY))
        self.canvas.coords(self.myShape, self.posX, self.posY, w, h)

    def animate(self):
        return
        # move an object
        # change an object's fill color
        # self.canvas.itemconfig(self.myShape, fill="green")


def main():
    # "globals"
    animatedObjects = []
    # set up logging info
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting Application")
    root = tkinter.Tk()
    # root.geometry("1040x720+300+300")
    root.attributes("-fullscreen", True)
    logging.info("Adding widgets")
    canvas = Canvas(root)
    #Debug array of elements
    elements = []
    values = [50, 14, 58, 26, 84, 26, 95, 16, 37, 46]
    xPos = 100
    yPos = 250
    for i in range(values.__len__()):
        newElement = (i, values[i], VisualElement(canvas))
        newElement[2].setShape(xPos, yPos, 10, newElement[1] * -1, "blue", "black")
        elements.append(newElement)
        xPos += 12
        animatedObjects.append(elements[i][2])
    canvas.pack(fill=BOTH, expand=1)
    exitApplication = False
    #process loop
    while not exitApplication:
        # process input
        if keyboard.is_pressed("esc"):
            exitApplication = True
        if keyboard.is_pressed("e"):
            for obj in animatedObjects:
                obj.setMoveTarget(1000, 200)
        # process movement
        for obj in animatedObjects:
            obj.move()
        # process animations
        for obj in animatedObjects:
            obj.animate()
        # update window
        root.update()
    logging.info("Application exiting")


if __name__ == '__main__':
    main()
