import sys
import argparse
import ConfigParser
import schedule
import time
import daemon
import functools
import os
import platform
import datetime
from playsound import playsound

from lib import Orgnode

class Org(object):
    def __init__(self, files):
        self._files = files


    def getTasks(self, date):
        tasks = []
        for f in self._files:
            nodelist = Orgnode.makelist(f)
            for n in nodelist:
                if n.Todo() != 'DONE' and n.Scheduled() == date:
                    tasks.append(n.Heading())
        return tasks


class Job(object):
    def __init__(self):
        self._system = platform.system()
        self._org = Org(['/Users/jingweigu/Dropbox/org/scratch.org'])

    def _speak(self, text):
        if self._system == 'Darwin':
            os.system('say {}'.format(text))
        else:                
            os.system('espeak -s 150 -a 200 "{}"'.format(text))

    def _report_time(self, sound ):
        playsound(sound)

    def _read_todays_org(self):
        self._speak('Todays task has: ')
        today = datetime.date.today() 
        tasks = self._org.getTasks(today)
        for task in tasks:
            self._speak(task)
            time.sleep(1.5)


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

def testOrg():
    job = Job()
    job._read_todays_org()

if __name__ == "__main__":
    testOrg()

