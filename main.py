from tkinter import filedialog
from appWindow import AppWindow
import tkinter as tk
from PIL import ImageTk, Image
from functools import partial
import os


class MovingImage:
    def __init__(self, main_window, img_path):
        super().__init__()
        self.main_window = main_window
        self.base_img = Image.open("BlankImage.png")
        self.base_img = self.base_img.convert("RGBA")
        self.base_img = self.base_img.resize((512, 512))
        self.img = Image.open(img_path)
        self.img = self.img.convert("RGBA")
        self.cassette_overlay = Image.open("CustomCassetteTemplate.png")
        self.pos_x = 0
        self.pos_y = 0
        self.scale = 1
        self.rotation = 0
        self.num_image = 1

    def update_image(self, adding_second_img=False):
        temp_base = self.base_img.copy()
        temp_img = self.img.copy()
        temp_img = temp_img.resize((int(temp_img.width * self.scale), int(temp_img.height * self.scale)))
        temp_img = temp_img.rotate(self.rotation)
        temp_base.paste(temp_img, (self.pos_x, self.pos_y), temp_img)
        if adding_second_img:
            self.base_img = temp_base.copy()
        temp_base.paste(self.cassette_overlay, (0, 0), self.cassette_overlay)
        self.main_window.make_image_from_obj(temp_base, 500, 300)
        return temp_base


    def resize(self, rate: float):
        if int(self.img.width * (self.scale * rate)) > 0 or int(self.img.height * (self.scale * rate)) > 0:
            self.scale *= rate
        self.update_image()

    def rotate(self, angle: int):
        self.rotation += angle
        self.update_image()

    def move(self, direction: str, amount=1):
        if direction.lower() == "left":
            self.pos_x -= amount
        if direction.lower() == "right":
            self.pos_x += amount
        if direction.lower() == "up":
            self.pos_y -= amount
        if direction.lower() == "down":
            self.pos_y += amount
        self.update_image()

    def reset(self):
        self.pos_x = 0
        self.pos_y = 0
        self.scale = 1
        self.rotation = 0
        self.update_image()

    def finished(self):
        try:
            final_img_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("Image file", "*.png")],
                                                          initialdir=(os.path.expanduser("~") + "\\AppData\\LocalLow\\Inzanity\\ROBOBEAT\\cassettes\\cassette_visuals"))
        except:
            final_img_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                          filetypes=[("Image file", "*.png")])
        if final_img_path:
            final_img = self.update_image()
            final_img.save(final_img_path)
            self.main_window.destroy_children()
            self.main_window.make_text("File Saved!", 500, 400)



    def add_second_img(self):
        if self.num_image < 2:
            new_img_path = filedialog.askopenfilename(filetypes=[('Allowed Types', '*.png *.jpeg *.jpg')])
            if new_img_path:
                self.num_image += 1
                self.update_image(True)
                self.reset()
                self.img = Image.open(new_img_path)
                self.img = self.img.convert("RGBA")
                self.update_image()




def select_file(window, making_second_image=False):
    img_path = filedialog.askopenfilename(filetypes=[('Allowed Types', '*.png *.jpeg *.jpg')])
    if img_path:
        window.destroy_children()
        moving_img = MovingImage(window, img_path)
        moving_img.update_image()
        main_editor(window, moving_img)

def main_editor(window, moving_img):
    window.make_button("Bigger", partial(moving_img.resize, 1.1), 500, 600)
    window.make_button("Bigger (Precise)", partial(moving_img.resize, 1.01), 650, 600)

    window.make_button("Smaller", partial(moving_img.resize, 0.9), 500, 650)
    window.make_button("Smaller (Precise)", partial(moving_img.resize, 0.99), 650, 650)

    window.make_button("Rotate", partial(moving_img.rotate, 90), 500, 700)

    window.make_text("Normal Movement", 150, 600)
    window.make_button("Up", partial(moving_img.move, "up", 10), 150, 650)
    window.make_button("Down", partial(moving_img.move, "down", 10), 150, 750)
    window.make_button("Left", partial(moving_img.move, "left", 10), 100, 700)
    window.make_button("Right", partial(moving_img.move, "right", 10), 200, 700)

    window.make_text("Precise Movement", 350, 600)
    window.make_button("Up", partial(moving_img.move, "up"), 350, 650)
    window.make_button("Down", partial(moving_img.move, "down"), 350, 750)
    window.make_button("Left", partial(moving_img.move, "left"), 300, 700)
    window.make_button("Right", partial(moving_img.move, "right"), 400, 700)

    window.make_button("Finished", partial(moving_img.finished), 850, 600)

    window.make_button("Add Second Image", partial(moving_img.add_second_img), 850, 650)


if __name__ == '__main__':
    newWindow = AppWindow(1000, 800)
    newWindow.make_image("CassetteImageMakerIcon.png", 500, 65)
    newWindow.make_text("Easy Cassette Image Maker for ROBOBEAT", 500, 25)
    newWindow.make_button("Select File", partial(select_file, newWindow), 500, 300)
    tk.mainloop()