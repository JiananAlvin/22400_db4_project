import os
import time


class Logger:
    folder = "logs"
    filename = "log"
    logfile = None
    init_string = "LOG AGENT STARTED\nLocal time: %d/%d/%d %d:%d:%d"
    log_string = "%d/%d/%d %d:%d:%d -> %s"

    def __init__(self):
        if self.folder not in os.listdir():
            os.mkdir(self.folder)
        self.logfile = open("./%s/%s" % (self.folder, self.filename), 'w')
        self.logfile.write(self.init_string % self.time_format())

    def log(self, text):
        self.logfile.write(self.log_string % (self.time_format() + (text,)))

    def end(self):
        self.logfile.close()

    def time_format(self):
        time_params = time.localtime()
        return (time_params[2],
                time_params[1],
                time_params[0],
                time_params[3],
                time_params[4],
                time_params[5])
