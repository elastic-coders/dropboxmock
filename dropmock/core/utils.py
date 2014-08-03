# #!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def build_formatted_response(body='', headers={}, status=200, 
                             *args, **kwargs):
    ''' utility unit to format correctly responses for HTTPretty server call
    '''
    content_type = headers.get('content-type', 'text/plain')
    if content_type == 'application/json':
        body = json.dumps(body)
    _body = body
    _headers = {'content-type': content_type,
                'server': headers.pop('server', 'HTTPretty')}
    if headers:
        _headers.update(headers)
    return status, _headers, _body

