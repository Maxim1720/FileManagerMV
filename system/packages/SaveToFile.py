from datetime import *
import psutil

pathToSaveLastOpenedDirs = "/home/almat/Документы/Kursach/kursovoy-os-master/system/log/lastOpenedDirs.txt"
pathToSaveProcessesData = "/home/almat/Документы/Kursach/kursovoy-os-master/system/log/Processes.txt"
pathToSaveProcessesOutput = "/home/almat/Документы/Kursach/kursovoy-os-master/system/log/Processes/output.txt"


def save_opened_dir(dirPath):
    __write_in_file(pathToSaveLastOpenedDirs, dirPath + "\n", "a")


def save_opened_process_data(pids: list):
    for pid in pids:
        _proc = psutil.Process(pid)
        _datetime = datetime.fromtimestamp(_proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        __write_in_file(pathToSaveProcessesData, "\n%s|%s" % (_proc.cmdline(), _datetime), "a")


def save_process_output(output: str):
    __write_in_file(pathToSaveProcessesOutput, output + "\n", "a")


def __write_in_file(path: str, text: str, mode: str):
    f = open(path, mode)
    f.write(text)
    f.close()


def clear_all_files():
    __write_in_file(pathToSaveLastOpenedDirs, "", "w")
    __write_in_file(pathToSaveProcessesData, "name|time", "w")
    __write_in_file(pathToSaveProcessesOutput, "", "w")

def __get_file_name(path: str):
    exist = path.rfind('/')
    if exist:
        return path[path.rfind('/') + 1:]