import os
import time
import tkinter as tk
from threading import Thread

class VideoEdu:
   
    def __init__(self, master):
        self.master = master
        self.grid_ = self.add_grid(master, 17, 5)

        self.path_value = tk.StringVar()
        self.path_value.set(os.getcwd() + '\IMG_0761.MP4')

        # 1 line
        self.label_video_path = tk.Label(self.grid_[0][0], text='video path', font=('Courier', '16', 'bold'))
        self.label_video_path.pack(side=tk.LEFT, padx=15)
        self.entry_video_path = tk.Entry(self.master, textvariable=self.path_value, width=40)
        self.entry_video_path.grid(row=0, column=1, columnspan=4, sticky=tk.W)        

        # 2 line
        self.label_jump_interval = tk.Label(self.grid_[1][0], text='jump interval', font=('Courier', '16', 'bold'))
        self.label_jump_interval.pack(side=tk.LEFT, padx=15)
        self.entry_jump_interval = tk.Entry(self.grid_[1][1], width=5, justify='center')
        self.entry_jump_interval.insert(0, '1.0')
        self.entry_jump_interval.pack(side=tk.LEFT)
        self.label_jump_interval_after = tk.Label(self.grid_[1][2], text='seconds', font=('Courier', '16', 'bold'))
        self.label_jump_interval_after.pack(side=tk.LEFT)   

        # 3 line
        self.label_resize = tk.Label(self.grid_[2][0], text='resize', font=('Courier', '16', 'bold'))
        self.label_resize.pack(side=tk.LEFT, padx=15)
        self.is_resized = tk.BooleanVar(value=True)      
        self.checkbox_resize = tk.Checkbutton(self.grid_[2][1], variable=self.is_resized)
        self.checkbox_resize.pack(side=tk.LEFT, padx=5) 

        # 4 line
        self.label_ssd = tk.Label(self.grid_[3][0], text='object detection', font=('Courier', '16', 'bold'))
        self.label_ssd.pack(side=tk.LEFT, padx=15)
        self.is_ssd_active = tk.BooleanVar(value=True)      
        self.checkbox_ssd = tk.Checkbutton(self.grid_[3][1], variable=self.is_ssd_active)
        self.checkbox_ssd.pack(side=tk.LEFT, padx=5)          

        # 5 line
        self.label_backward = tk.Label(self.grid_[4][0], text='backward', font=('Courier', '16', 'bold'))
        self.label_backward.pack(side=tk.LEFT, padx=15)
        self.entry_backward = tk.Entry(self.grid_[4][1], width=5, justify='center')
        self.entry_backward.insert(0, 'Z')
        self.entry_backward.pack(side=tk.LEFT)

        # 6 line
        self.label_pause = tk.Label(self.grid_[5][0], text='pause', font=('Courier', '16', 'bold'))
        self.label_pause.pack(side=tk.LEFT, padx=15)
        self.entry_pause = tk.Entry(self.grid_[5][1], width=5, justify='center')
        self.entry_pause.insert(0, 'X')
        self.entry_pause.pack(side=tk.LEFT)

        # 7 line
        self.label_forward = tk.Label(self.grid_[6][0], text='forward', font=('Courier', '16', 'bold'))
        self.label_forward.pack(side=tk.LEFT, padx=15)
        self.entry_forward = tk.Entry(self.grid_[6][1], width=5, justify='center')
        self.entry_forward.insert(0, 'C')
        self.entry_forward.pack(side=tk.LEFT)

        # 8 line
        self.label_rewind = tk.Label(self.grid_[7][0], text='rewind', font=('Courier', '16', 'bold'))
        self.label_rewind.pack(side=tk.LEFT, padx=15)
        self.entry_rewind = tk.Entry(self.grid_[7][1], width=5, justify='center')
        self.entry_rewind.insert(0, 'R')
        self.entry_rewind.pack(side=tk.LEFT)  

        # 9 line
        self.label_jump = tk.Label(self.grid_[8][0], text='jump to frame', font=('Courier', '16', 'bold'))
        self.label_jump.pack(side=tk.LEFT, padx=15)
        self.entry_jump = tk.Entry(self.grid_[8][1], width=5, justify='center')
        self.entry_jump.insert(0, 'J')
        self.entry_jump.pack(side=tk.LEFT)                 

        # 11 line
        self.label_time = tk.Label(self.grid_[10][0], text='executed in', font=('Courier', '16', 'bold'))
        self.label_time.pack(side=tk.LEFT, padx=15)
        self.label_time_value = tk.Label(
            text='-.-', font=('Courier', '16', 'bold'))
        self.label_time_value.grid(row=10, column=1, columnspan=2, sticky=tk.W)
        self.label_time_ms = tk.Label(self.grid_[10][3], text='ms', font=('Courier', '16', 'bold'))
        self.label_time_ms.pack(side=tk.LEFT, padx=15)

        # 12 line
        self.label_memory = tk.Label(self.grid_[11][0], text='memory used', font=('Courier', '16', 'bold'))
        self.label_memory.pack(side=tk.LEFT, padx=15)      
        self.label_memory_value = tk.Label(
            text='-.-', font=('Courier', '16', 'bold'))
        self.label_memory_value.grid(row=11, column=1, columnspan=2, sticky=tk.W)
        self.label_memory_mb = tk.Label(self.grid_[11][3], text='MB', font=('Courier', '16', 'bold'))
        self.label_memory_mb.pack(side=tk.LEFT, padx=15)        

        # 13 line
        self.label_fps = tk.Label(self.grid_[12][0], text='fps', font=('Courier', '16', 'bold'))
        self.label_fps.pack(side=tk.LEFT, padx=15)
        self.label_fps_value = tk.Label(
            text='-.-', font=('Courier', '16', 'bold'))
        self.label_fps_value.grid(row=12, column=1, columnspan=2, sticky=tk.W)

        # 14 line
        self.label_fps_total = tk.Label(self.grid_[13][0], text='frames total', font=('Courier', '16', 'bold'))
        self.label_fps_total.pack(side=tk.LEFT, padx=15)
        self.label_fps_total_value = tk.Label(
            text='-.-', font=('Courier', '16', 'bold'))
        self.label_fps_total_value.grid(row=13, column=1, columnspan=2, sticky=tk.W)

        # 15 line
        self.label_video_duration = tk.Label(self.grid_[14][0], text='duration', font=('Courier', '16', 'bold'))
        self.label_video_duration.pack(side=tk.LEFT, padx=15)
        self.label_video_duration_value = tk.Label(
            text='-.-', font=('Courier', '16', 'bold'))
        self.label_video_duration_value.grid(row=14, column=1, columnspan=2, sticky=tk.W)  
        self.label_video_duration_ms = tk.Label(self.grid_[14][3], text='secs', font=('Courier', '16', 'bold'))
        self.label_video_duration_ms.pack(side=tk.LEFT, padx=15)

        # 17 line
        self.button_run = tk.Button(self.master, text='Run', width=16, command=self.__run_on_click)
        self.button_run.grid(row=16, column=0, columnspan=5, pady=5)

        self.configure_main_window()

    def __run_on_click(self):
        t1 = time.perf_counter()
        t2 = time.perf_counter()

        self.label_time_value.config(text=f'{t2-t1:.3f}')
        self.label_memory_value.config(text=f'{self.vc.memory_used:.1f}')
        self.label_fps_value.config(text=f'{self.vc.fps:.3f}')
        self.label_fps_total_value.config(text=f'{self.vc.frames_total}')
        _dur = self.vc.frames_total / self.vc.fps
        self.label_video_duration_value.config(text=f'{_dur:.2f}')

        cycle = Thread(target=self.vc.main_cycle, daemon=True)
        cycle.start()

    def configure_main_window(self):
        """
        info: main window properties
        """
        self.master.title('Video Edu App')
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

