from collections import OrderedDict
import configparser
import subprocess
import os


DEFAULT_CONFIG = OrderedDict(
    username="your_sftp_username",
    password="your_sftp_password",
    hostname="yoursite.com",
    port="22",
    server_path="/where/on/the/server/to/store/things",
    web_url="http://website.to/prepend",
)


class Config(object):
    def __init__(self):
        self.config_path = os.path.join(os.path.expanduser("~"), '.shotput.conf')

        self.warnings = {}

        verify = True
        if not os.path.isfile(self.config_path):
            self.write_default_config()
            self.open()
            verify = False

        self.load(verify)

    def write_default_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = DEFAULT_CONFIG

        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def open(self):
        subprocess.call(['open', '-a', 'TextEdit', self.config_path])

    def load(self, verify=True):
        config_ini = configparser.ConfigParser()
        config_ini.read(self.config_path)

        config = {}
        for section in config_ini:
            config.update(dict(config_ini[section]))

        self.username = config.get('username')
        self.password = config.get('password')
        self.hostname = config.get('hostname')
        self.port = config.get('port', 22)
        self.server_path = config.get('server_path')
        self.web_url = config.get('web_url')

        for field in DEFAULT_CONFIG:
            if getattr(self, field) is None:
                self.warnings[field] = 'not set'
            elif getattr(self, field) == DEFAULT_CONFIG[field]:
                if field != 'port':
                    self.warnings[field] = 'still set to the default setting'
            else:
                if field in self.warnings:
                    del(self.warnings[field])

        self.load_screenshot_location()

    def load_screenshot_location(self):
        try:
            self.watch_dir = subprocess.check_output(['defaults', 'read', 'com.apple.screencapture', 'location'])
            self.watch_dir = self.watch_dir.decode()
        except subprocess.CalledProcessError:
            self.watch_dir = os.path.expanduser("~/Desktop")

        self.watch_dir = self.watch_dir.strip()
