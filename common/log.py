import datetime
from common import config

def log(event):
    now = datetime.datetime.now().strftime("%d,%m,%y %H:%M:%S")
    if config.cfg['options']['logging']['logToConsole']:
        print(f'[{now}]:{event}')
    if config.cfg['options']['logging']['logToFile']:
        with open(config.cfg['options']['logging']['logFilePath'],"a") as logFile:
            logFile.write(f'[{now}]:{event}\n')
            