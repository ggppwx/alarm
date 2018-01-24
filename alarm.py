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
                if (n.Todo() != 'DONE'
                    and n.Scheduled() and str(n.Scheduled()) <= str(date)):
                    print n.Scheduled()
                    print n.Heading()
                    tasks.append(n.Heading())
        return tasks


class Job(object):
    def __init__(self, org_file):
        self._system = platform.system()
        self._org = Org([org_file])

    def _speak(self, text):
        if self._system == 'Darwin':
            os.system('say "{}"'.format(text))
        else:
            os.system('espeak -s 150 -a 200 "{}"'.format(text))

    def _report_time(self, sound, text):
        playsound(sound)
        self._speak(text)

    def _read_todays_org(self):
        today = datetime.date.today() 
        tasks = self._org.getTasks(today)
        if len(tasks) == 0:
            self._speak('No task today')
        else:
            self._speak('Todays task has: ')
            for task in tasks:
                self._speak(task)
                time.sleep(1.5)


    def run(self, text, sound, org):
        self._report_time(sound, text)
        time.sleep(2)
        if org:
            self._read_todays_org()


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

    org_file = config.get('setting', 'orgfile')
    job = Job(org_file)

    for key, value in config.items('time'):
        sound = 'music.mp3'
        if config.has_option('sound', key):
            sound = config.get('sound', key)

        report_org = False
        if config.has_option('org', key):
            report_org = config.getboolean('org', key)

        print sound
        print value
        # adding system alarm
        schedule.every().day.at(value).do(job.run,
                                          text=str(value),
                                          sound=str(sound),
                                          org=report_org)

    while 1:
        schedule.run_pending()
        time.sleep(1) #one sec



def test():
    job = Job('/Users/jingweigu/Dropbox/org/scratch.org')
    job._speak('11')

def testOrg():
    job = Job('/home/roygu/Dropbox/org/scratch.org')
    job._read_todays_org()

if __name__ == "__main__":
    main()
    #testOrg()

