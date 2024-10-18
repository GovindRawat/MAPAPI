import configparser


def load_config():
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    return config
