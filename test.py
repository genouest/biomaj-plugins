import requests
import dateutil.parser
import logging
import os

from yapsy.IPlugin import IPlugin

class BiomajTestDownloader(IPlugin):

    def configure(self, options):
        self.options = options

    def name(self):
        return "test"

    def release(self):
        return "test"

    def list(self, release_name=None):
        remote_files= [{
                'name': 'hello.md',
                'save_as': 'hellosave.md',
                'permissions': '',
                'group': '',
                'size': 0,
                'year': 2019,
                'month': 9,
                'day': 1,
                'hash': None
        }]
        return remote_files

    def download(self, release_name, files_to_download, offline_dir=None):
        logging.debug('[plugin][test][download] ' + str(release_name) + ': ' + str(files_to_download))
        for f in files_to_download:
            with open(os.path.join(offline_dir, f['save_as']), 'w') as f:
                f.write('# Hello\n\n world\n')
        return True

