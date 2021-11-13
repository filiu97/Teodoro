
import os
from pathlib import Path

from tkinter import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


class GUI():

    _init_already = False

    def __init__(self):
        if not GUI._init_already:
            GUI._init_already = True

            self.window = Tk()
            self.window.geometry("1024x768")
            self.window.configure(bg = "#00D1FF")


            canvas = Canvas(
                self.window,
                bg = "#00D1FF",
                height = 768,
                width = 1024,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )

            canvas.place(x = 0, y = 0)
            canvas.create_text(
                53.0,
                62.0,
                anchor="nw",
                text="     Teodoro\nPersonal Assistant",
                fill="#000",
                font=("Lobster-Regular", int(32.0))
            )

            canvas.create_rectangle(
                477.0,
                0.0,
                1024.0,
                224.0,
                fill="#C1E1FF",
                outline="")

            entry_image_1 = PhotoImage(
                file=self.relative_to_assets("entry_1.png")
            )
            entry_bg_1 = canvas.create_image(
                832.0,
                62.0,
                image=entry_image_1
            )
            self.entry_1 = Entry(
                bd=0,
                bg="#FBFBFB",
                highlightthickness=0
            )
            self.entry_1.place(
                x=672.0,
                y=34.0,
                width=320.0,
                height=54.0
            )

            canvas.create_text(
                527.0,
                48.0,
                anchor="nw",
                text="Estado : ",
                fill="#000",
                font=("Limelight-Regular", int(24.0))
            )

            canvas.create_text(
                515.0,
                140.0,
                anchor="nw",
                text="Ha dicho :",
                fill="#000",
                font=("Limelight-Regular", int(24.0))
            )

            entry_image_2 = PhotoImage(
                file=self.relative_to_assets("entry_2.png")
            )
            entry_bg_2 = canvas.create_image(
                832.0,
                154.0,
                image=entry_image_2
            )
            self.entry_2 = Entry(
                bd=0,
                bg="#FBFBFB",
                highlightthickness=0
            )
            self.entry_2.place(
                x=672.0,
                y=126.0,
                width=320.0,
                height=54.0
            )

            entry_image_3 = PhotoImage(
                file=self.relative_to_assets("entry_3.png")
            )
            entry_bg_3 = canvas.create_image(
                527.0,
                480.5,
                image=entry_image_3
            )
            self.entry_3 = Entry(
                bd=0,
                bg="#FCFCFF",
                highlightthickness=0
            )
            self.entry_3.place(
                x=161.0,
                y=273.0,
                width=732.0,
                height=413.0
            )
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)
