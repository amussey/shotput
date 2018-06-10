from watchdog.observers import Observer
import os
import rumps
import logging


from .config import Config
from .uploader import Uploader


rumps.debug_mode(True)


class Shotput(rumps.App):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        self.config_path = os.path.join(os.path.expanduser("~"), '.shotput.conf')
        self.observer = None

        self.config = Config()
        self.uploader = Uploader(self.config)
        # self.start_watching()

    @rumps.clicked("Reload/Verify Preferences")
    def prefs_reload(self, sender):
        self.config.load()

        if self.config.warnings != {}:
            warning_str = ""
            for item, warning in self.config.warnings.items():
                warning_str += '"{}" is {}.\n'.format(item, warning)
            rumps.alert(title='Warning!', message=warning_str)

    @rumps.clicked("Edit Preferences")
    def prefs_open(self, sender=None):
        # rumps.alert("jk! no preferences available!")
        self.config.open()

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        print(sender.state)
        sender.state = not sender.state

    @rumps.clicked("Exit Shotput")
    def exit(self, _):
        self.stop_watching()
        rumps.quit_application()

    def start_watching(self):
        self.observer = Observer()
        self.observer.schedule(self.uploader, self.config.watch_dir)
        self.observer.start()

    def stop_watching(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
