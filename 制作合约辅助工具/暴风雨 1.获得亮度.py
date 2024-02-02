#===================================================================================#

# 精确获得pvz黑暗的暴风雨夜的照明亮度序列的方法：

# 录屏，使用Pr导出每一帧的png图片，图片名称为a0000, a0001, ... a2279，存放于py文件同层的picture文件夹内

# 运行 获得亮度.py，打印出亮度列表，列表内值的范围是22~251

# 复制粘贴列表进 处理序列.py

#===================================================================================#

import cv2
import time
import tkinter as tk
import keyboard
import pyscreenshot

a=b=c=d=0

def get_brightness(x, y):
    # 截屏并保存为临时文件
    # screenshot = pyscreenshot.grab()
    # screenshot.save("screenshot.png")
    
    # 读取保存的截图
    screenshot = cv2.cvtColor(cv2.imread(f"picture/a{a}{b}{c}{d}.png"), cv2.COLOR_BGR2GRAY)
    
    # 获取指定坐标的像素值
    brightness = screenshot[y, x]
    
    return brightness

def carry(left,right):
    if right == 10:
            right = 0
            left = left + 1
    return [left,right]
    
# 获取屏幕分辨率
# root = tk.Tk()
# screen_width = root.winfo_screenwidth() * 2
# screen_height = root.winfo_screenheight() * 2
# print(f"屏幕分辨率：{screen_width}x{screen_height}")
# 指定屏幕坐标 x,y = 
# 若屏幕分辨率为 3200 x 2000：
#
#    0,0  ----------> (x)  3199
#     |
#     |
#     |
#     v
#    (y)
#
#   1999,0   
    
# x, y = int(screen_width / 2 -1) , int(screen_height / 2 -1)

# 导出图像的分辨率为32，20
x,y=15,9 # 获取图片中央的值

try:
    list = []
    while True:
        # 获取亮度
        brightness = get_brightness(x, y)
        print(f"Brightness at ({x}, {y}): {brightness}")
        list.append(brightness)
        
        # 低效冗杂（但可用）的加法进位
        d = d+1
        temp = carry(c,d)
        c = temp[0]
        d = temp[1]
        temp = carry(b,c)
        b = temp[0]
        c = temp[1]
        temp = carry(a,b)
        a = temp[0]
        b = temp[1]

        if a==2 and b==2 and c==7 and d==9:
            break

        if keyboard.is_pressed("esc"):
            break

        # time.sleep(0.01)
        
    print(list)

except KeyboardInterrupt:
    print("程序已停止")