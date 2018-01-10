import sys
import argparse
import ConfigParser
import schedule
import time
import daemon
import functools
import pyttsx
from playsound import playsound
from os import system

def text_to_speech(text):

    pass



class Job(object):
    def __init__(self):
        #self._engine = pyttsx.init()
        #self._engine.setProperty('rate', 80)
        #self._engine.setProperty('volume', 5)
        pass

    def run(self, text, sound):
        playsound(sound)
        #system('say {} clock'.format(text))
        #self._engine.say(text)
        #self._engine.runAndWait()


def main():
    """
    Main function of the alarm module.
    it reads the config file, make chime alarm periodically 
    """
    parser = argparse.ArgumentParser(description='Processing config file')
    parser.add_argument('-c', '--config', nargs='?', default='config.ini', help='a config file')


    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    with open(args.config) as configFile:
        config.readfp(configFile)


    job = Job()

    for key, value in config.items('time'):
        sound = 'music.mp3'
        if config.has_option('sound', key):
            sound = config.get('sound', key)

        print sound
        print value
        # adding system alarm
        schedule.every().day.at(value).do(job.run, text=str(value), sound=str(sound))

    while 1:
        schedule.run_pending()
        time.sleep(1) #one sec



def test():
    job = Job()
    job.run(text='11 clock')



if __name__ == "__main__":
    with daemon.DaemonContext(
            working_directory='./',
            stdout=sys.stdout,
            stderr=sys.stderr):
        main()
