import os, time
import ConfigParser
import scrumboard
from scrumboard import *

config = ConfigParser.ConfigParser()
config_file = 'settings.ini'
def_config_path = os.path.join(os.path.dirname(__file__), config_file)
#config_path = os.path.join(os.path.expanduser("~/odol"), config_file)

def load_config():
    global def_config_path
    config.readfp(open(def_config_path))
    config.set('config', 'home_path', os.path.expanduser("~"))
#config.read(config_path)

load_config()
