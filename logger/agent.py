import os
import time


class Logger:
    folder = "logs"
    filename = "log"
    logfile = None
    init_string = "LOG AGENT STARTED\nLocal time: %d/%d/%d %d:%d:%d"
    log_string = "%d/%d/%d %d:%d:%d -> %s"

    def __init__(self):
        if self.folder in os.listdir():
            os.mkdir(self.folder)
            self.logfile = open("./%s/%s" % (self.folder, self.filename), 'w')
            time_params = time.localtime()
            self.logfile.write(self.init_string % self.time_format())

    def log(self, text):
        self.logfile.write(self.log_string % self.time_format() + (text,))

    def end(self):
        self.logfile.close()

    def time_format():
        time_params = time.localtime()
        return (time_params.tm_mday,
                time_params.tm_mon,
                time_params.tm_year,
                time_params.tm_hour,
                time_params.tm_min,
                time_params.tm_sec)
