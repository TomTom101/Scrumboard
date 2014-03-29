import os, time
import ConfigParser

config = ConfigParser.ConfigParser()
config_file = 'settings.ini'
def_config_path = os.path.join(os.path.dirname(__file__), config_file)
#config_path = os.path.join(os.path.expanduser("~/odol"), config_file)

config.readfp(open(def_config_path))
#config.set('data', 'home_path', os.path.expanduser("~"))
#config.read(config_path)
