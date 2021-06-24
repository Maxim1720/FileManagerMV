import ctypes
import multiprocessing
import os
import threading
import time
import tkinter as tk
from threading import Thread

import posix_ipc
import psutil
from PyQt5.QtCore import QSharedMemory, QBuffer, QDataStream, QSystemSemaphore, QThread


class VideoEdu:

    def __init__(self, master, window):
        from multiprocessing import shared_memory as shmemory
        self.master = master
        self.grid_ = self.add_grid(master, 8, 2)
        self.mainwindow = window
        self.path_value = tk.StringVar()
        self.path_value.set(os.getcwd() + '\IMG_0761.MP4')

        self.username = ""
        self.cpu_digits = []

        self.username_sem = posix_ipc.Semaphore("user_name_sem")

        def usernameUPD():

            self.username_sem.acquire()

            shmem_list = shmemory.ShareableList(name='user_name')
            self.username = shmem_list[0]
            shmem_list.shm.close()
            #shmem_list.shm.unlink()
            del shmem_list

            self.username_sem.release()

        curproc = multiprocessing.process.current_process()

        def cpu_persents_set():
            shmem = QSharedMemory('cpu')
            shmem.attach()
            print("inter>update_cpu_digits: ", shmem.errorString())
            def update():
                while curproc.is_alive():
                    shmem.lock()
#                    c_buf = ctypes.c_wchar_p(shmem.data().__int__())
#                    if self.cpu_digits:
#                        self.cpu_digits.append(c_buf.value)
                    shmem.unlock()
            t = threading.Thread(target=update)
            t.daemon = True
            t.start()

        def updating():
            while True:
                usernameUPD()
                QThread.sleep(1)

        thread = threading.Thread(target=updating)
        thread.daemon = True
        thread.start()


        self.cpu_percents = psutil.cpu_percent(0, True)[:]

        self.about_mainInfo = tk.Label(self.grid_[1][0],
                                       text="""Kursovoy FileManager\n0.1a""",
                                       font=('Courier', '17', 'bold'))
        self.about_mainInfo.pack(side=tk.TOP, padx=25)

        self.created = tk.Label(self.grid_[1][0], text="created by Musiev Maxim\n\n©2021 PSUTI",
                                font=('Courier', '10'))
        self.created.pack(side=tk.RIGHT, padx=0)

        self.username_label = tk.Label(self.grid_[2][0],
                                       text=f'Username: "{self.username}"',
                                       font=('Console', '14'))
        self.username_label.pack(side=tk.LEFT, padx=10)

        self.cpu_percents_label = tk.Label(self.grid_[4][0],
                                           text=f'cpu percents: ',
                                           font=('Courier', '15'))

        self.cpu_percents_label.pack(side=tk.LEFT, padx=10)

        self.cpu_percents_digits = tk.Label(self.grid_[4][0],
                                            text=f'',
                                            font=('Courier', '15'))
        self.cpu_percents_digits.pack(side=tk.LEFT, padx=10)

        self.configure_main_window()

        self.update_percents()


    def update_username(self):
        self.username_label.config(text=f'Username: "{self.username}"')
        self.username_label.after(110, self.update_username)

    def update_percents(self):
        percents = psutil.cpu_percent(0.5, True)
        str = ""
        for i, cpu in enumerate(percents):
            str += (f'cpu[{i+1}]={cpu:4.1f}%\n')
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



