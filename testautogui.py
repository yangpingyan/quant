#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 1:13 
# @Author : yangpingyan

import pyautogui
screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(screenWidth / 2, screenHeight / 2)

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
pyautogui.moveTo(100, 150)
pyautogui.click()
#  鼠标向下移动10像素
pyautogui.moveRel(None, 10)
pyautogui.doubleClick()
#  用缓动/渐变函数让鼠标2秒后移动到(500,500)位置
#  use tweening/easing function to move mouse over 2 seconds.
pyautogui.moveTo(1800, 500, duration=2, tween=pyautogui.easeInOutQuad)
#  在每次输入之间暂停0.25秒
pyautogui.typewrite('Hello world!', interval=0.25)
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')

pyautogui.PAUSE = 2.5
pyautogui.moveTo(100,100); pyautogui.click()


distance = 200
while distance > 0:
    pyautogui.dragRel(distance, 0, duration=0.5) # 向右
    distance -= 5
    pyautogui.dragRel(0, distance, duration=0.5) # 向下
    pyautogui.draInRel(-distance, 0, duration=0.5) # 向左
    distance -= 5
    pyautogui.dragRel(0, -distance, duration=0.5) # 向上