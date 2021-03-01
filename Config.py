import configparser
import os


class Config:
    def __init__(self):
        super().__init__()
        self.path = "config.ini"

    def get_config(self):
        if not os.path.exists(self.path):
            self.create_config()

        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read(self.path, encoding='windows-1251')
        return config

    def get_setting(self, section, setting):
        config = self.get_config()
        value = config.get(section, setting)
        return value


class ConfigGetter:
    def __init__(self):
        conf = Config()
        self.cameraIp = conf.get_setting("CAMERA", "CameraIp")
        self.cameraLogin = conf.get_setting("CAMERA", "CameraLogin")
        self.cameraPassword = conf.get_setting("CAMERA", "CameraPassword")
        self.cameraArguments = conf.get_setting("CAMERA", "CameraArguments")
