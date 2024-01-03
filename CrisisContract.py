import keyboard
import threading
import time
import os
import tkinter as tk

# 合约
class Contract:
    def __init__(self):
        # 合约列表
        self.contract_list = [
                10, "冲刺次数不超过10次*",
                20, "单手游戏*",
                25, "禁止空格",
                25, "按下方向键后立刻触发冲刺",
                35, "只能同时按下一个方向键",
                35, "遮住屏幕右侧3/4的区域",
                40, "上下翻转屏幕*",
                80, "禁止向左移动",
                10, "检测"
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
    def choose(self,id):
        id = int(id)
        try:
            if id <= self.term_num and id > -1:
                if id == 0:
                    return 0
                if self.contract_dic[id] == " ":
                    self.contract_dic[id] = "√"
                else:
                    self.contract_dic[id] = " "
                return 1
            else:
                print("输入的数字不合理，请重新输入!")
                time.sleep(1)
                return 1
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
        keys = ['W', 'A', 'S', 'D', 'Up', 'Left', 'Down', 'Right', 'Space']
        arrowkeys = ['W', 'A', 'S', 'D', 'Up', 'Left', 'Down', 'Right']
        def DetectionThread():
            def KeyboardDetection():
                # 当前按下的按键列表
                pressedkeys = [key for key in keys if keyboard.is_pressed(key)]
                

            while True:
                KeyboardDetection()

        thread = threading.Thread(target=DetectionThread)
        thread.start()


        # 冲刺次数不超过10次
        if self.contract_dic[1] == "√":
            self.tendash = 1

        # 禁止空格冲刺
        if self.contract_dic[3] == "√":
            keyboard.block_key("space")

        # 按下方向键后立刻触发冲刺
        if self.contract_dic[4] == "√":
            def on_key_event(e):
                if e.name in arrowkeys:
                    keyboard.press_and_release('space')
            keyboard.on_press(on_key_event)     # 监听按键事件


        #只能同时按下一个方向键
        if self.contract_dic[5] == "√":

            def detect_key():
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
            detect_key()
            
            
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

        # 禁止向左移动
        if self.contract_dic[8] == "√":
            keyboard.block_key("left")
            keyboard.block_key("a")

        if self.contract_dic[9] == "√":
            def thetest():
                print("123")
            thetest()

        






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
            if self.contract.choose(input("(选择合约请输入数字序号并回车)\n(最后启动合约请输入0)\n")) == 0:    # 选择合约条目
                break
        self.contract.run()
        keyboard.wait('esc')

# 主函数入口点
if __name__ == "__main__":
    program = MainProgram()
    program.run()