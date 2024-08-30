from tkinter import filedialog
from appWindow import AppWindow
import tkinter as tk
from PIL import Image, ImageOps, ImageGrab
from functools import partial
import os


class MovingImage:
    def __init__(self, main_window, img_path):
        super().__init__()
        self.main_window = main_window
        self.img_path = img_path
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
        self.flipped = False

    # Updates screen to user based on set variables
    def update_image(self, adding_second_img=False):
        temp_base = self.base_img.copy()
        temp_img = self.img.copy()
        temp_img = temp_img.resize((int(temp_img.width * self.scale), int(temp_img.height * self.scale)))
        temp_img = temp_img.rotate(self.rotation)
        if self.flipped:
            temp_img = ImageOps.flip(temp_img)
        temp_base.paste(temp_img, (self.pos_x, self.pos_y), temp_img)
        if adding_second_img:
            self.base_img = temp_base.copy()
        temp_base.paste(self.cassette_overlay, (0, 0), self.cassette_overlay)
        self.main_window.make_image_from_obj(temp_base, 500, 300)
        return temp_base

    # Changes the scale variable based on the input parameter and prevents the scale from reaching 0
    def resize(self, rate: float):
        if int(self.img.width * (self.scale * rate)) > 0 or int(self.img.height * (self.scale * rate)) > 0:
            self.scale *= rate
        self.update_image()

    # Changes the rotation variable based on the angle input
    def rotate(self, angle: int):
        self.rotation += angle
        self.update_image()

    # Flips over the current image
    def flip(self):
        self.flipped = not self.flipped
        self.update_image()

    # Moves the current image based on the set direction and distance to move
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

    # Resets variables in order to add a new image
    def reset(self):
        self.pos_x = 0
        self.pos_y = 0
        self.scale = 1
        self.rotation = 0
        self.update_image()

    # Asks the user for the destination of the cassette cover which attempts to default to the destination the game uses
    # Exports the image and removes the editing screen
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

    # Uses the first image for the second image and mirrors the second image
    # relative to x point 315, the center between the two cassette sides.
    def mirror(self):
        center_pos = int(315 - (self.img.width/2*self.scale))
        new_pos_x = center_pos - self.pos_x
        if new_pos_x < 0:
            new_pos_x *= -1
        else:
            new_pos_x += center_pos
        if self.num_image < 2:
            self.add_second_img(True)
            self.pos_x = new_pos_x
            print(self.pos_x)
            self.rotation += 180
            self.update_image()

    # creates a second image and merges the first image with the cassette template
    def add_second_img(self, is_mirroring=False, is_using_clipboard=False):
        new_img_path = ""
        if self.num_image < 2:
            if is_mirroring:
                new_img_path = self.img_path
            else:
                if not is_using_clipboard:
                    new_img_path = filedialog.askopenfilename(filetypes=[('Allowed Types', '*.png *.jpeg *.jpg')])
                else:
                    if not os.path.isdir("temp"):
                        os.mkdir("temp")
                    clipboard_img = ImageGrab.grabclipboard()
                    if clipboard_img is not None:
                        clipboard_img.save("temp\\clipboard.png", 'PNG')
                        new_img_path = "temp\\clipboard.png"
                        self.num_image += 1
                    else:
                        self.main_window.make_temp_message("No Image Found!", 1000, 850, 475)

            if new_img_path:
                self.num_image += 1
                self.update_image(True)
                if not is_mirroring:
                    self.reset()
                self.img = Image.open(new_img_path)
                self.img = self.img.convert("RGBA")
                self.update_image()


# Asks the user to select a file to use for an image
def select_file(window, using_clipboard=False):
    if using_clipboard:
        img_path = "temp\\clipboard.png"
    else:
        img_path = filedialog.askopenfilename(filetypes=[('Allowed Types', '*.png *.jpeg *.jpg')])
    if img_path:
        window.destroy_children()
        moving_img = MovingImage(window, img_path)
        moving_img.update_image()
        main_editor(window, moving_img)


def make_clipboard_file(window):
    if not os.path.isdir("temp"):
        os.mkdir("temp")
    img_from_clipboard = ImageGrab.grabclipboard()
    if img_from_clipboard is not None:
        img_from_clipboard.save("temp\\clipboard.png", 'PNG')
        select_file(window, True)
    else:
        window.make_temp_message("No Image Found!", 1000, 500, 475)


# layout of buttons and text that the user presses to change an image within the cassette template
def main_editor(window, moving_img):
    window.make_button("Bigger", partial(moving_img.resize, 1.1), 500, 600)
    window.make_button("Bigger (Precise)", partial(moving_img.resize, 1.01), 650, 600)

    window.make_button("Smaller", partial(moving_img.resize, 0.9), 500, 650)
    window.make_button("Smaller (Precise)", partial(moving_img.resize, 0.99), 650, 650)

    window.make_button("Rotate", partial(moving_img.rotate, 90), 500, 700)
    window.make_button("Flip", moving_img.flip, 650, 700)

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

    window.make_button("Finish", partial(moving_img.finished), 850, 550)

    window.make_button("Add 2nd Image", partial(moving_img.add_second_img), 850, 600)

    window.make_button("Add 2nd From Clipboard", partial(moving_img.add_second_img, False, True), 850, 650)

    window.make_button("Mirror 1st Image", moving_img.mirror, 850, 700)


if __name__ == '__main__':
    # Setup for the tkinter window
    newWindow = AppWindow(1000, 800)
    newWindow.make_image("CassetteImageMakerIcon.png", 500, 65)
    newWindow.make_text("Easy Cassette Image Maker for ROBOBEAT", 500, 25)
    newWindow.make_button("Select File", partial(select_file, newWindow), 500, 300)
    newWindow.make_button("Get Image From Clipboard", partial(make_clipboard_file, newWindow), 500, 400)
    tk.mainloop()
    if os.path.isfile("temp\\clipboard.png"):
        os.remove("temp\\clipboard.png")