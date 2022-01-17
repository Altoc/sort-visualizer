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
        self.master.title("Sort Algorithm Visualizer")

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
            return True
        return False

    def changeColor(self, argColorStr):
        # change an object's fill color
        self.canvas.itemconfig(self.myShape, fill=argColorStr)

    def swap(self, visualToSwap, argRoot):
        # swap the graphical representations
        tempX = visualToSwap.targetX
        tempY = visualToSwap.targetY
        visualToSwap.setMoveTarget(self.targetX, self.targetY)
        self.setMoveTarget(tempX, tempY)
        # swap the values
        while not visualToSwap.move() and not self.move():
            argRoot.update()


def scrambleElements(arr, argRoot):
    idx = 0
    for i in range(len(arr)):
        idx = random.randint(1, len(arr) - 1)
        arr[i][2].swap(arr[idx][2], argRoot)
        arr[i], arr[idx] = arr[idx], arr[i]


def selectionSort(arr, argRoot):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx][1] > arr[j][1]:
                min_idx = j
        arr[i][2].swap(arr[min_idx][2], argRoot)
        # swap the smallest value to the beginning of the array, and put the bigger value where the smaller was at
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return True


def bubbleSort(arr, argRoot):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(len(arr) - 1):
            if arr[i][1] > arr[i + 1][1]:
                sorted = False
                # swap the values
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                arr[i][2].swap(arr[i + 1][2], argRoot)
    return sorted


def recursiveInsertionSort(arr, n, argRoot):
    if n <= 1:
        return
    recursiveInsertionSort(arr, n - 1, argRoot)
    j = n - 2
    last = arr[n - 1]
    while j >= 0 and arr[j][1] > last[1]:
        arr[j][2].swap(last[2], argRoot)
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = last


# low is the first index
# high is the last index
def quickSort(arr, low, high, argRoot):
    if low < high:
        pivot = partition(arr, low, high, argRoot)
        # sort to the left of the pivot
        quickSort(arr, low, pivot - 1, argRoot)
        # sort to the right of the pivot
        quickSort(arr, pivot + 1, high, argRoot)


def partition(arr, low, high, argRoot):
    # pivot is the element to the furthest right
    pivot = arr[high]
    pivot[2].changeColor("green")
    # i is the index of the smaller element and indicates the right position of pivot found so far
    i = (low - 1)
    for j in range(low, high):
        # if the current element is smaller than the pivot
        if arr[j][1] < pivot[1]:
            i += 1
            arr[j][2].swap(arr[i][2], argRoot)
            arr[j], arr[i] = arr[i], arr[j]
    arr[i + 1][2].swap(arr[high][2], argRoot)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


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
    # pack label
    labelStr = tkinter.StringVar()
    label = tkinter.Label(root, textvariable=labelStr)
    labelStr.set("Press 'E' to begin.")
    label.pack()
    # pack canvas
    canvas = Canvas(root, bg="Cyan")
    canvas.pack(fill=BOTH, expand=True)
    elements = []
    # Debug array of elements
    # values = [10, 70, 30, 50, 90, 20, 80, 40, 60,  100]
    values = []
    for i in range(0, 80):
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
            labelStr.set("Recursive Insertion Sort")
            recursiveInsertionSort(elements, len(elements), root)
            labelStr.set("Scrambling Array...")
            scrambleElements(elements, root)
            labelStr.set("Bubble Sort")
            bubbleSort(elements, root)
            labelStr.set("Scrambling Array...")
            scrambleElements(elements, root)
            labelStr.set("Selection Sort")
            selectionSort(elements, root)
            labelStr.set("Scrambling Array...")
            scrambleElements(elements, root)
            labelStr.set("Quick Sort")
            quickSort(elements, 0, len(elements) - 1, root)
            labelStr.set("Scrambling Array...")
            scrambleElements(elements, root)
            labelStr.set("Press 'E' to begin.")
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
