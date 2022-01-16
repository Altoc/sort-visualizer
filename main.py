import os
import logging
import keyboard
import time
import math
import random
import tkinter
from tkinter import Canvas, Frame, BOTH


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
    speed = 0.1

    def __init__(self, argCanvas):
        super().__init__()
        self.myShape
        self.canvas = argCanvas
        self.initUI(self.canvas)

    def initUI(self, canvas):
        self.master.title("Visual Element")

    def setShape(self, x, y, w, h, fillColor, outlineColor):
        self.posX = x
        self.posY = y
        self.relW = w
        self.relH = h
        self.targetX = self.posX
        self.targetY = self.posY
        self.myShape = self.canvas.create_rectangle(self.posX, self.posY, self.posX + self.relW, self.posY + self.relH,
                                                    fill=fillColor, outline=outlineColor)

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
        if abs(self.posX - self.targetX) < 0.05 and abs(self.posY - self.targetY) < 0.05:
            self.animate()
            return True
        return False

    def animate(self):
        # change an object's fill color
        self.canvas.itemconfig(self.myShape, fill="green")


def insertSort(arr, argRoot):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx][1] > arr[j][1]:
                min_idx = j
        # swap the graphical representations
        tempX = arr[i][2].targetX
        tempY = arr[i][2].targetY
        arr[i][2].setMoveTarget(arr[min_idx][2].targetX, arr[min_idx][2].targetY)
        arr[min_idx][2].setMoveTarget(tempX, tempY)
        # swap the smallest value to the beginning of the array, and put the bigger value where the smaller was at
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        while not arr[i][2].move() and not arr[min_idx][2].move():
            argRoot.update()
    return "Done"

def main():
    # "globals"
    animatedObjects = []
    # set up logging info
    logging.basicConfig(level=logging.WARNING)
    logging.info("Starting Application")
    root = tkinter.Tk()
    root.geometry("1040x720+400+100")
    # root.attributes("-fullscreen", True)
    logging.info("Adding widgets")
    canvas = Canvas(bg="Cyan")
    canvas.pack(fill=BOTH, expand=True)
    # Debug array of elements
    elements = []
    values = []
    for i in range(0, 89):
        values.append(random.randint(1, 700))
    xPos = 1
    yPos = 720
    for i in range(values.__len__()):
        newElement = (i, values[i], VisualElement(canvas))
        newElement[2].setShape(xPos, yPos, 10, newElement[1] * -1, "blue", "black")
        elements.append(newElement)
        xPos += 12
        animatedObjects.append(elements[i][2])
    exitApplication = False
    # process loop
    while not exitApplication:
        # process input
        if keyboard.is_pressed("esc"):
            exitApplication = True
        if keyboard.is_pressed("e"):
            print(insertSort(elements, root))
        # process movement
        # for obj in animatedObjects:
        # obj.move()
        # obj.animate()
        # process animations
        # for obj in animatedObjects:
        # obj.animate()
        # update window
        root.update_idletasks()
        root.update()
    logging.info("Application exiting")


if __name__ == '__main__':
    main()
