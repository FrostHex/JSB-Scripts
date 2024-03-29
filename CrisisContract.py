import keyboard
import threading
import time
import os
import sys
import tkinter as tk
import rotatescreen
import random
from datetime import datetime
# 实现点击穿透
import ctypes
from win32api import SetWindowLong,RGB
from win32con import WS_EX_LAYERED,WS_EX_TRANSPARENT,GWL_EXSTYLE,LWA_ALPHA
from win32gui import SetLayeredWindowAttributes

# 合约
class Contract:
    def __init__(self):
        # 合约的二维列表, 每个条目内的参数为 [分数, 内容, 选中状态]
        self.contract_list = [
                [20, '随机选择下列1~3条 (选中此条后将会跳过选择直接运行!)'],
                [20, '按下方向键后立刻触发冲刺'],
                [25, '冲刺附带三秒冷却'],
                [25, '只能同时按下一个方向键'],
                [25, '出现弹跳窗口遮挡屏幕'],
                [30, '不断出现窗口遮挡屏幕'],
                [30, '遮住屏幕右侧3/4的区域'],
                [30, '屏幕逐渐变暗，按空格恢复'],
                [40, '上下翻转屏幕'],
                [60, '禁止向左移动']
            ]
        
        self.score = 0  # 总分数
        self.term_num = len(self.contract_list)  # 合约总数
        for i in range(self.term_num):  # 生成第三栏'选中状态', 初始化为不勾选
            self.contract_list[i].append('-')  

        # 测试某一条合约用，减轻输入负担
        # self.contract_list[8][2]= "√"

    # 展示合约信息
    def show_info(self):
        # 列出合约条目
        for i in range(self.term_num):
            print(f"{self.contract_list[i][2]} {i+1}.{self.contract_list[i][1]} ({self.contract_list[i][0]}分)")

        # 计算当前分数
        self.score = 0
        for i in range(self.term_num):
            if self.contract_list[i][2] == "√":
                self.score += self.contract_list[i][0]
        print("-"*15 + f"\n总分数: {self.score}")

    # 输入选择合约条目 (返回值: 0循环 1结束 2报错)
    def choose(self):
        print("-"*15 + "\n请选择合约请输入数字序号并回车 (输入多个合约用空格分隔)\n" + "\033[32;1m" + "选择完成后开始运行请双击回车\n" + "\033[0m" + "您将有2秒准备时间, 启动后请迅速切换至游戏\n在按Delete键退出之前不要切换到其他窗口\n")
        ids = input()
        try:
            if ids == '':  # 若用户只输入回车
                return 1
            id_list = [int(i) for i in ids.split()]  # 将输入的数字字符串分割成列表, 并转换为int型
            for id in id_list:  # 选中此条合约, 若此条目已选中则将其取消
                if id <= self.term_num and id > 0:
                    if self.contract_list[id-1][2] == '-':
                        # 禁同时选的模板代码
                        # if id == 3:
                        #     self.contract_list[3][2] = '-'
                        # elif id == 4:
                        #     self.contract_list[2][2] = '-'
                        if id == 1:
                            random_contract = [random.randint(1, 9) for _ in range(3)]
                            for i in range(3):
                                self.contract_list[random_contract[i]][2] = '√'
                        self.contract_list[id-1][2] = '√'
                        if self.contract_list[0][2] == '√':
                            keyboard.send('enter')
                    else:
                        self.contract_list[id-1][2] = '-'
                else:
                    print(f"输入的数字 {id} 不合理，请重新输入!")
                    time.sleep(1)
            return 0
        except Exception as e:
            print(f"发生了异常：{e}")
            print(random_contract)
            time.sleep(10)
            return 2  # 目前没用上

    # 开始运行合约
    def run(self):
        # 用文档记录分数
        def append_to_score_file(score):
            file_path = "Score.txt"

            # 检查文件是否存在，如果不存在则创建
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write("")
            contract_name = []
            for ctr in self.contract_list:
                if ctr[2] == '√':
                    contract_name.append(ctr[1])

            contract_name_utf8 = str(contract_name)
            
            # 在文件末尾追加一行文字
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\t'+ contract_name_utf8 + '\t' + score + "\n")
        
        # 生成小悬浮窗提示合约启动
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
            label = tk.Label(root, text="合约启动 按 Delete 键退出", font=font_style, fg="white", bg="black")
            label.pack(pady=60)

        def hide_root(window, delay):
            window.after(delay, lambda: window.geometry("1x1+0+0"))

        # 打印按下的按键
        # def DetectionThread():
        #     def KeyboardDetection():
        #         global pressedkeys 
        #         pressedkeys = [key for key in keys if keyboard.is_pressed(key)] # 当前按下的按键列表
        #         print(pressedkeys)
        #        
        #     while True:
        #         KeyboardDetection()

        # keys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right', 'space']
        arrowkeys = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right']
        print("\033[31;1m即将开始运行合约, 按 Delete 键终止程序\033[0m")
        append_to_score_file(str(self.score))
        root = tk.Tk()
        start_root(root)
        root.after(2000, lambda: hide_root(root, 0))
        # detectthread = threading.Thread(target=DetectionThread)
        # detectthread.start()
        time.sleep(2)


        #=================================== 合约内容代码 ===================================#

        # 2.按下方向键后立刻触发冲刺
        if self.contract_list[1][2] == "√":
            def on_key_event_4(e):
                nonlocal spaceblocking
                if e.name in arrowkeys and not spaceblocking:
                    for key in arrowkeys:
                        if keyboard.is_pressed(key):
                            keyboard.send('space')
                            if self.contract_list[0][2] == "√":
                                class espace:
                                    pass
                                espace = espace()
                                espace.name = "space"
                                space_event(espace)
                                
            spaceblocking = False                    
            keyboard.on_press(on_key_event_4)     # 监听按键事件

        # 3.冲刺附带三秒冷却
        if self.contract_list[2][2] == "√":
            def space_event(e):
                nonlocal spaceblocking
                if e.name == "space" and not spaceblocking:
                    spaceblocking = True
                    keyboard.block_key("space")
                    time.sleep(3)
                    keyboard.unblock_key("space")
                    keyboard.release("space")
                    spaceblocking = False
            
            spaceblocking = False
            thread = threading.Thread(target=keyboard.on_press, args=(space_event,))  # ags传参,附带逗号表示单个元素的元组
            thread.start()

        # 4.只能同时按下一个方向键
        if self.contract_list[3][2] == "√":
            def chopsticks(key):
                for fkey in arrowkeys:
                    if fkey != key.name and key.name in arrowkeys:
                        keyboard.release(fkey)
                        
            keyboard.on_press(chopsticks)

        # 5.出现弹跳窗口遮挡屏幕
        if self.contract_list[4][2] == "√":
            if self.contract_list[5][2] == "√":
                def open_window():
                    # 初始化
                    window = [tk.Toplevel(root) for _ in range(6)] # 创建6个顶级窗口
                    sidelength = window[0].winfo_screenwidth() // 4 # 计算每个窗口的边长
                    width = window[0].winfo_screenwidth() - sidelength # 计算窗口的宽度
                    height = window[0].winfo_screenheight() - sidelength # 计算窗口的高度
                    vx = [10 + random.randint(-5,5) for _ in range(6)] # 随机生成水平速度
                    vy = [10 + random.randint(-5,5) for _ in range(6)] # 随机生成垂直速度
                    x = [random.randint(0, width) for _ in range(6)] # 随机生成初始水平位置
                    y = [random.randint(0, height) for _ in range(6)] # 随机生成初始垂直位置
                    for i in range(6):
                        window[i].title("弹弹弹") # 设置窗口标题
                        window[i].configure(bg="#fe1f6f") # 设置窗口背景色为粉红色
                        window[i].attributes('-topmost', True)  # 置顶窗口
                        window[i].attributes('-disabled', True)  # 禁止点击
                    # 循环更新位置
                    while True:
                        for i in range(6):
                            window[i].geometry(f"{sidelength}x{sidelength}+{x[i]}+{y[i]}") # 设置窗口的几何属性
                            if x[i] >= width or x[i] <= 0: # 如果窗口碰到水平边界，反转水平速度方向
                                vx[i] = -1 * vx[i]
                            if y[i] >= height or y[i] <= 0: # 如果窗口碰到垂直边界，反转垂直速度方向
                                vy[i] = -1 * vy[i]
                            x[i] = x[i] + vx[i] # 更新水平位置
                            y[i] = y[i] + vy[i] # 更新垂直位置
                        time.sleep(0.015)  # 稍微延迟，控制动画速度
                    # window.after(1000, lambda: window.destroy())
                
            else:
                def open_window():
                    window = tk.Toplevel(root)  # 创建一个顶级窗口
                    sidelength = window.winfo_screenwidth() // 5
                    width = window.winfo_screenwidth() - sidelength
                    height = window.winfo_screenheight() - sidelength
                    vx = 20
                    vy = 15
                    x = random.randint(0, width)
                    y = random.randint(0, height)

                    # window.title("弹弹弹")
                    window.configure(bg="#fe1f6f")
                    window.attributes('-topmost', True)
                    window.attributes('-disabled', True)

                    # 拖尾窗口降低透明度
                    def shrink_window(windows):
                        # 获得透明度 减小窗口的透明度
                        transparency = windows.attributes('-alpha') - 0.05
                        # 更新窗口透明度
                        if transparency >= 0:
                            windows.attributes('-alpha', transparency)
                        else:
                            windows.destroy()

                        # 每隔一段时间调用shrink_window函数
                        if windows.winfo_exists():
                            windows.after(100, shrink_window, windows)


                    def set_track(window):
                        window.geometry(f"{sidelength}x{sidelength}+{x}+{y}")
                        window.configure(bg="#fe1f6f")
                        window.overrideredirect(True)
                        window.attributes('-topmost', True)
                        shrink_window(window)
                    counter = 0
                    while True:
                        counter += 1
                        if counter == 5:
                            counter = 0
                            track = tk.Toplevel(root)  # 创建一个顶级窗口
                            set_track(track)
                        
                        if x >= width or x <= 0:
                            vx = -1 * vx
                        if y >= height or y <= 0:
                            vy = -1 * vy
                        x = x + vx
                        y = y + vy
                        window.geometry(f"{sidelength}x{sidelength}+{x}+{y}")
                        time.sleep(0.015)

            lockthread = threading.Thread(target=open_window)
            lockthread.start()

        # 6.不断出现窗口遮挡屏幕
        if self.contract_list[5][2] == "√":
            # if not self.contract_list[4][2] == "√":
                def set_window2(window):
                    window.title("HELLO")
                    window.configure(bg="#fe1f6f")
                    window.attributes('-topmost', True)  # 置顶窗口
                    window.attributes('-disabled', True)  # 禁止点击
                    sidelength = window.winfo_screenwidth() // 4
                    width = window.winfo_screenwidth() - sidelength
                    height = window.winfo_screenheight() - sidelength
                    # 设置窗口位置和大小
                    window.geometry(f"{sidelength}x{sidelength}+{random.randint(0, width)}+{random.randint(0, height)}") 
                    
                def open_window(index):
                    window = tk.Toplevel(root)
                    set_window2(window)
                    window.after(200, lambda: open_window(index + 1))  # 200ms后执行匿名函数, 匿名函数调用 open_window 函数, 传参 index+1
                    window.after(1000, lambda: window.destroy())

                open_window(0)

        # 7.遮住屏幕右侧3/4的区域
        if self.contract_list[6][2] == "√":
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

        # 8.屏幕逐渐变暗，冲刺时恢复
        if self.contract_list[7][2] == "√":
            # 窗口穿透, 防止置顶窗口占用焦点
            def setWinThrowON():
                while True:
                    hwnd = ctypes.windll.user32.FindWindowW(None, "tempestissimo")
                    if hwnd != 0:
                        hWindow = hwnd
                        exStyle = WS_EX_LAYERED | WS_EX_TRANSPARENT
                        SetWindowLong(hWindow, GWL_EXSTYLE, exStyle)
                        SetLayeredWindowAttributes(hWindow, RGB(0, 0, 0), 150, LWA_ALPHA)
                        break
                    time.sleep(0.1)
       
            def set_transparency(window, alpha):
                window.attributes('-alpha', alpha)  # 设置窗口透明度

            def set_background_color(window, color):
                window.configure(bg=color)  # 设置窗口背景颜色

            def set_window(window):
                window.attributes('-topmost', True)  # 置顶窗口
                window.overrideredirect(True)  # 隐藏窗口
                window.attributes('-disabled', True)  # 禁止点击
                window.title("tempestissimo") 
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                width = screen_width
                height = screen_height - 2
                window.geometry(f"{width}x{height}+{screen_width - width}+0")  # 设置窗口位置和大小

            def flash():
                while True:
                    if self.add == 1:
                        self.add = 0
                        # print (self.add)
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
                        # 可修改random.randint()内的参数, 值越大照明时间越长
                        # 总持续时间为: 随机出的整数 * 0.15
                        self.linger = round(random.randint(4, 10) * 0.0015, 4)  # round( ,4)保留4位小数
                        flash_sequence = dissipate_sequence
                        for i in range(len(flash_sequence)):
                            if self.add == 1:
                                break
                            set_transparency(storm, flash_sequence[i])  # 读取序列
                            # print(flash_sequence[i])
                            # print('linger:'+str(self.linger))
                            time.sleep(self.linger)
                        # 光芒余波
                        flash_sequence = aftermath_list[random.randint(0,3)]
                        for i in range(len(flash_sequence)):
                            if self.add == 1:
                                break
                            set_transparency(storm, abs(flash_sequence[i]))  # 读取序列
                            # print(flash_sequence[i])
                            # print('linger:'+str(self.linger))
                            time.sleep(0.02)
                    time.sleep(0.05)
            
            def stromstart():
                while True:
                    if keyboard.is_pressed("delete"):
                        storm.destroy()
                    elif keyboard.is_pressed("space"):
                        if self.lock == 0:
                            self.lock = 1  # 锁定
                            # print (self.lock)
                            self.add = 1 # 可以添加新闪电
                            # print (self.add)
                    time.sleep(0.1)

            def on_key_release(event):
                if event.name == 'space':
                    self.lock = 0  # 解锁
                    # print (self.lock)

            def lock():
                while 1:
                    keyboard.on_release_key('space', on_key_release)   
                    keyboard.wait() # 阻塞等待，松开空格进on_key_release回调
                    time.sleep(0.1)

            self.add = 0  # 添加闪屏的标志位
            self.lock = 0  # 控制闪屏冷却的标志位
            # 消散序列
            dissipate_sequence = [int(0.1 * 1.05 ** (i + 41.6)) / 100 for i in range(1,101)]
            # 余波列表，从列表中抽取作为余波序列
            aftermath_list = [
                [1.0],
                [1.0, 1.0, 1.0, 1.0, 0.7, 0.2664, 0.2664, 0.31, 0.31, 0.2926, 0.2926, 0.2926, 0.3624, 0.4061, 0.4061, 0.4061, 0.4061, 0.4061, 0.4236, 0.5721, 0.5721, 0.5721, 0.6157, 0.6157, 0.5459, 0.5721, 0.5721, 0.5721, 0.6157, 0.6157, 0.6157, 0.738, 0.738, 0.738, 0.7904, 0.7904, 0.8341, 0.9039, 0.9039, 0.9039, 0.9214, 0.9214, 0.9214, 0.9476, 0.9476, 0.9476, 0.9301, 0.9301, 0.9913, 0.9913, 0.9913, 0.9913, 0.9913, 0.9476, 0.9476, 0.9651, 0.9651, 0.9651, 0.9651, 0.9651, 0.9651, 0.9913, 0.9913, 0.9913, 0.9913, 0.9913, 1.0, 1.0, 1.0, 0.9825, 0.9825, 0.9825, 0.9825, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9913, 0.9913, 0.9913, 1.0],
                [1.0, 1.0, 1.0, 1.0, 0.7, 0.2485, 0.3706, 0.3709, 0.3708, 0.3186, 0.3193, 0.3183, 0.3631, 0.3614, 0.4675, 0.4682, 0.4764, 0.4765, 0.5275, 0.528, 0.5807, 0.5805, 0.581, 0.581, 0.5808, 0.6061, 0.6078, 0.6508, 0.6411, 0.6411, 0.7285, 0.7293, 0.7295, 0.7729, 0.7731, 0.7724, 0.782, 0.7816, 0.9121, 0.9126, 0.9127, 0.9483, 0.9482, 0.9309, 0.9293, 0.9474, 0.9485, 0.947, 0.9394, 0.9648, 0.9659, 0.9301, 0.9305, 0.956, 0.9557, 0.9661, 0.9651, 0.9922, 0.9914, 0.9906, 0.9481, 0.9484, 0.9484, 0.9479, 0.9483, 0.9477, 0.9479, 0.9819, 0.9827, 0.9823, 0.982, 0.9824, 0.9829, 0.9643, 0.9653, 0.9993, 1.0002, 1.0006, 1.0, 1.0, 0.9917, 0.9906, 0.9918, 0.9923, 0.992, 0.9918, 0.9913, 0.9913, 0.9912, 1.0],
                [1.0, 1.0, 1.0, 1.0, 0.7, 0.1965, 0.1965, 0.31, 0.3537, 0.3537, 0.3537, 0.4148, 0.4148, 0.4061, 0.4061, 0.4061, 0.4323, 0.5022, 0.5022, 0.5022, 0.5371, 0.5371, 0.5371, 0.607, 0.607, 0.6507, 0.6507, 0.6507, 0.6943, 0.6943, 0.738, 0.738, 0.738, 0.7293, 0.7904, 0.7904, 0.7904, 0.8166, 0.8166, 0.8166, 0.8515, 0.8515, 0.8515, 0.8865, 0.8865, 0.9301, 0.9301, 0.9825, 0.9825, 0.9825, 0.9825, 0.9825, 0.9825, 0.9825, 0.9825, 1.0],
                [1.0, 1.0, 1.0, 1.0, 0.7, 0.1965, 0.1965, 0.25, 0.31, 0.3537, 0.3537, 0.3537, 0.81, 0.4148, 0.4061, 0.4061, 0.21, 0.4323, 0.5022, 0.5022, 0.62, 0.71, 0.5371, 0.5371, 0.5371, 0.607, 0.732, 0.607, 0.6507, 0.6507, 0.6507, 0.6943, 0.6943, 0.738, 0.738, 0.738, 0.7293, 0.7904, 0.7904, 0.7904, 0.8166, 0.8166, 0.792, 0.8515, 0.8515, 0.8515, 0.8865, 0.8865, 0.9301, 0.9301, 0.9825, 0.65, 0.72, 0.9825, 0.9825, 0.9825, 0.9825, 0.9825, 1.0]
                ]
            storm = tk.Toplevel(root)
            set_background_color(storm, "black")  # 初始化窗口为半透明
            set_transparency(storm, 0.5)
            set_window(storm)
            original_position = (storm.winfo_x(), storm.winfo_y())
            setWinThrowtread = threading.Thread(target=setWinThrowON)  # 设置窗口穿透线程
            setWinThrowtread.start()
            stormthread = threading.Thread(target=stromstart)  # 设置暴风雨线程，控制锁定、允许添加新闪电
            stormthread.start()
            flashthread = threading.Thread(target=flash)  # 设置闪屏线程，执行闪电并清除添加闪电的标志位
            flashthread.start()
            lockthread = threading.Thread(target=lock)  # 设置闪屏冷却线程，控制解锁
            lockthread.start()

        # 9.上下翻转屏幕
        if self.contract_list[8][2] == "√":
            screen = rotatescreen.get_primary_display()
            screen.rotate_to(180)

        # 10.禁止向左移动
        if self.contract_list[9][2] == "√":
            keyboard.block_key("left")
            keyboard.block_key("a")

        root.mainloop()
        #===================================================================================#


# 主类 
class MainProgram:
    def __init__(self):
        self.contract = Contract() 

    def restart_program(self, e):
        print("Restarting program...")
        screen = rotatescreen.get_primary_display()  # 获取主显示器对象
        screen.rotate_to(0)  # 屏幕旋转归零
        del self.contract  # 删除实体释放内存
        python = sys.executable
        os.execl(python, python, *sys.argv)  # 启动一个新的 Python 进程

    def run(self):
        keyboard.on_press_key('delete', self.restart_program)
        while True:
            print("请选择挑战合约: \n")
            os.system('cls')  # 清除终端内的文字
            self.contract.show_info()  # 展示合约列表
            if self.contract.choose() == 1:  # 选择合约条目
                break
        self.contract.run()  # 开始运行合约
        keyboard.wait()

# 主函数入口点
if __name__ == "__main__":
    program = MainProgram()
    program.run()