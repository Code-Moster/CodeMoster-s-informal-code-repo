from os import system
import sys
import customtkinter as ctk
import json

exitcode: int = 0

def makecommandfunc(command: str):
    def commandfunc():
        system(command)
    return commandfunc

def LoadJsonConfig(config_path: str) -> dict:
    res: dict
    try:
        f = open(config_path, "r", encoding="utf-8")
        config: str = f.read()
        f.close()
        res = json.loads(config)
    except FileNotFoundError:
        res = {}
    return res

def EXITHISWINDOW() -> None:
    sys.exit(exitcode)

class AppLaucher:
    def LoadUnitConfig(self, config: dict) -> None:
        self.window.title(config["window_title"])
        self.window.geometry(f"{config["window_size"][0]}x{config["window_size"][1]}")
        ctk.set_default_color_theme(config["window_default_color_theme"])
        
    def LoadContent(self, config: dict) -> None:
        index: int = 0
        for content_config in config["content"]:
            content: ctk.CTkEntry | ctk.CTkButton
            if content_config["command"] == "ENTER":
                content = ctk.CTkEntry(self.window, width=content_config["width"])
            elif content_config["command"] == "EXITHISWINDOW":
                content = ctk.CTkButton(self.window, text=content_config["text"], command=EXITHISWINDOW)
            else:
                content = ctk.CTkButton(self.window, text=content_config["text"], command=makecommandfunc(content_config["command"]))
            content.grid(row=content_config["grid"]["r"], column=content_config["grid"]["c"])
            self.contents.append(content)
            index += 1

    def __init__(self, config_path: str):
        config: dict = LoadJsonConfig(config_path)
        if not config:
            exitcode = 1
            print("错误：配置文件丢失或为空")
            EXITHISWINDOW()
        self.contents: list = []
        self.window = ctk.CTk()
        self.LoadUnitConfig(config)
        self.LoadContent(config)
        
    def main(self, args: list[str]):
        self.window.mainloop()

if __name__ == "__main__":
    AppLaucher("./config.json").main(sys.argv)