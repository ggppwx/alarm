import sys
import argparse
import ConfigParser
import schedule
import time
import daemon

def job():
    print('im doing this shit')



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

    for key, value in config.items('time'):
        print value
        # adding system alarm
        schedule.every().day.at(value).do(job)

    while 1:
        schedule.run_pending()
        time.sleep(1) #one sec


if __name__ == "__main__":
    with daemon.DaemonContext(
            working_directory='./',
            stdout=sys.stdout,
            stderr=sys.stderr):
        main()
