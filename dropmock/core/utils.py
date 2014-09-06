# #!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


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

# thanks to stackoverflow!!!!
def human_size(size_bytes):
    """
    format a size in bytes into a 'human' file size, 
    e.g. bytes, KB, MB, GB, TB, PB
    Note that bytes/KB will be reported in whole numbers 
    but MB and above will have greater precision
    e.g. 1 byte, 43 bytes, 443 KB, 4.3 MB, 4.43 GB, etc
    """
    if size_bytes == 1:
        # because I really hate unnecessary plurals
        return "1 byte"

    suffixes_table = [('bytes',0),('KB',0),('MB',1),
                      ('GB',2),('TB',2), ('PB',2)]

    num = float(size_bytes)
    for suffix, precision in suffixes_table:
        if num < 1024.0:
            break
        num /= 1024.0
            
    if precision == 0:
        formatted_size = "%d" % num
    else:
        formatted_size = str(round(num, ndigits=precision))
                
    return "%s %s" % (formatted_size, suffix)

def get_mime_type(file_name_key):
    _, ext = os.path.splitext(file_name_key)
    ext = ext.lower()
    if ext == '.txt':
        return 'text/plain'
    elif ext == '.pdf':
        return 'application/pdf'
    elif ext == '.xls':
        return 'application/vnd.ms-excel'
    elif ext == '.csv':
        return 'text/csv'
    else:
        return ''
        
def normalize_file_name(file_name):
    ''' normalize file name from full_path passed in dropbox request path
    "/1/files_put/auto/test/test.txt" becomes "auto/test/test.txt"
    '''
    file_name_parts = file_name.split('/')
    if file_name_parts[0] == 'auto':
        # in this case the name is already normalized
        # when root will be handled this statements become == self.root
        return file_name
    return '/'.join(file_name_parts[3:])
