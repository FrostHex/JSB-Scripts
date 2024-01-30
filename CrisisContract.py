import keyboard
import threading
import time
import os
import sys
import tkinter as tk
import rotatescreen
import random
from datetime import datetime
from pynput import keyboard as pkeyboard



# 合约
class Contract:
    def __init__(self):
        # 合约的二维列表, 每个条目内的参数为 [分数, 内容, 选中状态]
        self.contract_list = [
                [20, '冲刺附带五秒冷却'],
                [60, '禁止向左移动'],
                [25, '禁止空格'],
                [25, '按下方向键后立刻触发冲刺'],
                [35, '只能同时按下一个方向键'],
                [35, '遮住屏幕右侧3/4的区域'],
                [40, '上下翻转屏幕'],
                [25, '屏幕逐渐变暗，按空格恢复'],
                [20, '不断出现窗口遮挡屏幕'],
                [1,  '检测']
            ]
        
        self.score = 0  # 总分数
        self.term_num = len(self.contract_list)  # 合约总数
        for i in range(self.term_num):  # 初始化合约选中状态
            self.contract_list[i].append('-')

    # 展示合约列表
    def show_info(self):
        for i in range(self.term_num):
            print(f"{self.contract_list[i][2]} {i+1}.{self.contract_list[i][1]} ({self.contract_list[i][0]}分)")

        #计算当前分数
        for i in range(self.term_num):
            if self.contract_list[i][2] == "√":
                self.score += self.contract_list[i][0]
        print("-"*15 + f"\n总分数: {self.score}")


    # 选择合约条目 (返回值: 0循环 1结束 2报错)
    def choose(self):
        ids = input("-"*15 + "\n请选择合约请输入数字序号并回车 (输入多个合约用空格分隔)\n开始运行请直接输入回车\n")
        try:
            if ids == '':  # 若用户只输入回车
                return 1
            id_list = [int(i) for i in ids.split()]  # 将输入的数字字符串分割成列表, 并转换为int型
            for id in id_list:  # 选中此条合约, 若此条目已选中则将其取消
                if id <= self.term_num-1 and id > -1:
                    if self.contract_list[id-1][2] == '-':
                        self.contract_list[id-1][2] = '√'
                    else:
                        self.contract_list[id-1][2] = '-'
                else:
                    print(f"输入的数字 {id} 不合理，请重新输入!")
                    time.sleep(1)
            return 0
        except:
            print("输入有误!")
            time.sleep(1)
            return 2

    # 开始运行合约
    def run(self):
        print("开始运行合约, 按R键终止程序")
        self.quit = 0

        # 用文档记录分数
        def append_to_score_file(text):
            file_path = "Score.txt"

            # 检查文件是否存在，如果不存在则创建
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write("")

            # 在文件末尾追加一行文字
            with open(file_path, 'a') as file:
                file.write(text + "\n")
        
        append_to_score_file(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\t' + str(self.score))

        keys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right', 'space']
        arrowkeys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right']


        def start_root(window):
            window.attributes('-topmost', True)  # 置顶窗口
            window.overrideredirect(True)  #隐藏窗口
            window.attributes('-disabled', True)  #禁止点击
            window.attributes('-alpha', 0.7)
            rootx = (window.winfo_screenwidth() - 800) // 2
            rooty = window.winfo_screenheight() - 400
            window.configure(bg="black")
            window.geometry(f"800x200+{rootx}+{rooty}")
            font_style = ("Segoe UI", 32, "bold")
            label = tk.Label(root, text="合约启动 按R键退出", font=font_style, fg="white", bg="black")
            label.pack(pady=60)

        def hide_root(window, delay):
            window.after(delay, lambda: window.geometry("1x1+0+0"))

        root = tk.Tk()
        start_root(root)
        root.after(2000, lambda: hide_root(root, 0))
        


        def DetectionThread():
            def KeyboardDetection():
                # 当前按下的按键列表
                global pressedkeys
                pressedkeys = [key for key in keys if keyboard.is_pressed(key)]
                
            while True:
                KeyboardDetection()
        detectthread = threading.Thread(target=DetectionThread)
        #detectthread.start()


        # 1.冲刺附带五秒冷却
        if self.contract_list[0][2] == "√":
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

        # 2.禁止向左移动
        if self.contract_list[1][2] == "√":
            keyboard.block_key("left")
            keyboard.block_key("a")

        # 3.禁止空格
        if self.contract_list[2][2] == "√":
            keyboard.block_key("space")

        # 4.按下方向键后立刻触发冲刺
        if self.contract_list[3][2] == "√":
            spaceblocking = False
            def on_key_event(e):
                nonlocal spaceblocking
                if e.name in arrowkeys and not spaceblocking:
                    for key in arrowkeys:
                        if keyboard.is_pressed(key):
                            keyboard.send('space')
            keyboard.on_press(on_key_event)     # 监听按键事件

        # 5.只能同时按下一个方向键
        if self.contract_list[4][2] == "√":
            def chopsticks(key):
                for fkey in arrowkeys:
                    if fkey != key.name and key.name in arrowkeys:
                        keyboard.release(fkey)
            keyboard.on_press(chopsticks)
                
            
        # 6.遮住屏幕右侧3/4的区域
        if self.contract_list[5][2] == "√":
            def set_topmost(window):
                window.configure(bg="#fe1f6f")
                window.attributes('-topmost', True)  # 置顶窗口
                window.overrideredirect(True)  #隐藏窗口
                window.attributes('-disabled', True)

            def set_geometry(window):
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()

                width = screen_width // 4 * 3  # 右侧四分之三的宽度
                height = screen_height

                window.geometry(f"{width}x{height}+{screen_width - width}+0")  # 设置窗口位置和大小

            mask = tk.Toplevel(root)
            mask.title("右侧四分之三")
            set_topmost(mask)
            set_geometry(mask)
            
        # 7.上下翻转屏幕
        if self.contract_list[6][2] == "√":

            screen = rotatescreen.get_primary_display()
            screen.rotate_to(180)

        # 8.屏幕逐渐变暗，冲刺时恢复
        if self.contract_list[7][2] == "√":
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

            def flash():
                    # 闪电照亮
                    for _ in range(3):
                        set_background_color(storm, "white")
                        set_transparency(storm, 0.3)
                        storm.geometry(f"+{random.randint(-50, 50)}+{random.randint(-50, 50)}")
                        time.sleep(0.03)
                        set_background_color(storm, "black")
                        set_transparency(storm, 0.2)
                        storm.geometry(f"+{random.randint(-50, 50)}+{random.randint(-50, 50)}")
                        time.sleep(0.03)
                    storm.geometry(f"+{original_position[0]}+{original_position[1]}")
                    # 光芒消逝
                    self.linger = random.randint (50, 100)*0.02
                    for i in range(1,101):
                        set_transparency(storm, int(0.1 * 1.05 ** (i + 42)) / 100)
                        time.sleep(self.linger/100)
                    # time.sleep(0.5*(2.5-self.linger))  # 额外冷却时间
            
            def stromstart():
                while True:
                    if keyboard.is_pressed("r"):
                        storm.destroy()
                    elif keyboard.is_pressed("space") and self.cooldown == True:
                        self.cooldown = False  # 锁定
                        flash()
                        self.cooldown = True  # 解锁

            self.cooldown = True  # 控制闪电冷却
            storm = tk.Toplevel(root)
            set_background_color(storm, "black")
            set_transparency(storm, 0.5)
            set_window(storm)
            original_position = (storm.winfo_x(), storm.winfo_y())
            stormthread = threading.Thread(target=stromstart)
            stormthread.start()


        # 9.不断窗口出现遮挡屏幕
        if self.contract_list[8][2] == "√":
            def set_window2(window):
                window.title("HELLO")
                window.configure(bg="#fe1f6f")
                window.attributes('-topmost', True)  # 置顶窗口
                window.attributes('-disabled', True)  #禁止点击
                sidelength = window.winfo_screenwidth() // 4
                width = window.winfo_screenwidth() - sidelength
                height = window.winfo_screenheight() - sidelength
                window.geometry(f"{sidelength}x{sidelength}+{random.randint(0, width)}+{random.randint(0, height)}") 
                # 设置窗口位置和大小
            def open_window(index):
                window = tk.Toplevel(root)
                set_window2(window)
                window.after(200, lambda: open_window(index + 1))
                window.after(1000, lambda: window.destroy())
            open_window(0)
            
        # 10.测试
        if self.contract_list[9][2] == "√":
            def test():
                while True:
                    print(spaceblocking)
            testthread = threading.Thread(target=test)
            testthread.start()
        root.mainloop()



# 主类 
class MainProgram:
    def __init__(self):
        self.contract = Contract() 

    def restart_program(self, e):
        print("Restarting program...")
        screen = rotatescreen.get_primary_display() # 获取主显示器对象
        screen.rotate_to(0)
        del self.contract
        keyboard.press_and_release('backspace')
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def run(self):
        keyboard.on_press_key('r', self.restart_program)
        while True:
            print("请选择挑战合约: \n")
            os.system('cls')
            self.contract.show_info()    # 展示合约列表
            if self.contract.choose() == 1:    # 选择合约条目
                break
        self.contract.run()
        keyboard.wait()

# 主函数入口点
if __name__ == "__main__":
    program = MainProgram()
    program.run()