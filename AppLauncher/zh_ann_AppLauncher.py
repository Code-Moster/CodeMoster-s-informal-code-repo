#源代码但是附带了详细的中文注释版

from os import system       #调用系统命令函数(位于函数makecommandfunc里)
import sys                  #调用退出(位于函数EXITHISWINDOW里)和接收命令行参数(最后一行代码里)
import customtkinter as ctk #使用customtkinter模块(其实有更好的图形模块，但如果让作者自己写的话甚至不会使用python而是C++编写)
import json                 #使用json解析函数(位于函数LoadJsonConfig里)

exitcode: int = 0 
"""
退出状态码 调用sys.exit时作为退出码
返回给父进程或操作系统来报告程序是否正常运行
(正常情况返回整数0, 其他整数都表示程序出现问题)
学过C/C++都懂这是什么意思
"""

def makecommandfunc(command: str): #用于创建函数的函数
    def commandfunc(): #创建一个函数
        system(command) #函数负责调用命令
    return commandfunc #返回函数标识
"""
用于在代码运行中动态创建函数功能
有了它妈妈就再也不用担心我创建新功能时要各种def了
"""

def LoadJsonConfig(config_path: str) -> dict: #用于读取json文件并解析的函数
    res: dict #先定义返回的结果
    try:
        f = open(config_path, "r", encoding="utf-8") #尝试以UTF8编码打开文件，找不到文件就见下面的except语句
        config: str = f.read() #读取文件的所有内容作为一个字符串存起来
        f.close() #关闭文件释放资源占用
        res = json.loads(config) #用json.loads功能解析json文件内容字符串，解析出来的是一个字典存进结果里
    except FileNotFoundError: #捕获文件找不到的报错
        res = {} #如果找不到文件就返回空字典
    return res #返回结果

def EXITHISWINDOW() -> None: #用于退出程序
    sys.exit(exitcode) #把exitcode整数变量作为退出码返回出去，前面提到过

class AppLaucher: #主应用启动器类(你应该从构造函数__init__那里看起)
    def LoadUnitConfig(self, config: dict) -> None: #用于加载一些基本配置比如窗口标题，大小等
        self.window.title(config["window_title"])                                      #获取配置字典中键为"window_title"对应的值作为标题    (其实这里可以判断一下值是否为字符串，但是作者懒得写了，以后在写吧)来自自己的吐槽: "在"字都写错了
        self.window.geometry(f"{config["window_size"][0]}x{config["window_size"][1]}") #获取配置字典中键为{懒得复制粘贴了}对应的值作为屏幕大小 (其实这里可以判断一下值是否为字符串，但是作者懒得写了，以后在写吧)
        ctk.set_default_color_theme(config["window_default_color_theme"])              #获取配置字典中键为{}对应的值作为主题配色             (其实这里可以判断一下值是否为字符串，但是作者懒得写了，以后在写吧)
        
    def LoadContent(self, config: dict) -> None: #用于加载元素如按钮，输入框等
        index: int = 0 #这边才发现调试时加的这个index变量没有作用但是作者忘记删了
        for content_config in config["content"]: #遍历配置字典中键为{懒得复制粘贴了}的包含字典的列表值为 (其实这里可以判断一下值是否为非空列表，但是作者懒得写了，以后在写吧)
            content: ctk.CTkEntry | ctk.CTkButton #定义元素变量(目前仅支持按钮和输入框，更多元素作者懒得写了，以后在写吧)
            if content_config["command"] == "ENTER": #判断当前遍历的代表元素的字典里的command键的字符串值是不是"ENTER"                         (其实这里可以判断一下值是否为字符串，但是作者懒得写了，以后在写吧)
                content = ctk.CTkEntry(self.window, width=content_config["width"]) #给主窗口创建一个输入框并读取width键的值作为输入框的宽
            elif content_config["command"] == "EXITHISWINDOW": #判断当前遍历的代表元素的字典里的command键的字符串值是不是"EXITHISWINDOW"       (其实这里可以判断一下值是否为字符串，但是作者懒得写了，以后在写吧)
                content = ctk.CTkButton(self.window, text=content_config["text"], command=EXITHISWINDOW) #给主窗口创建一个按钮，并设置显示的文本为text键对应的字符串值和把退出程序功能设置为点击时运行的功能
            else:
                content = ctk.CTkButton(self.window, text=content_config["text"], command=makecommandfunc(content_config["command"])) #给主窗口创建一个按钮，并设置显示的文本为text键对应的字符串值和创建一个功能为运行command键对应的字符串值并把此功能设置为点击时运行的功能
            content.grid(row=content_config["grid"]["r"], column=content_config["grid"]["c"]) #设置创建的元素的表格位置
            self.contents.append(content) #把创建的元素添加进内容列表里
            index += 1 #这边才发现调试时加的这个index变量没有作用但是作者忘记删了

    def __init__(self, config_path: str): #应用启动器类的构造函数，用于加载配置和创建窗口实例
        config: dict = LoadJsonConfig(config_path) #读取json配置文件并解析为字典
        if not config: #判断字典是否是空字典
            exitcode = 1 #如果是空字典把退出码改为1
            print("错误：配置文件丢失或为空")
            EXITHISWINDOW() #调用用于退出程序的函数
        self.contents: list = [] #添加的元素的列表
        self.window = ctk.CTk() #创建主窗口实例
        self.LoadUnitConfig(config) #加载基本配置
        self.LoadContent(config) #创建和加载元素配置
        
    def main(self, args: list[str]): #主函数，接收命令行参数(尽管并没做什么功能)
        self.window.mainloop() #窗口主循环

if __name__ == "__main__": #判断是不是以当前文件为入口文件执行，防止代码是被其他python文件import时执行
    AppLaucher("./config.json").main(sys.argv) #创建启动器类实例并带上命令行参数运行
