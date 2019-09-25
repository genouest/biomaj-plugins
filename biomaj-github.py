import requests
import dateutil.parser
import logging

from yapsy.IPlugin import IPlugin


class BiomajGithubDownloader(IPlugin):
    '''
    Requirements: python-dateutil, Yapsy
    '''

    def configure(self, options):
        self.repo = options['repo']
        self.url = "https://api.github.com/repos/%s/releases" % (options['repo'])

    def name(self):
        return "github"

    def release(self):
        resp = requests.get(self.url)
        if not resp.status_code == 200:
            raise Exception('Failed to get release from GitHub')
        github_releases = resp.json()
        if len(github_releases) == 0:
            return None
        release = None
        releases = []
        for rel in github_releases:
            name = rel['tag_name']
            if rel['name'] is not None:
                name = rel['name']
            releases.append({'id': rel['id'], 'name': name, 'published': dateutil.parser.parse(rel['published_at'])})
        releases.sort(key=lambda x: x['published'], reverse=True)
        logging.debug("Releases: %s" % (str(releases)))
        return releases[0]['name']

    def list(self, release_name=None):
        logging.info('Plugin:GitHub:Release:%s' % (str(release_name)))
        if not release_name:
            logging.error('No release provided')
            return []
        resp = requests.get(self.url)
        if not resp.status_code == 200:
            raise Exception('Failed to list release files from GitHub')
        github_releases = resp.json()
        if len(github_releases) == 0:
            return None
        release = None
        for rel in github_releases:
            if rel['name'] == release_name or rel['tag_name'] == release_name:
                release = rel
                break
        if release is None:
            raise Exception('Failed to list release files from GitHub')
        remote_files = []
        
        for asset in release['assets']:
            asset_update = dateutil.parser.parse(asset['updated_at'])
            remote_files.append({
                'name': '/%s/releases/download/%s/%s' % (self.repo, rel['tag_name'], asset['name']),
                'save_as': asset['name'],
                'permissions': '',
                'group': '',
                'size': asset['size'],
                'year': asset_update.year,
                'month': asset_update.month,
                'day': asset_update.day,
                'hash': None
            })
        logging.info(remote_files)
        return remote_files


#test = BiomajGithubDownloader()
#test.configure({'repo': 'osallou/goterra-cli'})
#test.release()
#files = test.list()
#print("=> %s" % (str(files)))
