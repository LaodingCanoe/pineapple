import threading
import multiprocessing
import customtkinter
import pyttsx3
import mttkinter
import pytube.helpers
import gosha_voice as voice
import tkinter
from PIL import Image
from math import ceil
from threading import Thread
import comand
import words
from pytube import YouTube
from pytube import Stream
import requests as r
from tkinter import filedialog as fd
import re


class Yotube_window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("700x450")
        self.resizable(False, False)
        self.title("Скачать видео Youtube")
        self.iconbitmap(r'icon.ico')

        def check_button():
            try:
                URL = self.link.get("1.0", 'end')
                video = YouTube(URL)
                self.info_name.delete("1.0", 'end')
                self.info_name.insert('end', text=video.title)
                self.info_textbox.delete("1.0", 'end')

                full_html = r.get(URL).text
                y = re.search(r'shortDescription":"', full_html)
                desc = ""

                count = y.start() + 19
                while True:
                    letter = full_html[count]
                    if letter == "\"":
                        if full_html[count - 1] == "\\":
                            desc += letter
                            count += 1
                        else:
                            break
                    else:
                        desc += letter
                        count += 1
                self.info_textbox.insert('end', text=desc)
                img = r.get(video.thumbnail_url, stream=True).raw
                self.my_image = customtkinter.CTkImage(dark_image=Image.open(img), size=(320, 180))
                self.image_label.configure(info_frame, image=self.my_image)
                self.image_label.image = self.my_image
            except:
                pass

        def save():
            try:
                check_button()
                URL = self.link.get("1.0", 'end')
                file = self.save_tb.get("1.0", 'end')
                file = file.replace("\n", '')
                video = YouTube(URL)
                stream = video.streams.get_by_itag(22)
                stream.download(output_path=file)
                self.progressbar.set(1)
            except:
                pass

        def select_button():
            name = fd.askdirectory()
            self.save_tb.delete("1.0", 'end')
            self.save_tb.insert('end', text=name)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        link_frame = customtkinter.CTkFrame(master=self, width=650, height=50)
        link_frame.grid(row=1, column=1, padx=0, sticky="new", pady=(0, 0))

        self.text_link = customtkinter.CTkLabel(link_frame, text="Ссылка")
        self.link = customtkinter.CTkTextbox(link_frame, width=500, height=26.5, fg_color="#1E1F22")
        self.button_check = customtkinter.CTkButton(link_frame, text='Проверить', width=60, height=30, command=check_button)
        self.text_link.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="nw")
        self.link.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="n")
        self.button_check.grid(row=0, column=2, pady=(10, 0), padx=10, sticky="ne")

        info_frame = customtkinter.CTkFrame(master=self)
        info_frame.grid(row=1, column=1, padx=0, sticky="ew", pady=(0, 0), columnspan=2, rowspan=2)
        self.image_label = customtkinter.CTkLabel(info_frame, text="")
        self.info_textbox = customtkinter.CTkTextbox(master=info_frame, width=350, height=180,
                                              font=('Helvetica', 15),
                                              fg_color="#32353A", wrap='word')
        self.info_name = customtkinter.CTkTextbox(master=info_frame, width=690, height=26.5,
                                              font=('Helvetica', 15),
                                              fg_color="#32353A", wrap='word')
        self.info_name.grid(row=1, column=1, sticky="n", padx=(0, 0), pady=(5, 10), columnspan=2, rowspan=2)
        self.info_textbox.grid(row=3, column=2, sticky="se", padx=(20, 5))
        self.image_label.grid(row=3, column=1, sticky="sw", padx=(5, 0))

        progres_frame = customtkinter.CTkFrame(master=self)
        progres_frame.grid(row=2, column=1, padx=0, sticky="sew", pady=(0, 0), columnspan=2, rowspan=2)

        self.save_lb = customtkinter.CTkLabel(progres_frame, text='Сохранить в')
        self.save_tb = customtkinter.CTkTextbox(progres_frame, width=515, height=30)
        self.button_select = customtkinter.CTkButton(master=progres_frame, text='выбрать', width=60, height=30, command=select_button)
        self.save_lb.grid(row=1, column=0, pady=(20, 0), padx=(10, 20), sticky="nw", columnspan=2, rowspan=2)
        self.save_tb.grid(row=1, column=2, pady=(20, 0), padx=0, sticky="nw", columnspan=2, rowspan=2)
        self.button_select.grid(row=1, column=3, pady=(20, 0), padx=10, sticky="ne", columnspan=2, rowspan=2)

        self.progressbar = customtkinter.CTkProgressBar(progres_frame, orientation="horizontal", width=515, height=30)
        self.button_safe = customtkinter.CTkButton(master=progres_frame, text='скачать', width=60, height=30,
                                                   command=save)
        self.progressbar.grid(row=3, column=2, pady=(20, 5), padx=0, sticky="sw", columnspan=1, rowspan=1)
        self.button_safe.grid(row=3, column=3, pady=(20, 5), padx=10, sticky="se")

        self.progressbar.set(0)


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.geometry("400x650")
        self.resizable(False, False)
        self.title("Gosha Beta2")
        self.iconbitmap(r'icon.ico')
        customtkinter.set_appearance_mode("dark")

        def youtube_save():
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = Yotube_window(self)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it


        def talk(comands):
            try:
                engine = pyttsx3.init()
                comands = (list(word for word in comands.split() if not word.startswith("http")))
                comands = " ".join(comands)
                engine.say(comands)
                engine.runAndWait()
            except:
                pass

        def clear():
            for widget in tk_label_frame.winfo_children():
                widget.destroy()

        def change(event):
            button.configure(image=image_ico)

        def button_function():
            Obj['run'] = not Obj['run']
            while Obj['run']:
                button.configure(image=image_lisens)
                text = voice.listen()
                text_len = len(text)
                if text_len == 0:
                    continue
                text_round = int(ceil(text_len / 40))
                tk_textbox = customtkinter.CTkTextbox(master=tk_label_frame, width=350, height=26.5 * text_round,
                                                      font=('Helvetica', 15),
                                                      fg_color="#32353A", wrap='word')
                tk_textbox.pack(padx=(10, 0), pady=(5, 0), anchor="nw")
                tk_textbox.insert('end', text=text)
                button.bind('<Button-1>', change)
                text = comand.recognize(text, words.data_set)
                if text == 1:
                    button.configure(image=image_ico)
                    break
                elif text == 2:
                    youtube_save()
                    button.configure(image=image_ico)
                    break
                elif text != None:
                    text_len = len(text)
                    text_round = int(ceil(text_len / 40))
                    tk_textbox = customtkinter.CTkTextbox(master=tk_label_frame, width=350, height=25.5 * text_round,
                                                          font=('Helvetica', 15),
                                                          fg_color="#32353A", wrap='word')
                    tk_textbox.pack(padx=(10, 0), pady=(5, 0), anchor="ne")
                    tk_textbox.insert('end', text=text)
                    button.bind('<Button-1>', change)
                    talk(text)

        image_ico = customtkinter.CTkImage(light_image=Image.open("icon.png"),
                                           dark_image=Image.open("icon.png"),
                                           size=(75, 75))

        image_gear = customtkinter.CTkImage(light_image=Image.open("gear.png"),
                                            dark_image=Image.open("gear.png"),
                                            size=(60, 60))

        image_clear = customtkinter.CTkImage(light_image=Image.open("clear.png"),
                                             dark_image=Image.open("clear.png"),
                                             size=(60, 60))

        image_lisens = customtkinter.CTkImage(light_image=Image.open("lisen.png"),
                                             dark_image=Image.open("lisen.png"),
                                             size=(75, 75))

        button_frame = customtkinter.CTkFrame(master=self)
        button_frame.grid(row=3, column=1, pady=(0,0), padx=0, sticky="sew", columnspan=2)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        tk_label_frame = customtkinter.CTkScrollableFrame(master=self, fg_color="#1E1F22")
        tk_label_frame.grid(row=0, column=1, padx=0, sticky="nsew", pady=(0, 0), columnspan=2,rowspan=2)

        Obj = dict(run=False)

        button = customtkinter.CTkButton(master=button_frame, text='',  image=image_ico, width=60, height=60, fg_color="#2B2B2B",
                                         command=lambda: Thread(target=button_function).start())
        button.configure(image=image_ico)
        button_1 = customtkinter.CTkButton(master=button_frame, text='', image=image_gear, width=60, height=60, fg_color="#2B2B2B")

        button_2 = customtkinter.CTkButton(master=button_frame, text='', image=image_clear, width=60, height=60,
                                           fg_color="#2B2B2B",
                                           command=clear)

        button.grid(row=1, column=2, padx=25, pady=20, sticky="s")
        button_1.grid(row=1, column=0, padx=(20,30), pady=25,  sticky="sw")
        button_2.grid(row=1, column=3, padx=(30,20), pady=25, sticky="se")

        self.toplevel_window = None


app = App()
app.mainloop()

