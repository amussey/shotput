from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer
import logging
import os
import paramiko
import pync
import pyperclip
import random
import string
import sys
import time


# setup logging
# paramiko.util.log_to_file("demo_sftp.log")

# Paramiko client configuration
UseGSSAPI = True  # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True
Port = 22


PRIVATE_KEY = ''
HOSTNAME = ''
USERNAME = ''
PASSWORD = ''
SERVER_PATH = ''
WATCH_DIRECTORY = ''
BASE_URL = ''


def random_alphanum_str(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Uploader(LoggingEventHandler):

    # def __init__(self),

    def _load_hostkey(self):
        # get host key, if we know one
        hostkeytype = None
        hostkey = None
        try:
            host_keys = paramiko.util.load_host_keys(
                os.path.expanduser("~/.ssh/known_hosts")
            )
        except IOError:
            try:
                # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
                host_keys = paramiko.util.load_host_keys(
                    os.path.expanduser("~/ssh/known_hosts")
                )
            except IOError:
                print("*** Unable to open host keys file")
                host_keys = {}

        if HOSTNAME in host_keys:
            hostkeytype = host_keys[HOSTNAME].keys()[0]
            hostkey = host_keys[HOSTNAME][hostkeytype]
            print("Using host key of type %s" % hostkeytype)


    def _put_to_ssh(self, filename):
        try:
            t = paramiko.Transport((HOSTNAME, 22))
            t.connect(
                self._load_hostkey(),
                username=USERNAME,
                password=PASSWORD,
            )
            sftp = paramiko.SFTPClient.from_transport(t)

            # dirlist on remote host
            dirlist = sftp.listdir(SERVER_PATH)
            print("Dirlist: %s" % dirlist)

            new_filename = '{}.png'.format(random_alphanum_str(6))
            while new_filename in dirlist:
                new_filename = '{}.png'.format(random_alphanum_str(6))

            sftp.put(filename, "{}{}".format(SERVER_PATH, new_filename))
            sftp.close()
            t.close()
        except Exception as e:
            print(e)

        print(new_filename)

        return new_filename

    def do_push(self, filename):
        filename = self._put_to_ssh(filename)

        url = '{}{}'.format(BASE_URL, filename)
        pyperclip.copy(url)
        print(url)

        pync.notify('Screenshot Uploader', title=url)


    def on_moved(self, event):
        super(Uploader, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

        if what == 'file' and event.dest_path[-4:] == '.png':
            filename = self.do_push(event.dest_path)


    def on_created(self, event):
        super(Uploader, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

        if what == 'file' and event.src_path[-4:] == '.png':
            filename = self.do_push(event.src_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else WATCH_DIRECTORY  # '.'
    event_handler = Uploader()  # LoggingEventHandler()

    # event_handler._put_to_ssh('./cool.png')
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
