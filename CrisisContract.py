import keyboard
import time
import os
import tkinter as tk

# 合约
class Contract:
    def __init__(self):
        # 合约列表
        self.contract_list = [
                40, "方向键颠倒",
                40, "禁止向左移动",
                10, "慢郎中",
                20, "禁止冲刺",
                30, "单手游戏",
                40, "上下翻转屏幕",
                40, "一手拿一根筷子, 只能用筷子触碰按键",
                40, "遮住屏幕右侧3/4的屏幕"
            ]
        
        # 合约总数
        self.term_num = int(len(self.contract_list) / 2)
        
        # 合约选中状态
        self.contract_dic = {}
        for i in range(1 , self.term_num + 1):
            self.contract_dic[i] = " "

    # 展示合约列表
    def show_info(self):
        print("-----------------")
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

        # 方向键颠倒
        if self.contract_dic[1] == "√":
            keyboard.remap_hotkey("up", "down")
            keyboard.remap_hotkey("down", "up")
            keyboard.remap_hotkey("left", "right")
            keyboard.remap_hotkey("right", "left")
            keyboard.remap_hotkey("w", "s")
            keyboard.remap_hotkey("s", "w")
            keyboard.remap_hotkey("a", "d")
            keyboard.remap_hotkey("d", "a")

        # 禁止向左移动
        if self.contract_dic[2] == "√":
            keyboard.block_key("left")
            keyboard.block_key("a")

        # 慢郎中
        if self.contract_dic[3] == "√":
            print()

        # 禁止冲刺
        if self.contract_dic[4] == "√":
            keyboard.block_key("space")
        
        # 遮住屏幕右侧3/4的屏幕
        if self.contract_dic[8] == "√":
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
            root.mainloop()

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