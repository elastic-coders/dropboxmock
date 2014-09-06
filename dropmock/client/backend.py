# #!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import datetime

from httpretty import HTTPretty

from dropmock.core.base import BaseBackend
from dropmock.core.utils import get_mime_type, human_size, normalize_file_name


class ClientBackend(BaseBackend):
    '''this class mock dropbox backend...
    Client backend manage file put and other dropbox event!
    '''
    
    def __init__(self, *args, **kwargs):
        super(ClientBackend, self).__init__(*args, **kwargs)
        self.file_list = []

    def add_file_to_backend(self, file_name_key, file_obj, overwrite=False):
        ''' function to add a file to the backend server
        the backend have a list of dictionary object
        every object is a file loaded
        input:
        - file_name_key: the full_path_key of the single file
        - file_obj: the real file object
        output:
        None if not overwrite and document already present
        dictionary rapresenting document otherwse
        '''
        if not file_obj:
            raise ValueError('file is required')
        file_name_key = normalize_file_name(file_name_key)
        file_data = self.get_file_from_backend(file_name_key)
        if file_data and not overwrite:
            return None
        file_obj.seek(0, os.SEEK_END)
        size = file_obj.tell()
        ret_val = {'size': human_size(size),
                   'rev': unicode(uuid.uuid4()),
                   'thumb_exists': False,
                   'bytes': size,
                   'modified': datetime.datetime.now().isoformat(' '),
                   'path': file_name_key,
                   'is_dir': False,
                   'icon': '',
                   'root': 'dropbox',
                   'mime_type': get_mime_type(file_name_key),
                   'revision': 0}
        if file_data:
            file_data['metadata'] = ret_val
            file_data['file'] = file_obj
        else:
            file_data = {'name': file_name_key,
                         'file': file_obj,
                         'metadata': ret_val}
            self.file_list.append(file_data)
        return ret_val

    def get_file_from_backend(self, file_name_key):
        assert file_name_key is not None
        file_name_key = normalize_file_name(file_name_key)
        for file_data in self.file_list:
            if file_data['name'] == file_name_key:
                return file_data
        return None

    def delete_file(self, file_name_key):
        assert file_name_key is not None
        for file_data in self.file_list:
            if file_data['name'] == file_name_key:
                self.file_list.remove(file_data)
                return file_data
        return None


dbox_client_backend = ClientBackend()
