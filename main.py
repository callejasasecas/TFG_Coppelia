# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy

import sim
import time as t
import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from scipy.spatial import distance

gradosJ1 = 0

def connect(port):
    sim.simxFinish(-1)
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID==0:
        print("Conectado a:", port)
    else:
        raise Exception("no se puedo conectar")
    return clientID
# Press the green button in the gutter to run the script.





def close_gripper(clientID):

    retcode, j1 = sim.simxGetObjectHandle(clientID, 'fingers12_motor1_jaco', sim.simx_opmode_blocking)
    retcode, j2 = sim.simxGetObjectHandle(clientID, 'fingers12_motor2_jaco', sim.simx_opmode_blocking)
    retcode, j3 = sim.simxGetObjectHandle(clientID, 'finger3_motor1_jaco', sim.simx_opmode_blocking)
    retcode, j4 = sim.simxGetObjectHandle(clientID, 'finger3_motor2_jaco', sim.simx_opmode_blocking)
    closingVel = -0.04
    sim.simxSetJointTargetVelocity(clientID, j1, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j2, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j3, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j4, closingVel, sim.simx_opmode_blocking)


def open_gripper(clientID):

    retcode, j1 = sim.simxGetObjectHandle(clientID, 'fingers12_motor1_jaco', sim.simx_opmode_blocking)
    retcode, j2 = sim.simxGetObjectHandle(clientID, 'fingers12_motor2_jaco', sim.simx_opmode_blocking)
    retcode, j3 = sim.simxGetObjectHandle(clientID, 'finger3_motor1_jaco', sim.simx_opmode_blocking)
    retcode, j4 = sim.simxGetObjectHandle(clientID, 'finger3_motor2_jaco', sim.simx_opmode_blocking)
    closingVel = 0.04
    sim.simxSetJointTargetVelocity(clientID, j1, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j2, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j3, closingVel, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, j4, closingVel, sim.simx_opmode_blocking)


def subeJ1(clientId,joint1):
    global gradosJ1
    gradosJ1 += 1
    print(gradosJ1)
    sim.simxSetJointTargetPosition(clientID, joint1, math.radians(gradosJ1), sim.simx_opmode_blocking)

def mover(clientId,i,grd):

    print(grd)
    print(i)
    #joint = sim.simxGetObjectHandle(clientID, 'joint'+str(i), sim.simx_opmode_blocking)
    grados = int(grd)
    #sim.simxSetJointTargetPosition(clientID, joint, math.radians(grados), sim.simx_opmode_blocking)
"""
def show_text(index):
    text = text_boxes[index].get()
    grados = int(text)
    #print(f'Texto de la caja {index+1}: {text}')
    jointName = 'joint'+str(index+1)
    print(jointName)
    retcode,joint = sim.simxGetObjectHandle(clientID, str(jointName), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, joint, math.radians(grados), sim.simx_opmode_blocking)
"""

def movimiento(clientID, handle, pos, ori):
    sim.simxSetObjectOrientation(clientID, handle, -1, ori, sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(clientID, handle, -1, pos, sim.simx_opmode_blocking)


def puntoMedio(a,b):
    d=[0,0,0]
    d[0]= (a[0]+b[0])/2
    d[1] = (a[1] + b[1]) / 2
    d[2] = (a[2] + b[2]) / 2
    return d

def grab_grey(clientID,UR5):
    retcode, cilindro = sim.simxGetObjectHandle(clientID, 'cil_dummy', sim.simx_opmode_blocking)
    retcode, cilindroGrab = sim.simxGetObjectHandle(clientID, 'cil_dummy_grab', sim.simx_opmode_blocking)
    retcode, basket = sim.simxGetObjectHandle(clientID, 'basket', sim.simx_opmode_blocking)
    retcode, basketFinal = sim.simxGetObjectHandle(clientID, 'basket_final', sim.simx_opmode_blocking)
    retcode, cilindroObjeto = sim.simxGetObjectHandle(clientID, 'Cylinder_grey', sim.simx_opmode_blocking)

    retcode, ori = sim.simxGetObjectOrientation(clientID, cilindro, -1, sim.simx_opmode_blocking)
    retcode, pos = sim.simxGetObjectPosition(clientID, cilindro, -1, sim.simx_opmode_blocking)

    retcode, oriGrab = sim.simxGetObjectOrientation(clientID, cilindroGrab, -1, sim.simx_opmode_blocking)
    retcode, posGrab = sim.simxGetObjectPosition(clientID, cilindroGrab, -1, sim.simx_opmode_blocking)

    retcode, oriBasket = sim.simxGetObjectOrientation(clientID, basket, -1, sim.simx_opmode_blocking)
    retcode, posBasket = sim.simxGetObjectPosition(clientID, basket, -1, sim.simx_opmode_blocking)

    retcode, oriBasketFinal = sim.simxGetObjectOrientation(clientID, basketFinal, -1, sim.simx_opmode_blocking)
    retcode, posBasketFinal = sim.simxGetObjectPosition(clientID, basketFinal, -1, sim.simx_opmode_blocking)

    movimiento(clientID, UR5, pos, ori)

    t.sleep(1)
    movimiento(clientID, UR5, posGrab, ori)
    t.sleep(0.5)
    close_gripper(clientID)
    t.sleep(1)
    retcode, attachPointJaco = sim.simxGetObjectHandle(clientID, 'attachPointJaco', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto,attachPointJaco,-1,sim.simx_opmode_blocking)

    t.sleep(1)
    movimiento(clientID, UR5, posBasket, oriBasket)

    t.sleep(1)
    movimiento(clientID, UR5, posBasketFinal, oriBasketFinal)
    retcode, table1 = sim.simxGetObjectHandle(clientID, 'table1', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto, table1, 1, sim.simx_opmode_blocking)
    open_gripper(clientID)
    t.sleep(1)
    retcode, target_pos = sim.simxGetObjectPosition(clientID, UR5, -1, sim.simx_opmode_blocking)
    target_pos[0] = target_pos[0] - 0.05
    movimiento(clientID, UR5, target_pos, oriBasket)


def grab_red(clientID, UR5):
    retcode, cilindroRojo = sim.simxGetObjectHandle(clientID, 'red_cil', sim.simx_opmode_blocking)
    retcode, cilindroRojoGrab = sim.simxGetObjectHandle(clientID, 'red_cil_grab', sim.simx_opmode_blocking)
    retcode, apoyo = sim.simxGetObjectHandle(clientID, 'apoyo', sim.simx_opmode_blocking)
    retcode, oriRed = sim.simxGetObjectOrientation(clientID, cilindroRojo, -1, sim.simx_opmode_blocking)
    retcode, posRed = sim.simxGetObjectPosition(clientID, cilindroRojo, -1, sim.simx_opmode_blocking)
    retcode, oriGrabRed = sim.simxGetObjectOrientation(clientID, cilindroRojoGrab, -1, sim.simx_opmode_blocking)
    retcode, posGrabRed = sim.simxGetObjectPosition(clientID, cilindroRojoGrab, -1, sim.simx_opmode_blocking)
    retcode, basketRed = sim.simxGetObjectHandle(clientID, 'basket_red', sim.simx_opmode_blocking)
    retcode, oriBasketRed = sim.simxGetObjectOrientation(clientID, basketRed, -1, sim.simx_opmode_blocking)
    retcode, posBasketRed = sim.simxGetObjectPosition(clientID, basketRed, -1, sim.simx_opmode_blocking)
    retcode, cilindroObjeto = sim.simxGetObjectHandle(clientID, 'Cylinder_red', sim.simx_opmode_blocking)
    retcode, posApoyo = sim.simxGetObjectPosition(clientID, apoyo, -1, sim.simx_opmode_blocking)
    etcode, oriApoyo = sim.simxGetObjectOrientation(clientID, apoyo, -1, sim.simx_opmode_blocking)


    movimiento(clientID, UR5, posRed, oriRed)
    t.sleep(1)
    movimiento(clientID, UR5, posGrabRed, oriGrabRed)
    t.sleep(0.5)
    close_gripper(clientID)
    t.sleep(1)
    retcode, attachPointJaco = sim.simxGetObjectHandle(clientID, 'attachPointJaco', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto, attachPointJaco, -1, sim.simx_opmode_blocking)
    movimiento(clientID, UR5, posApoyo, oriApoyo)
    t.sleep(0.5)
    movimiento(clientID, UR5, posBasketRed, oriBasketRed)
    t.sleep(1)
    retcode, target_pos = sim.simxGetObjectPosition(clientID, UR5, -1, sim.simx_opmode_blocking)
    target_pos[2] = target_pos[2] - 0.05
    movimiento(clientID, UR5, target_pos, oriBasketRed)
    open_gripper(clientID)
    t.sleep(0.5)
    retcode, table1 = sim.simxGetObjectHandle(clientID, 'table1', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto, table1, 1, sim.simx_opmode_blocking)
    t.sleep(1)
    retcode, target_pos = sim.simxGetObjectPosition(clientID, UR5, -1, sim.simx_opmode_blocking)
    target_pos[0] = target_pos[0] - 0.15
    movimiento(clientID, UR5, target_pos, oriBasketRed)




def grab_blue(clientID, UR5):
    retcode, cilindroAzul = sim.simxGetObjectHandle(clientID, 'blue_cil', sim.simx_opmode_blocking)
    retcode, oriBlue = sim.simxGetObjectOrientation(clientID, cilindroAzul, -1, sim.simx_opmode_blocking)
    retcode, posBlue = sim.simxGetObjectPosition(clientID, cilindroAzul, -1, sim.simx_opmode_blocking)
    retcode, basketBlue = sim.simxGetObjectHandle(clientID, 'basket_blue', sim.simx_opmode_blocking)
    retcode, oriBasketBlue = sim.simxGetObjectOrientation(clientID, basketBlue, -1, sim.simx_opmode_blocking)
    retcode, posBasketBlue = sim.simxGetObjectPosition(clientID, basketBlue, -1, sim.simx_opmode_blocking)
    retcode, cilindroObjeto = sim.simxGetObjectHandle(clientID, 'Cylinder_blue', sim.simx_opmode_blocking)

    t.sleep(1)
    movimiento(clientID, UR5, posBlue, oriBlue)
    t.sleep(1)
    retcode, target_pos = sim.simxGetObjectPosition(clientID, UR5, -1, sim.simx_opmode_blocking)
    target_pos[1] = target_pos[1] - 0.180
    movimiento(clientID, UR5, target_pos, oriBlue)
    t.sleep(0.5)
    close_gripper(clientID)
    t.sleep(1)
    retcode, attachPointJaco = sim.simxGetObjectHandle(clientID, 'attachPointJaco', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto, attachPointJaco, -1, sim.simx_opmode_blocking)
    movimiento(clientID, UR5, posBasketBlue, oriBasketBlue)
    t.sleep(1)
    retcode, target_pos = sim.simxGetObjectPosition(clientID, UR5, -1, sim.simx_opmode_blocking)
    target_pos[2] = target_pos[2] - 0.05
    movimiento(clientID, UR5, target_pos, oriBasketBlue)
    t.sleep(1)
    retcode, table1 = sim.simxGetObjectHandle(clientID, 'table1', sim.simx_opmode_blocking)
    sim.simxSetObjectParent(clientID, cilindroObjeto, table1, 1, sim.simx_opmode_blocking)
    open_gripper(clientID)


if __name__ == '__main__':
    try:
        print("Hola")
        clientID = connect(19999)
        retcode, UR5 = sim.simxGetObjectHandle(clientID, 'target', sim.simx_opmode_blocking)
        retcode, cilindro = sim.simxGetObjectHandle(clientID, 'cil_dummy', sim.simx_opmode_blocking)
        retcode, cilindroGrab = sim.simxGetObjectHandle(clientID, 'cil_dummy_grab', sim.simx_opmode_blocking)
        retcode, originalPosition = sim.simxGetObjectHandle(clientID, 'original_position', sim.simx_opmode_blocking)
        retcode, cilindroRojo = sim.simxGetObjectHandle(clientID, 'red_cil', sim.simx_opmode_blocking)
        retcode, cilindroRojoGrab = sim.simxGetObjectHandle(clientID, 'red_cil_grab', sim.simx_opmode_blocking)
        retcode, cilindroAzul = sim.simxGetObjectHandle(clientID, 'blue_cil', sim.simx_opmode_blocking)
        retcode, basket = sim.simxGetObjectHandle(clientID, 'basket', sim.simx_opmode_blocking)
        retcode, basketFinal = sim.simxGetObjectHandle(clientID, 'basket_final', sim.simx_opmode_blocking)
        retcode, basketRed = sim.simxGetObjectHandle(clientID, 'basket_red', sim.simx_opmode_blocking)
        retcode, apoyo = sim.simxGetObjectHandle(clientID, 'apoyo', sim.simx_opmode_blocking)
        retcode, robot = sim.simxGetObjectHandle(clientID, 'UR5', sim.simx_opmode_blocking)

        retcode, oriOrigin = sim.simxGetObjectOrientation(clientID, originalPosition, -1, sim.simx_opmode_blocking)
        retcode, posOrigin = sim.simxGetObjectPosition(clientID, originalPosition, -1, sim.simx_opmode_blocking)




        grab_grey(clientID, UR5)

        t.sleep(0.5)
        movimiento(clientID, UR5, posOrigin, oriOrigin)

        grab_red(clientID, UR5)
        grab_blue(clientID, UR5)





        """
        window = tkinter.Tk()
        window.geometry("500x200")
        buttonInc = tkinter.Button(window,text="sube")
        buttonInc.place(x=50, y=50)
        buttonDec = tkinter.Button(window,text="baja")
        entry = tkinter.Entry()
        buttonInc.config(command=lambda: subeJ1(clientID, joint1))
        buttonDec.config(command=lambda: bajaJ1(clientID, joint1, entry.get()))
        buttonInc.pack()
        buttonDec.pack()
        entry.pack()
        window.mainloop()
       
        print("despues de los handles")
        retcode, cilinder = sim.simxGetObjectHandle(clientID, 'cilDum', sim.simx_opmode_blocking)

        print("test")
        retcode, UR5_pos = sim.simxGetObjectPosition(clientID, UR5,-1, sim.simx_opmode_blocking)
        retcode, UR5_or = sim.simxGetObjectOrientation(clientID, UR5, -1, sim.simx_opmode_blocking)
        print(UR5_pos)
        print(UR5_or)

        retcode, cilinderPos = sim.simxGetObjectPosition(clientID, cilinder,-1, sim.simx_opmode_blocking)

        #retcode, UR5_or = sim.simxSetObjectOrientation(clientID, UR5, 0,[cilinderPos[0],cilinderPos[1],0], sim.simx_opmode_blocking)
        print(UR5_or)
        print(cilinderPos)

        retcode, jacoTip = sim.simxGetObjectHandle(clientID, 'jaco_tip', sim.simx_opmode_blocking)
      
        pi = 3.141592653
        sim.simxSetJointTargetPosition(clientID, joint1, pi * 3 / 4, sim.simx_opmode_blocking)
        t.sleep(0.4)
        sim.simxSetJointTargetPosition(clientID, joint2, pi / 6, sim.simx_opmode_blocking)
        t.sleep(0.4)
        sim.simxSetJointTargetPosition(clientID, joint3, pi / 7, sim.simx_opmode_blocking)
        t.sleep(0.4)
        # sim.simxSetJointTargetPosition(clientID, joint4, 20, sim.simx_opmode_blocking)
        sim.simxSetJointTargetPosition(clientID, joint5, -0.4, sim.simx_opmode_blocking)
        sim.simxSetJointTargetPosition(clientID, joint6, pi * 3 / 4, sim.simx_opmode_blocking)
        t.sleep(0.4)
        """
        print("Hola")

        #sim.simxSetObjectPosition(clientID,jacoTip,-1,cilinderPos,sim.simx_opmode_blocking)
        #sim.simxSetJointTargetPosition(clientID, joint1, 2.65, sim.simx_opmode_blocking)

        #for i in range(6):
        #   joints[i] = sim.simxGetObjectHandle(clientID, 'joint'+str(i + 1), sim.simx_opmode_blocking)

        #sim.simxSetJointTargetPosition(clientID,joint1,cilinderPos,sim.simx_opmode_blocking)
    except:
        print("No se ha podido conectar")

