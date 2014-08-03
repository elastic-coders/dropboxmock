from django.test import TestCase
import dropbox

from dropmock import mock_dbx_session

DROPBOX_CLIENT_ID_FAKE = 'p5sqcubc8ndn70x'
DROPBOX_CLIENT_SECRET_FAKE = '8a44il5xhkoize6'

class SessionTestCase(TestCase):

    @mock_dbx_session
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
