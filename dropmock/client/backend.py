# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from httpretty import HTTPretty

from dropmock.core.base import BaseBackend


class ClientBackend(BaseBackend):
    
    def __init__(self, *args, **kwargs):
        super(ClientBackend, self).__init__(*args, **kwargs)



dbox_client_backend = ClientBackend()
