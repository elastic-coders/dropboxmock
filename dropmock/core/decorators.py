# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from django.utils.decorators import available_attrs

from dropmock.core.utils import build_formatted_response
from dropmock.session import dbx_session_backend


def authenticate_oauth2(func):
    '''
    decorate function that need oauth2 authentication
    '''
    def _authenticate_ouath2(request, url, headers, *args, **kwargs):
        bearer_token = request.headers.get('Authorization', '')
        token = bearer_token[7:]
        global dbx_session_backend
        if not dbx_session_backend.is_connected(token=token):
            return build_formatted_response(status=403)
        if bearer_token != 'Bearer ABCDEFG':
            return build_formatted_response(status=403)
        return func(request, url, headers, *args, **kwargs)
    return wraps(func, assigned=available_attrs(func))(_authenticate_ouath2)
