import os
import time
import constant


class Logger:
    folder = "logs"
    filename = "log"
    logfile = None
    init_string = "LOG AGENT STARTED\n%s\n\nLocal time: %d/%d/%d %d:%d:%d\n"
    log_string = "%d/%d/%d %02d:%02d:%02d -> %s\n"
    logfile_names = [constant.FEEDNAME_TEMP,constant.FEEDNAME_COOL_MOTOR,constant.FEEDNAME_FOOD_MOTOR,constant.FEEDNAME_LIGHTSENSOR]
    logfile_pool = {}
    def __init__(self):
        if self.folder not in os.listdir():
            os.mkdir(self.folder)

        for name in self.logfile_names:
            logfile = open("./%s/%s%s" % (self.folder, self.filename, name), 'w+')
            logfile.write(self.init_string % ((name,) + (self.time_format())))
            self.logfile = logfile
            self.logfile_pool[name] = logfile


    def log(self, text, name):
        
        print("We are logging in %s : %s" % (name,text))
        self.logfile_pool[name].write(self.log_string % (self.time_format() + (text,)))

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
