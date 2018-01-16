import sys
import argparse
import ConfigParser
import schedule
import time
import daemon
import functools
import os
import platform
from playsound import playsound




class Job(object):
    def __init__(self):
        self._system = platform.system()

    def _speak(self, text):
        if self._system == 'Darwin':
            os.system('say {} clock'.format(text))
        else:                
            os.system('espeak -s 150 -a 200 "{} clock"'.format(text))
    
    def run(self, text, sound):
        playsound(sound)
        self._speak(text)


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
    job._speak('11')



if __name__ == "__main__":
    main()
