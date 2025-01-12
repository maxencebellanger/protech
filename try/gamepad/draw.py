import turtle
import random
import keyboard
import usb.core
import usb.util
import time 


colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink"]

def interpret_angles(valueX, valueY):
    if valueX>127:
        valueX = ((valueX - 128)/127) - 1 
    elif valueX == 0:
        pass
    else:
        valueX = 1 - (127-valueX)/127

    if valueY>127:
        valueY = ((valueY - 128)/127) - 1 
    elif valueY == 0:
        pass
    else:
        valueY = 1 - (127 - valueY)/127

    return(valueX, valueY)

def drawturtle(dev, endpoint):
    # Setup the screen
    screen = turtle.Screen()
    screen.bgcolor("white")

    spiral = turtle.Turtle()
    spiral.speed(0)
    spiral.width(2)
    
    spiral.isdown()
    spiral.color("black")
    screen.bgcolor("white")
    
    Button_Status = False
    
    def move_forward():
        spiral.forward(10)

    def switch():
    	if not Button_Status:
            if spiral.isdown():
                spiral.penup() 
            else:
                spiral.pendown()  
    while True:
        raw_data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        data = raw_data[10:14]
        direction_x, direction_y = interpret_angles(data[1],data[3])
        boutons = bin(raw_data[3]+ 256)
        Moving = False
        if boutons[5] == '1':
            break
        if boutons[6] == '1':
            switch()
            Button_Status = True
        if boutons[6] == '0':
            Button_Status = False
        if boutons[8] == '1':
            screen.clear()
            spiral = turtle.Turtle()
            spiral.speed(0)
            spiral.width(2)
    
            spiral.isdown()
            spiral.color("black")
            screen.bgcolor("white")
        if boutons[9] == '1':
            spiral.color("black")
        if boutons[10] == '1':
            spiral.color("red")
        if abs(direction_x) + abs(direction_y) > 0:
            Moving = True
        # Set the turtle heading based on direction vector
        if direction_x != 0 or direction_y != 0:
            angle = turtle.towards(direction_x, direction_y)
            spiral.setheading(angle)
        if Moving:
            move_forward()
