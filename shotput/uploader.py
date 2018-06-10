from watchdog.events import LoggingEventHandler
import logging
import os
import paramiko
import pyperclip
import random
import rumps
import string


def random_alphanum_str(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Uploader(LoggingEventHandler):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def load_hostkey(self):
        # get host key, if we know one
        hostkeytype = None
        hostkey = None
        hostname = self.config.hostname
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
                return

        if hostname in host_keys:
            hostkeytype = host_keys[hostname].keys()[0]
            hostkey = host_keys[hostname][hostkeytype]
            print("Using host key of type %s" % hostkeytype)

        return hostkey

    def put(self, filename):
        hostname = self.config.hostname
        print(self.config.__dict__)

        try:
            t = paramiko.Transport((hostname, 22))
            t.connect(
                self.load_hostkey(),
                username=self.config.username,
                password=self.config.password,
            )
            sftp = paramiko.SFTPClient.from_transport(t)
        except Exception as e:
            print('Problem connecting: ', e)
            return None

        try:
            # dirlist on remote host
            dirlist = sftp.listdir(self.config.server_path)
        except Exception as e:
            print('Path {} not found on the server.  (error: {})'.format(self.config.server_path, e))
            return None

        try:
            print("Dirlist: %s" % dirlist)

            new_filename = '{}.png'.format(random_alphanum_str(6))
            while new_filename in dirlist:
                new_filename = '{}.png'.format(random_alphanum_str(6))

            sftp.put(filename, "{}/{}".format(self.config.server_path, new_filename))
            sftp.close()
            t.close()
        except Exception as e:
            print(e)

        return new_filename

    def do_push(self, filename):
        filename = self.put(filename)

        if filename is not None:
            url = '{}{}'.format(self.config.web_url, filename)
            pyperclip.copy(url)

            rumps.notification(title='Shotput', subtitle=url, message='', sound=False)
        else:
            rumps.notification(title='Upload failed.', subtitle='', message='', sound=True)

    def on_moved(self, event):
        super(Uploader, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

        if what == 'file' and event.dest_path[-4:] == '.png':
            print(event.dest_path)
            self.do_push(event.dest_path)

    def on_created(self, event):
        super(Uploader, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

        if what == 'file' and event.src_path[-4:] == '.png':
            print(event.src_path)
            self.do_push(event.src_path)
