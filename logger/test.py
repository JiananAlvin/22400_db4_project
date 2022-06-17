class Cooling:
    name = "cooling"
    def __init__(self,logger):
        self.logger = logger
        self.logger.log()

    
class Temp:
    name = "temp"

    def __init__(self,logger):
        self.logger = logger
        self.logger.log()


class Feed:
    name = "feed"

    def __init__(self,logger):
        self.logger = logger
        self.logger.log()


class Logger:
    def __init__(self):
        self.logfile = open("./test.txt", 'w')
        self.logfile.write("hee")
        self.logfile.close()        
    

    def log(self, name):
        self.logfile.write(self, name)
    
    

def main():
    logger = Logger()
    Cooling(logger)
    Temp(logger)
    Feed(logger)

main()