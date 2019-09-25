import requests
import dateutil.parser
import logging
import re
from yapsy.IPlugin import IPlugin


class BiomajUniclustDownloader(IPlugin):
    '''
    Requirements: python-dateutil, Yapsy
    '''

    def configure(self, options):
        self.regexp = None
        if 'regexp' in options:
            self.regexp = options['regexp']
        self.url = "http://gwdu111.gwdg.de/~compbiol/uniclust"

    def name(self):
        return "uniclust"

    def release(self):
        resp = requests.get('%s/current_release' % (self.url))
        if not resp.status_code == 200:
            raise Exception('Failed to get release from uniclust')
        data = resp.text
        match = re.search('href="%s"' % (self.regexp), data)
        if not match:
            logging.exception('Failed to get release from uniclust')
            raise Exception('Failed to get release from uniclust')
        release = match.group(1)
        logging.debug("Plugin:Uniclust:Release: %s" % (str(release)))
        return release

    def list(self, release_name=None):
        logging.info('Plugin:Uniclust:List:Release:%s' % (str(release_name)))
        if not release_name:
            logging.error('No release provided')
            return []
        url = '~compbiol/uniclust/%s/uniclust30_%s.tar.gz' % (release_name, release_name)

        resp = requests.head('%s/%s' % ('http://gwdu111.gwdg.de', url))
        if resp.status_code != 200:
            logging.exception('File does not seem to exists: http://gwdu111.gwdg.de/%s' % (url))
            raise Exception('Failed to find expected file')

        info = release_name.split('_')
        remote_files= [{
                'name': url,
                'save_as': 'uniclust30_%s.tar.gz' % (release_name),
                'permissions': '',
                'group': '',
                'size': int(resp.headers['Content-Length']),
                'year': int(info[0]),
                'month': int(info[1]),
                'day': 1,
                'hash': None
        }]
        logging.info('Plugin:Uniclust:Files:%s' % (str(remote_files)))
        return remote_files


#test = BiomajGithubDownloader()
#test.configure({'repo': 'osallou/goterra-cli'})
#test.release()
#files = test.list()
#print("=> %s" % (str(files)))
