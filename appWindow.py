import tkinter as tk
from PIL import Image, ImageTk, ImageFile
from ctypes import windll

class AppWindow:
    def __init__(self, size_x, size_y):
        super().__init__()
        windll.shcore.SetProcessDpiAwareness(1)
        self.window = tk.Tk()
        self.window.geometry(str(size_x) + "x" + str(size_y))
        self.window.title("Easy Cassette Image Maker")
        self.window.iconbitmap("CassetteImageMakerIcon.ico")
        self.window.configure(bg="#121212")
        self.window.resizable(False, False)

    def make_image_from_obj(self, image_obj: ImageFile, pos_x=0, pos_y=0, scale=1):
        image_obj = image_obj.resize((int(image_obj.width*scale), int(image_obj.height*scale)))
        image_obj = ImageTk.PhotoImage(image_obj)
        image_label = tk.Label(self.window,
                               image=image_obj,
                               bg=self.window.cget("bg"))
        image_label.image = image_obj
        image_label.place(x=pos_x, y=pos_y, anchor=tk.CENTER)
        return image_label

    def make_image(self, image_path: str, pos_x=0, pos_y=0, scale=1):
        image_obj = Image.open(image_path)
        image_obj = image_obj.resize((int(image_obj.width*scale), int(image_obj.height*scale)))
        image_obj = ImageTk.PhotoImage(image_obj)
        image_label = tk.Label(self.window,
                               image=image_obj,
                               bg=self.window.cget("bg"))
        image_label.image = image_obj
        image_label.place(x=pos_x, y=pos_y, anchor=tk.CENTER)
        return image_label

    def make_text(self, text, pos_x=0, pos_y=0):
        text_label = tk.Label(self.window,
                              text=text,
                              fg="white",
                              bg=self.window.cget("bg"))
        text_label.place(x=pos_x, y=pos_y, anchor=tk.CENTER)
        return text_label

    def make_button(self, text, command="", pos_x=0, pos_y=0):
        button = tk.Button(self.window,
                           text=text,
                           command=command,
                           fg="white",
                           bg=self.window.cget("bg"))
        button.place(x=pos_x, y=pos_y, anchor=tk.CENTER)
        return button

    # removes all items from a tkinter canvas
    # Don't take this function out of context
    def destroy_children(self):
        for child in self.window.winfo_children():
            child.destroy()