#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import threading
import time

class PS4Controller(threading.Thread):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def __init__(self,lock,rate):
        threading.Thread.__init__(self)
        self.lock = lock
        self.rate = rate
        self.keys = {}
        self.init()


    def init(self):
        """Initialize the joystick components"""
        threading.Thread.__init__(self)
        self.axis_data = { i:0 for i in range(6)}
        self.button_data = { i:0 for i in range(12)}
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()


    def run(self):
        """Listen for events to happen"""
        print "started"
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                self.setKeys()
                time.sleep(self.rate)
                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
    def getKeys(self):
        self.lock.acquire()
        ans = self.keys
        self.lock.release()
        return ans


    def setKeys(self):
        self.lock.acquire()
        self.keys = { 
            #"buttons" : self.button_data,
            "arrows" : {
                "x" : self.hat_data[0][0],
                "y" : self.hat_data[0][1],
            },
            "joysticks" : {
                "left" : {
                    "x" : self.axis_data[0],
                    "y" : -self.axis_data[1],
                },
                "right" : {
                    "x" : self.axis_data[2],
                    "y" : -self.axis_data[3],
                },
            },
            "back_buttons" : {
                "L" : self.axis_data[4]+1,
                "R" : self.axis_data[5]+1,
            },
            "buttons" : {
                "X" : self.button_data[1],
                "O" : self.button_data[2],
                "T" : self.button_data[3],
                "S" : self.button_data[0],
                "L1" : self.button_data[4],
                "R1" : self.button_data[5],
                "R2" : self.button_data[7],
                "R3" : self.button_data[11],
            }
        }
        self.lock.release()
