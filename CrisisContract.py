import keyboard
import threading
import time
import os
import tkinter as tk
import rotatescreen
import pyautogui
import random


# 合约
class Contract:
    def __init__(self):
        # 合约列表
        self.contract_list = [
                20, "冲刺附带五秒冷却",
                60, "禁止向左移动",
                25, "禁止空格",
                25, "按下方向键后立刻触发冲刺",
                35, "只能同时按下一个方向键",
                35, "遮住屏幕右侧3/4的区域",
                40, "上下翻转屏幕",
                20, "屏幕逐渐变暗，按空格恢复",
                1, "检测"
            ]
        
        # 合约总数
        self.term_num = int(len(self.contract_list) / 2)
        
        # 合约选中状态
        self.contract_dic = {}
        for i in range(1 , self.term_num + 1):
            self.contract_dic[i] = " "

    # 展示合约列表
    def show_info(self):
        for i in range(1 , self.term_num + 1):
            print(f"{self.contract_dic[i]} {i}.{self.contract_list[i*2-1]} ({self.contract_list[i*2-2]}分)")

    # 选择合约条目
    def choose(self, ids):
        try:
            id_list = [int(i) for i in ids.split()]  # 将输入的数字字符串分割成列表
            for id in id_list:
                if id <= self.term_num and id > -1:
                    if self.contract_dic[id] == " ":
                        self.contract_dic[id] = "√"
                    else:
                        self.contract_dic[id] = " "
                else:
                    print(f"输入的数字 {id} 不合理，请重新输入!")
                    time.sleep(1)
            return 0
        except ValueError:
            print("输入的数字不合理，请重新输入!")
            time.sleep(1)
            return 1

    # 计算分数
    def calculate_score(self):
        self.score = 0
        for i in range(1 , self.term_num + 1):
            if self.contract_dic[i] == "√":
                self.score += self.contract_list[i*2-2]
        print(f"总分数: {self.score}")

    # 开始运行合约
    def run(self):
        print("开始运行合约, 按ESC终止程序")
        self.quit = 0
        keys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right', 'space']
        arrowkeys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right']
        def DetectionThread():
            def KeyboardDetection():
                # 当前按下的按键列表
                global pressedkeys
                pressedkeys = [key for key in keys if keyboard.is_pressed(key)]
                
            while True:
                KeyboardDetection()
        detectthread = threading.Thread(target=DetectionThread)
        #detectthread.start()


        # 冲刺后等待5秒才能继续冲刺
        if self.contract_dic[1] == "√":
            spaceblocking = False
            def space_event(e):
                nonlocal spaceblocking
                if e.name == "space" and not spaceblocking:
                    spaceblocking = True
                    keyboard.block_key("space")
                    time.sleep(5)
                    keyboard.unblock_key("space")
                    spaceblocking = False
            thread = threading.Thread(target=keyboard.on_press, args=(space_event,))
            thread.start()

        # 禁止向左移动
        if self.contract_dic[2] == "√":
            keyboard.block_key("left")
            keyboard.block_key("a")

        # 禁止空格冲刺
        if self.contract_dic[3] == "√":
            keyboard.block_key("space")

        # 按下方向键后立刻触发冲刺
        if self.contract_dic[4] == "√":
            spaceblocking = False
            def on_key_event(e):
                nonlocal spaceblocking
                if e.name in arrowkeys and not spaceblocking:
                    for key in arrowkeys:
                        if keyboard.is_pressed(key):
                            pyautogui.press('space')
            keyboard.on_press(on_key_event)     # 监听按键事件

        #只能同时按下一个方向键
        if self.contract_dic[5] == "√":

            def chopsticks():
                key_state = False
                while True:

                    pressedkey = None
                    for key in arrowkeys:
                        if keyboard.is_pressed(key):
                            pressedkey = key
                            break
                    #遍历词典，检测按下的键

                    if pressedkey in arrowkeys:
                        if not key_state:
                            for key in arrowkeys:
                                if key != pressedkey:
                                    keyboard.block_key(key)
                            key_state = True
                            global releasedkey
                            releasedkey = pressedkey
                            #按下按键屏蔽其他键
                    else:
                        if key_state:
                            for rkey in arrowkeys:
                                if rkey != releasedkey:
                                    keyboard.unblock_key(rkey)
                            key_state = False
                            #松开恢复
            chopsthread = threading.Thread(target=chopsticks)
            chopsthread.start()
            
            
        # 遮住屏幕右侧3/4的区域
        if self.contract_dic[6] == "√":
            def set_topmost(window):
                window.attributes('-topmost', True)  # 置顶窗口

            def set_geometry(window):
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()

                width = screen_width // 4 * 3  # 右侧四分之三的宽度
                height = screen_height

                window.geometry(f"{width}x{height}+{screen_width - width}+0")  # 设置窗口位置和大小

            root = tk.Tk()
            root.title("右侧四分之三")
            set_topmost(root)
            set_geometry(root)
            root.update()

        #上下翻转屏幕
        if self.contract_dic[7] == "√":

            screen = rotatescreen.get_primary_display()
            screen.rotate_to(180)
            def restore():
                screen.rotate_to(0)
            keyboard.on_press_key("esc", restore)

        #屏幕逐渐变暗，冲刺时恢复
        if self.contract_dic[8] == "√":
            def set_transparency(window, alpha):
                window.attributes('-alpha', alpha)  # 设置窗口透明度

            def set_background_color(window, color):
                window.configure(bg=color)  # 设置窗口背景颜色

            def set_window(window):
                window.attributes('-topmost', True)  # 置顶窗口
                window.overrideredirect(True)  #隐藏窗口
                window.attributes('-disabled', True)  #禁止点击

                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                width = screen_width
                height = screen_height - 2
                window.geometry(f"{width}x{height}+{screen_width - width}+0")  # 设置窗口位置和大小

            root = tk.Tk()
            root.title("Transparent Window")
            set_background_color(root, "black")
            set_transparency(root, 0.5)
            set_window(root)
            original_position = (root.winfo_x(), root.winfo_y())
            def flash():
                for _ in range(3):
                    set_background_color(root, "white")
                    set_transparency(root, 0.4)
                    root.geometry(f"+{random.randint(-50, 50)}+{random.randint(-50, 50)}")
                    time.sleep(0.03)
                    set_background_color(root, "black")
                    set_transparency(root, 0.2)
                    root.geometry(f"+{random.randint(-50, 50)}+{random.randint(-50, 50)}")
                    time.sleep(0.03)
                root.geometry(f"+{original_position[0]}+{original_position[1]}")
                for i in range(100):
                    transparency = i / 100
                    set_transparency(root, transparency)
                    time.sleep(0.005)
                    if keyboard.is_pressed("space") == True:
                        return
            
            def cooldownfuc():
                global cooldown
                cooldown = False
                while True:
                    if keyboard.is_pressed("esc"):
                        root.destroy()
                    elif keyboard.is_pressed("space"):
                        if not cooldown:
                            cooldown = True
                            flash()
                            cooldown = False
                        else:
                            set_background_color(root, "black")
                            set_transparency(root, 0.8)
                            root.geometry(f"+{original_position[0]}+{original_position[1]}")
            cooldownthread = threading.Thread(target=cooldownfuc)
            cooldownthread.start()
            root.mainloop()

        #测试
        if self.contract_dic[9] == "√":
            def test():
                while True:
                    print(spaceblocking)
            testthread = threading.Thread(target=test)
            testthread.start()




# 主类 
class MainProgram:
    def __init__(self):
        self.contract = Contract() 

    def run(self):
        print("请选择挑战合约: \n")
        while True:
            os.system('cls')
            self.contract.show_info()    # 展示合约列表
            self.contract.calculate_score()    # 计算分数
            if self.contract.choose(input("(选择合约请输入数字序号并回车（多个合约用空格分隔）)\n(最后启动合约请输入0)\n")) == 0:    # 选择合约条目
                break
        self.contract.run()
        keyboard.wait('esc')

# 主函数入口点
if __name__ == "__main__":
    program = MainProgram()
    program.run()