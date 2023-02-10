from configparser import ConfigParser
import os

nowpath = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(nowpath, "config.ini")


def readconfig(secname="JIRA", option="JVERSION"):
    cf = ConfigParser()
    cf.read(path)
    result = cf.get(secname, option)
    return result
