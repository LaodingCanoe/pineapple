import customtkinter
from pytube import YouTube
from tkinter import filedialog as fd
import requests as r
from PIL import Image
import os
from threading import Thread
import sys

API = 'AIzaSyBxEqEzDxjFYHqR_Xpi4jjCYjUMc5Z8uyc'

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        self.geometry("700x480")
        self.resizable(False, False)
        self.title("YT_save")

        def resource_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        self.iconbitmap(resource_path('icon.ico'))

        customtkinter.set_appearance_mode("dark")

        def get_video_description(video_url):
            try:
                video_id = video_url.split("=")[-1]
                url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API}"
                response = r.get(url)
                response_json = response.json()
                video_description = response_json["items"][0]["snippet"]["description"]
                self.info_textbox.insert('end', text=video_description)
            except IndexError:
                self.info_textbox.insert('end', text='Не удалось загрузить описание')

        def check_button():
            try:
                self.progress_lb.configure(text="0%")
                self.progressbar.set(0)
                URL = self.link.get("1.0", 'end')
                URL = URL.replace("\n","")
                video = YouTube(URL, use_oauth=True, allow_oauth_cache=True)
                #video.check_availability()
                self.info_name.delete("1.0", 'end')
                self.info_name.insert('end', text=video.title)
                self.info_textbox.delete("1.0", 'end')
                t1 = Thread(target=get_video_description, args=[URL])
                t1.start()
                img = r.get(video.thumbnail_url, stream=True).raw
                self.my_image = customtkinter.CTkImage(dark_image=Image.open(img), size=(320, 180))
                self.image_label.configure(info_frame, image=self.my_image)
                self.image_label.image = self.my_image
                views = "Просмотры: " + str(video.views)
                self.show_lb.configure(text=views)
                lengh = video.length
                hour = lengh // 3600
                minut = (lengh // 60) - 60 * hour
                sec = lengh % 60
                hour = str(hour); minut = str(minut); sec = str(sec)
                if len(hour) == 1:
                    hour = "0" + hour
                if len(minut) == 1:
                    minut = "0" + minut
                if len(sec) == 1:
                    sec = "0" + sec
                lengh = "Продолжительность: " + hour + ":" + minut + ":" + sec
                self.time_lb.configure(text=lengh)
                resolutions = sorted(
                    set(stream.resolution for stream in video.streams.filter(type='video', progressive=True)),
                    key=lambda s: int(s.split('p')[0])
                )
                resolutions_full = sorted(
                    set(stream.resolution for stream in video.streams.filter(type='video')),
                    key=lambda s: int(s.split('p')[0])
                )

                i, j = 0, 0
                print(resolutions_full)
                len_resolution = len(resolutions)
                len_resolution_full = len(resolutions_full)
                while j != len_resolution_full:
                    if resolutions[i] != resolutions_full[j]:
                        resolutions_full[j] = "!" + resolutions_full[j]
                        if len_resolution - 1 != i:
                            i -= 1
                    if len_resolution - 1 != i:
                        i += 1
                    j += 1
                print(resolutions_full)
                self.optionmenu.configure(values=resolutions_full)
            except IOError:
                self.info_name.insert('end', text="Проверьте подключение к интернету")

        def select_button():
            name = fd.askdirectory()
            self.save_tb.delete("1.0", 'end')
            self.save_tb.insert('end', text=name)

        def progress(streams, chunk: bytes, bytes_remaining: int):
            try:
                size = contentsize - bytes_remaining
                progres = round(float(size / contentsize), 2)
                self.progress_lb.configure(text=str(round(progres*100, 2))+"%")
                self.progressbar.set(progres)
            except IndexError:
                self.info_textbox.insert('end', text='Не удалось загрузить описание')

        def download(video_dw, file):
            i = 0
            file = video_dw.download(output_path=file)
            while True:
                try:
                    filename = os.path.splitext(file)[0]
                    os.rename(file, filename + "(" + str(i) + ")" ".mp4")
                    break
                except FileExistsError:
                    i += 1

        def ffpeg(video, video_dw, file_path, res):
            audio = video.filter(only_audio=True).first()
            audio_file = audio.download(output_path=file_path)
            video_file = video_dw.download(output_path=file_path)
            print(video_file + '\n' + audio_file)
            video_file = video_file.replace('\\', '/')
            audio_file = audio_file.replace('\\', '/')
            print(video_file + '\n' + audio_file)
            os.rename(video_file, file_path + "/video.mp4")
            os.rename(audio_file, file_path + "/audio.mp4")
            video_index = video_file.rfind('.')
            video_file = video_file[:video_index]
            print(video_file)
            video_file = video_file + '.mp4'
            video_file = video_file.replace(' ', '_')
            print(video_file)
            filename_video = file_path + "/video.mp4"
            filename_audio = file_path + "/audio.mp4"
            cmd = 'ffmpeg -i ' + filename_video + ' -i ' + filename_audio + ' -c:a copy ' + video_file
            os.system(cmd)
            os.remove(filename_video)
            os.remove(filename_audio)

        def save():
            try:
                t3 = Thread(target=check_button)
                t3.start()
                URL = self.link.get("1.0", 'end')
                file = self.save_tb.get("1.0", 'end')
                file = file.replace("\n", '')
                video = YouTube(URL, use_oauth=True, allow_oauth_cache=True, on_progress_callback=progress)
                res = self.optionmenu.get()
                video = video.streams
                #video_dw = video.filter(res=res).desc().first()
                global contentsize
                #contentsize = video_dw.filesize
                if res[0] == '!':
                    res = res[1:]
                    video_dw = video.filter(res=res).desc().first()
                    contentsize = video_dw.filesize
                    print(contentsize)
                    fftread = Thread(target=ffpeg, args=[video, video_dw, file, res])
                    fftread.start()
                else:
                    video_dw = video.filter(res=res, progressive=True).desc().first()
                    contentsize = video_dw.filesize
                    t1 = Thread(target=download, args=[video_dw, file])
                    t1.start()
            except IOError:
                self.info_name.insert('end', text="Проверьте подключение к интернету")
            except:
                self.info_name.insert('end', text="Ошибка загрузки видео")

        def file_path():
            home = os.path.expanduser('~')
            download_path = os.path.join(home, 'Downloads')
            return download_path

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        link_frame = customtkinter.CTkFrame(master=self, width=650, height=70)
        link_frame.grid(row=0, column=0, padx=0, sticky="new", pady=(0, 0), columnspan=2, rowspan=2)

        t = Thread(target=check_button)
        self.text_link = customtkinter.CTkLabel(link_frame, text="Ссылка", width=70)
        self.link = customtkinter.CTkTextbox(link_frame, width=515, height=26.5, fg_color="#1E1F22")
        self.button_check = customtkinter.CTkButton(link_frame, text='Проверить', width=70, height=30, command=t.start)
        self.text_link.grid(row=0, column=0, pady=(10, 10), padx=10, sticky="nw")
        self.link.grid(row=0, column=1, pady=(10, 0), padx=(0, 10), sticky="n")
        self.button_check.grid(row=0, column=4, pady=(10, 0), padx=(0, 0), sticky="ne", columnspan=2, rowspan=2)

        info_frame = customtkinter.CTkFrame(master=self,  width=650, height=240)
        info_frame.grid(row=1, column=1, padx=0, sticky="new", pady=(60, 0), columnspan=2, rowspan=2)
        self.image_label = customtkinter.CTkLabel(info_frame, text="")
        self.info_textbox = customtkinter.CTkTextbox(master=info_frame, width=350, height=180,
                                                     font=('Helvetica', 15),
                                                     fg_color="#32353A", wrap='word')
        self.info_name = customtkinter.CTkTextbox(master=info_frame, width=690, height=26.5,
                                                  font=('Helvetica', 15),
                                                  fg_color="#32353A", wrap='word')
        self.info_name.grid(row=1, column=1, sticky="n", padx=(5, 0), pady=(5, 10), columnspan=2, rowspan=2)
        self.info_textbox.grid(row=3, column=2, sticky="se", padx=(20, 0), pady=(0, 10))
        self.image_label.grid(row=3, column=1, sticky="sw", padx=(5, 10))

        info_kach_frame = customtkinter.CTkFrame(master=self, width=650, height=70)
        info_kach_frame.grid(row=2, column=1, padx=0, sticky="new", pady=(0, 0))
        self.show_lb = customtkinter.CTkLabel(info_kach_frame, text='Просмотры:', anchor='w', width=180)
        self.time_lb = customtkinter.CTkLabel(info_kach_frame, text='Продолжительность:', anchor='w', width=180)
        self.kach_lb = customtkinter.CTkLabel(info_kach_frame, text='Качество:', anchor='w', width=80)
        self.optionmenu = customtkinter.CTkOptionMenu(info_kach_frame, values=[''], width=100)
        self.show_lb.grid(row=1, column=0, pady=(20, 0), padx=(10, 30), sticky="w")
        self.time_lb.grid(row=1, column=2, pady=(20, 0), padx=(10, 80), sticky="n")
        self.kach_lb.grid(row=1, column=3, pady=(20, 0), padx=(10, 10), sticky="ne")
        self.optionmenu.grid(row=1, column=4, pady=(20, 0), padx=(0, 5), sticky="ne", columnspan=2)

        progres_frame = customtkinter.CTkFrame(master=self)
        progres_frame.grid(row=3, column=1, padx=0, sticky="sew", pady=(0, 0), columnspan=2, rowspan=2)

        self.save_lb = customtkinter.CTkLabel(progres_frame, text='Сохранить в')
        self.save_tb = customtkinter.CTkTextbox(progres_frame, width=515, height=30)
        self.button_select = customtkinter.CTkButton(master=progres_frame, text='выбрать', width=70, height=30, command=select_button)
        self.save_lb.grid(row=1, column=0, pady=(20, 0), padx=(10, 20), sticky="nw", columnspan=2, rowspan=2)
        self.save_tb.grid(row=1, column=2, pady=(20, 0), padx=0, sticky="nw", columnspan=2, rowspan=2)
        self.button_select.grid(row=1, column=3, pady=(20, 0), padx=10, sticky="ne", columnspan=2, rowspan=2)
        self.save_tb.insert('end', text=file_path())

        self.progress_lb = customtkinter.CTkLabel(progres_frame, text='0%', height=30)
        self.progressbar = customtkinter.CTkProgressBar(progres_frame, orientation="horizontal", width=515, height=30)
        self.button_safe = customtkinter.CTkButton(master=progres_frame, text='скачать', width=70, height=30, command=save)
        self.progress_lb.grid(row=3, column=0, pady=(20, 5), padx=(45, 20), sticky="se", columnspan=2, rowspan=2)
        self.progressbar.grid(row=3, column=2, pady=(20, 5), padx=0, sticky="s", columnspan=1, rowspan=1)
        self.button_safe.grid(row=3, column=3, pady=(20, 5), padx=10, sticky="se")
        self.progressbar.set(0)



app = App()
app.event_add('<<Paste>>', '<Control-igrave>')
app.event_add("<<Copy>>", "<Control-ntilde>")
app.mainloop()