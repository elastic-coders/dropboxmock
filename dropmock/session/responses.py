# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from dropmock.core.utils import build_formatted_response


#TODO in next release of this package: retrieve objects 
#that couple token and authenticated account ID

class SessionResponse(object):

    def __init__(self, backend):
        self.backend = backend


def request_token(request, url, headers, *args, **kwargs):
    return build_formatted_response(body="oauth_token_secret=b9q1n5il4lcc&oauth_token=mh7an9dkrg59",
                                    status=200)

def access_token(request, url, headers, *args, **kwargs):
    return build_formatted_response(body="oauth_token_secret=95grkd9na7hm&oauth_token=ccl4li5n1q9b&uid=100",
                                    status=200)

def oauth2_token(request, url, headers, *args, **kwargs):
    return build_formatted_response(body={"access_token": "ABCDEFG", 
                                          "token_type": "bearer", 
                                          "uid": "12345"},
                                    header={"content-type": 'application/json'},
                                    status=200)


