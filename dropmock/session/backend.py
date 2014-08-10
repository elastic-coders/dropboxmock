# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from httpretty import HTTPretty

from dropmock.core.base import BaseBackend
from urlparse import urlparse, parse_qs


class SessionBackend(BaseBackend):
    
    def __init__(self, *args, **kwargs):
        super(SessionBackend, self).__init__(*args, **kwargs)

    def oauth2_authorize_url(self, url=''):
        assert url != ''
        parsed_url = urlparse(url, allow_fragments=True)
        query_string = parse_qs(parsed_url.query)
        resp_type = query_string.get('response_type', None)
        client_id = query_string.get('client_id', None)
        state = query_string.get('state', None)
        redirect_uri = query_string.get('redirect_uri', None)
        # response type and client id is required data
        if resp_type is None:
            raise ValueError('response_type required on oauth2 authorization')
        if client_id is None:
            raise ValueError('clien id required on oauth2 authorization')
        if redirect_uri is None:
            redirect_uri = 'http://localhost'
        # handle token flow
        if resp_type[0] == 'token':
            ret_val = '{}#access_token=ABCDEFG&uid={}'\
                '&token_type=bearer&state={}'.format(redirect_uri[0],
                                                     client_id[0],
                                                     state[0] if state else '')
        elif resp_type[0] == 'code':
            ret_val = '{}?code=ABCDEFG&uid={}&state={}'\
                .format(redirect_uri[0],
                        state[0] if state else '')
        return ret_val
        

dbox_session_backend = SessionBackend()
