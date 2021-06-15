import os
import time
import tkinter as tk
from threading import Thread

import psutil


class VideoEdu:

    def __init__(self, master):
        self.master = master
        self.grid_ = self.add_grid(master, 8, 2)

        self.path_value = tk.StringVar()
        self.path_value.set(os.getcwd() + '\IMG_0761.MP4')

        import getpass
        self.username = getpass.getuser()
        self.cpu_percents = psutil.cpu_percent(0, True)[:]

        self.about_mainInfo = tk.Label(self.grid_[1][0],
                                       text="""Kursovoy FileManager\n0.1a""",
                                       font=('Courier', '17', 'bold'))
        self.about_mainInfo.pack(side=tk.TOP, padx=25)

        self.created = tk.Label(self.grid_[1][0], text="created by Musiev Maxim\n\n©2021 PSUTI",
                                font=('Courier', '10'))
        self.created.pack(side=tk.RIGHT, padx=0)

        self.username_label = tk.Label(self.grid_[2][0],
                                       text=f'username: {self.username}',
                                       font=('Console', '13'))
        self.username_label.pack(side=tk.LEFT, padx=10)

        self.cpu_percents_label = tk.Label(self.grid_[3][0],
                                           text=f'cpu percents: ',
                                           font=('Courier', '15'))

        self.cpu_percents_label.pack(side=tk.LEFT, padx=10)

        self.cpu_percents_digits = tk.Label(self.grid_[4][0],
                                           text=f'',
                                           font=('Courier', '15'))   
        self.cpu_percents_digits.pack(side=tk.LEFT, padx=10)
        
        self.configure_main_window()

        self.update_percents()

    def update_percents(self):
        percents = psutil.cpu_percent(0, True)
        str = ""
        for cpu in percents:
            str += (f'{cpu:4.1f}\n')
        self.cpu_percents_digits.config(text=f'{str}')
        self.cpu_percents_digits.after(110, self.update_percents)


    def configure_main_window(self):
        """
        info: main window properties
        """
        self.master.title('Kursovoy')
        self.master.resizable(False, False)

    def add_grid(self, master, sizex=8, sizey=8):
        """
        info: creates a table structure on a given frame
        """
        result = list()
        for i in range(sizex):
            result.append(list())
            tk.Grid.rowconfigure(master, i, weight=0)
            for j in range(sizey):
                frame = tk.Frame(master, width=50, height=30)
                frame.grid(row=i, column=j, sticky=tk.NSEW)
                tk.Grid.columnconfigure(master, j, weight=0)
                result[i].append(frame)
        return result


if __name__ == "__main__":
    root = tk.Tk()
    im = VideoEdu(root)
    root.mainloop()
