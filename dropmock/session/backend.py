#!/usr/bin/env python
# -*- coding: utf-8 -*-

from httpretty import HTTPretty

from dropmock.core.base import BaseBackend
from urlparse import urlparse, parse_qs


class SessionBackend(BaseBackend):
    ''' This class mock the dropbox backend...
    Session Backend manage some account info such as token, connection, etc
    and is used by mock library to know if a session is active or not
    and check if workflow used in test is correct 
    '''
    ACCOUNT_STATUS_CONNECTED = 'c'
    ACCOUNT_STATUS_DISCONNECTED = 'd'
    ACCOUNT_STATUS_CHOICES = [(ACCOUNT_STATUS_CONNECTED, 'connected'),
                              (ACCOUNT_STATUS_DISCONNECTED, 'disconnected')]
    
    def __init__(self, *args, **kwargs):
        ''' Initialize session backend and his accounts
        '''
        self.account_list = self.init_accounts()
        super(SessionBackend, self).__init__(*args, **kwargs)

    def init_accounts(self):
        '''At the moment we define 3 account for test
        '''
        return [{'id': 1,
                 'access_token': 'ABCDEFG',
                 'oauth_token_secret': '',
                 'oauth_token': '', 
                 'token_oauth_type': 2,
                 'status': self.ACCOUNT_STATUS_DISCONNECTED},
                {'id': 2,
                 'access_token': '',
                 'oauth_token_secret': '95grkd9na7hm',
                 'oauth_token': 'ccl4li5n1q9b', 
                 'token_oauth_type': 1,
                 'status': self.ACCOUNT_STATUS_DISCONNECTED},
                {'id': 3,
                 'access_token': '',
                 'oauth_token_secret': 'b9q1n5il4lcc',
                 'oauth_token': 'mh7an9dkrg59', 
                 'token_oauth_type': 1,
                 'status': self.ACCOUNT_STATUS_DISCONNECTED},]

    def get_account(self, token='', oauth_token='', oauth_token_secret=''):
        ''' function that retrieve account by oauth2 token or oauth token
        '''
        for account in self.account_list:
            if (account['access_token'] != token and 
                account['oauth_token'] != oauth_token):
                continue
            return account
        return None


    def is_connected(self, token='', oauth_token='', oauth_token_secret=''):
        ''' test if a specific account is connected by his token
        '''
        account = self.get_account(token, oauth_token, oauth_token_secret)
        return account['status'] == self.ACCOUNT_STATUS_CONNECTED

    def connect(self, token='', oauth_token='', oauth_token_secret=''):
        # connect session
        account = self.get_account(token, oauth_token, oauth_token_secret)
        if not account:
            raise ValueError('account not existent {}'\
                                 .format(token if token != '' else oauth_token))
        account['status'] = self.ACCOUNT_STATUS_CONNECTED

    def disconnect(self, token='', oauth_token='', oauth_token_secret=''):
        # disconnect session
        account = self.get_account(token, oauth_token, oauth_token_secret)
        if not account:
            raise ValueError('account not existent {}'\
                                 .format(token if token != '' else oauth_token))
        account['status'] = self.ACCOUNT_STATUS_DISCONNECTED

    def oauth2_authorize_url(self, url=''):
        ''' function that simulate authorize workflow
        in your test you don't need to use webbrowser 
        to authorize a specific token
        '''
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
        self.connect()
        return ret_val
        
    def get_oauth2_access_token_direct(self):
        token = 'ABCDEFG'
        self.connect(token=token)
        return token

dbox_session_backend = SessionBackend()
