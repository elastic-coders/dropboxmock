# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from httpretty import HTTPretty

from dropmock.core.base import BaseBackend


class SessionBackend(BaseBackend):
    
    def __init__(self, *args, **kwargs):
        super(SessionBackend, self).__init__(*args, **kwargs)



dbox_session_backend = SessionBackend()
