# #!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pytz

from urlparse import urlparse, parse_qs

from dropmock.core.utils import build_formatted_response, normalize_file_name
from dropmock.core.decorators import authenticate_oauth2
from dropmock.session import dbx_session_backend
from dropmock.client import dbx_client_backend

#TODO in next release of this package: 
# manage document flow for different account


class ClientResponse(object):

    def __init__(self, backend):
        self.backend = backend


def token_from_oauth1(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/oauth2/token_from_oauth1
    global dbx_session_backend
    if not dbx_session_backend.is_connected(token='ABCDEFG'):
        dbx_session_backend.connect(token='ABCDEFG')
    return build_formatted_response(body={'access_token': 'ABCDEFG', 
                                          'token_type': 'bearer'},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def disable_access_token(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/disable_access_token
    global dbx_session_backend
    token = headers.get('access_token', '')
    oauth_token, oauth_token_secret = '', ''
    if token == '':
        oauth_token, oauth_token_secret = get_oauth_from_url(url)
        if ((oauth_token == '') and (request.parsed_body not in ['', None])):
            oauth_token = request.parsed_body.get('oauth_token', '')
    dbx_session_backend.disconnect(token=token, 
                                   oauth_token=oauth_token,
                                   oauth_token_secret=oauth_token_secret)
    return build_formatted_response(body={},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def get_oauth_from_url(url):
    parsed_url = urlparse(url, allow_fragments=True)
    query_string = parse_qs(parsed_url.query)
    oauth_token = query_string.get('oauth_token', '')
    oauth_token_secret = query_string.get('oauth_token_sercet', '')
    return oauth_token, oauth_token_secret

def account_info(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/account/info
    #TODO: retrieve different account info depending by request token
    return build_formatted_response(body={
            'referral_link': 'https://www.dropbox.com/referrals/r1a2n3d4m5s6t7',
            'display_name': 'John Doe',
            'uid': 12345678,
            'team': {
                'name': 'Elastic Inc.'
                },
            'country': 'IT',
            'quota_info': {
                'shared': 253738410565,
                'quota': 107374182400000,
                'normal': 680031877871
                }
            },
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)


def get_token(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/oauth2/token
    global dbx_session_backend
    if not dbx_session_backend.is_connected(token='ABCDEFG'):
        dbx_session_backend.connect(token='ABCDEFG')
    return build_formatted_response(body={'access_token': 'ABCDEFG', 
                                          'token_type': 'bearer', 
                                          'uid': '12345'},
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

def _build_metadata(list_metadata):
    # base metadata content
    _metadata = {
        'size': '225.4KB',
        'rev': '35e97029684fe',
        'thumb_exists': False,
        'bytes': 230783,
        'modified': 'Tue, 19 Jul 2011 21:55:38 +0000',
        'client_mtime': 'Mon, 18 Jul 2011 18:04:35 +0000',
        'path': '/Getting_Started.pdf',
        'is_dir': False,
        'icon': 'page_white_acrobat',
        'root': 'dropbox',
        'mime_type': 'application/pdf',
        'revision': 220823
        }
    if list_metadata:
        _metadata['contents'] = {
            'size': "2.3 MB",
            'rev': "38af1b183490",
            'thumb_exists': True,
            'bytes': 2453963,
            'modified': 'Mon, 07 Apr 2014 23:13:16 +0000',
            'client_mtime': 'Thu, 29 Aug 2013 01:12:02 +0000',
            'path': '/Photos/flower.jpg',
            'photo_info': {
              'lat_long': [
                37.77256666666666,
                -122.45934166666667
              ],
              'time_taken': 'Wed, 28 Aug 2013 18:12:02 +0000'
            },
            'is_dir': False,
            'icon': 'page_white_picture',
            'root': 'dropbox',
            'mime_type': 'image/jpeg',
            'revision': 14511
        }
    return _metadata


@authenticate_oauth2
def get_delta(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/delta
    cursor = request.parsed_body.get('cursor', [''])
    list_metadata = request.parsed_body.get('list', [False])
    if cursor[0] == '1st':
        body = {'entries':[['/photo', _build_metadata(list_metadata)],],
                'reset': False,
                'cursor': '2nd',
                'has_more': False}
    else:
        body = {'entries': [['/photo', _build_metadata(list_metadata)],],
                'reset': False,
                'cursor': '1st',
                'has_more': True}
    return build_formatted_response(body=body,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def sandbox(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/metadata/sandbox
    # sandbox only retrieve 200 status code
    return build_formatted_response()

@authenticate_oauth2
def get_media(request, url, headers, *args, **kwargs):
    # mock https://api.dropbox.com/(\d+)/media/auto/
    # expires: the url is valid 4 hours, 
    # look at https://www.dropbox.com/developers/core/docs#media
    file_full_path = urlparse(request.path).path
    file_path = normalize_file_name(file_full_path)
    body = {'url': 
            'https://dl.dropboxusercontent.com/1/view/{}'\
                .format(file_path),
            'expires': (datetime.datetime.utcnow()\
                            .replace(tzinfo=pytz.utc)+datetime\
                .timedelta(hours=4)).strftime('%a, %d %b %Y %H:%M:%S %z')}
    return build_formatted_response(body=body,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def put_file(request, url, headers, *args, **kwargs):
    # mock https://api-content.dropbox.com/(\d+)/files_put/([a-zA-Z]+)/([a-zA-Z]+)
    global dbx_client_backend
    url_parse = urlparse(request.path)
    file_full_path = url_parse.path
    overwrite = parse_qs(url_parse.query).get('overwrite', False)
    # here file_full_path looks like /1/files_put/auto/test/test.txt

    file_obj = request.rfile
    dropbox_file = dbx_client_backend\
        .add_file_to_backend(file_full_path, file_obj, overwrite=overwrite)
    #TODO: get document file path (not only name) from url
    # and manage it in a session backend dictionary
    return build_formatted_response(body=dropbox_file,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def get_file(request, url, headers, *args, **kwargs):
    # mock https://api-content.dropbox.com/(\d+)/files/([a-zA-Z]+)/([a-zA-Z]+)
    if request.method != 'GET':
        return build_formatted_response(body='method not allowed',
                                        status=400)
    global dbx_client_backend
    url_parse = urlparse(request.path)
    file_full_path = url_parse.path
    dropbox_file = dbx_client_backend.get_file_from_backend(file_full_path)
    if not dropbox_file:
        return build_formatted_response(status=404)
    #FIXME: httpretty in this case doesn't work!! :-(
    return dropbox_file['file']

@authenticate_oauth2
def delete_file(request, url, headers, *args, **kwargs):
    if request.method != 'POST':
        return build_formatted_response(body='method_not_allowed',
                                       status=400)
    global dbx_client_backend
    file_path = '{}{}'.format(request.parsed_body['root'][0],
                               request.parsed_body['path'][0])
    file_deleted_response = dbx_client_backend.delete_file(file_path)
    if not file_deleted_response:
        return build_formatted_response(status=404)
    return build_formatted_response(body=file_deleted_response['metadata'], 
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

@authenticate_oauth2
def move_file(request, url, headers, *args, **kwargs):
    if request.method != 'POST':
        return build_formatted_response(body='method_not_allowed',
                                       status=400)
    #TODO for the moment root path is always auto....
    # we have to handle this info in client backend!!!!
    from_path = 'auto{}'.format(request.parsed_body['from_path'][0])
    to_path = 'auto{}'.format(request.parsed_body['to_path'][0])
    global dbx_client_backend
    moved_file = dbx_client_backend.move_file(from_path, to_path)
    if not moved_file:
        return build_formatted_response(status=404)
    return build_formatted_response(body=moved_file['metadata'], 
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)
    
@authenticate_oauth2
def metadata(request, url, headers, *args, **kwargs):
    if request.method != 'GET':
        return build_formatted_response(body='method not allowed',
                                        status=400)
    global dbx_client_backend
    parsed_url = urlparse(request.path)
    file_full_path = parsed_url.path
    qs = parse_qs(parsed_url.query)
    list_content = qs.get('list', True)
    include_deleted = qs.get('include_deleted', True)
    file_limit = qs.get('file_limit', 25000)
    ret_val = dbx_client_backend.metadata(file_full_path, 
                                          list_content, 
                                          include_deleted, 
                                          file_limit)
    if not ret_val:
        return build_formatted_response(status=404)
    return build_formatted_response(body=ret_val,
                                    headers={'content-type': 
                                             'application/json'},
                                    status=200)

