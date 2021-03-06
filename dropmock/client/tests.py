import dropbox
import requests
import datetime
import os

from django.test import TestCase

from dropmock import mock_dbx_session, mock_dbx_client

DROPBOX_CLIENT_ID_FAKE = 'p5sqcubc8ndn70x'
DROPBOX_CLIENT_SECRET_FAKE = '8a44il5xhkoize6'

class ClientTestCase(TestCase):

    @mock_dbx_session
    @mock_dbx_client
    def test01(self):
        dbx_session = dropbox.session.DropboxSession(DROPBOX_CLIENT_ID_FAKE,
                                                     DROPBOX_CLIENT_SECRET_FAKE)
        token = dbx_session.obtain_request_token()
        auth_url = dbx_session.build_authorize_url(token)
        # the url contain the token passed
        self.assertEqual(auth_url, 
                         'https://www.dropbox.com/1/oauth/authorize?'
                         'oauth_token=mh7an9dkrg59')
        oauth1_token = dbx_session.obtain_access_token()
        # assert the mocked data
        self.assertEqual(oauth1_token.key, 'ccl4li5n1q9b')
        self.assertEqual(oauth1_token.secret, '95grkd9na7hm')
        dbx_client = dropbox.client.DropboxClient(dbx_session)
        oauth2_token = dbx_client.create_oauth2_access_token()
        self.assertEqual(oauth2_token, 'ABCDEFG')
        dbx_client = dropbox.client.DropboxClient(oauth2_token)
        account_info = dbx_client.account_info()
        self.assertEqual(account_info['display_name'], 'John Doe')
        self.assertEqual(account_info['uid'], 12345678)
        self.assertEqual(account_info['country'], 'IT')
        self.assertEqual(account_info['team']['name'], 'Elastic Inc.')
        delta = dbx_client.delta()
        cursor = delta.get('cursor')
        entries = delta.get('entries')
        self.assertEqual(delta.get('has_more'), True)
        self.assertEqual(cursor, '1st')
        self.assertEqual(len(entries), 1)
        delta_entries = entries[0]
        self.assertEqual(delta_entries[0], '/photo')
        self.assertEqual(delta_entries[1]['size'], '225.4KB')
        self.assertEqual(delta_entries[1]['rev'], '35e97029684fe')
        self.assertEqual(delta_entries[1]['thumb_exists'], False)
        self.assertNotIn('contents', delta_entries)
        delta = dbx_client.delta(cursor=cursor)
        self.assertEqual(delta.get('cursor'), '2nd')
        self.assertEqual(delta.get('has_more'), False)
        # test sandbox for the user
        resp = requests.get('https://api.dropbox.com/1/metadata/sandbox/',
                            headers={'Authorization': 'Bearer {}'
                                     .format(oauth2_token)})
        self.assertEqual(resp.status_code, 200, resp.content)
        # check disable access token to disconnect session
        dbx_client.disable_access_token()
        resp = requests.get('https://api.dropbox.com/1/metadata/sandbox/',
                            headers={'Authorization': 'Bearer {}'
                                     .format(oauth2_token)})
        self.assertEqual(resp.status_code, 403, resp.content)
        # test reconnection
        dbx_client = dropbox.client.DropboxClient(dbx_session)
        oauth2_token = dbx_client.create_oauth2_access_token()
        resp = requests.get('https://api.dropbox.com/1/metadata/sandbox/',
                            headers={'Authorization': 'Bearer {}'
                                     .format(oauth2_token)})
        self.assertEqual(resp.status_code, 200, resp.content)
        dbx_client = dropbox.client.DropboxClient(oauth2_token)
        media = dbx_client.media('/photo/mypdf.pdf')
        self.assertRegexpMatches(media['url'],
                                 r'^https://dl.dropboxusercontent.com/(\d+)/view/([a-z]+)')
        self.assertEqual(media['url'], 'https://dl.dropboxusercontent.com/1/view/auto/photo/mypdf.pdf')
        self.assertIn('expires', media)
        print media['expires']
        path, _ = os.path.split(os.path.realpath(__file__))
        sample_file = open('{}/data/test.txt'\
                               .format(path), 'r')
        full_path = '/test/test.txt'
        # TODO: test using dropbox command
        resp1 = dbx_client.put_file(full_path, sample_file)
        sample_file2 = open('{}/data/test2.txt'\
                               .format(path), 'r')
        full_path2 = '/test/test2.txt'
        resp2 = dbx_client.put_file(full_path2, sample_file2)
        self.assertNotEqual(resp1, resp2)
        # new_file = dbx_client.get_file(full_path)
        # self.assertEqual(sample_file.read(), new_file.read())
        resp3 = dbx_client.file_delete(full_path)
        self.assertFalse(resp1['is_deleted'])
        self.assertTrue(resp3['is_deleted'])
        resp1.pop('is_deleted')
        resp3.pop('is_deleted')
        self.assertEqual(resp3, resp1)
        move_to = 'imported/{}'.format(full_path2)
        resp_moved = dbx_client.file_move(full_path2, move_to)
        metadata_file1 = dbx_client.metadata(full_path, list=True, 
                                             include_deleted=True)
        print metadata_file1

