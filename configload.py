import configparser

def getConfigSetting(type, name):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[type][name]