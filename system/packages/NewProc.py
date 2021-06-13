import sys
import subprocess
import PyQt5.Qt
import psutil
import posix

child_processes = []


def open_file_as_process(file: str):
    if __check_is_application(file):
        # return other_open(file)
        return __openApp(file)
        #return __openAnother(file)
    else:
        # other_open(file)
        return __openAnother(file)


def __openApp(files: str):
    return __open_new_process(files)


def __open_new_process(file: str):
    # proc = psutil.Popen(["chmod", "+x", file])
    try:
        proc = subprocess.Popen([file])
        print(proc.stdout)
        # if "No application is registered as handling this file" in proc.stdout:
        #    return -1
        child_processes.append(proc)
        return proc.pid
    except:
        return -1


def __openAnother(_path: str):
    return 0

def other_open(file: str):
    # PyQt5.Qt.QDesktopServices.openUrl(PyQt5.Qt.QUrl.fromLocalFile(file))
    # return 0

    opener = "open" if sys.platform == "darwin" else "xdg-open"

    output = subprocess.getoutput([opener, file])
    print(output)
    if "No application is registered as handling this file" in output:
        return -1

    proc = subprocess.Popen([opener, file])
    return proc.pid

    def __get_file_name(path: str):
        exist = path.rfind('/')
        if exist:
            return path[path.rfind('/') + 1:]

    for pid in psutil.pids():
        proc_cmd_lines: str = psutil.Process(pid).cmdline()
        for line in proc_cmd_lines:
            if line.rfind(__get_file_name(file)) >= 0:
                print(psutil.Process(pid).name())
                return pid
    print("process didn't founded")
    return -1


def __check_is_application(path):

   # st = subprocess.check_output("file  --mime-type '{}' ".format(path), stderr=subprocess.STDOUT,
    #                             universal_newlines=True, shell=True)
    # if "application/x" in st:

   #
    st = subprocess.getoutput(subprocess.check_output("file  --mime-type '{}' ".format(path), stderr=subprocess.STDOUT,
                                 universal_newlines=True, shell=True))
    if st.find("/x", 0) > -1:
        print(path, "is an application")
        return True
    else:
        return False
