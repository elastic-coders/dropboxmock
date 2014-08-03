# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from .responses import (request_token,
                        access_token,
                        oauth2_token)

# the (\d+) parameter in urls is the api version info

url_paths = [{'https://api.dropbox.com/(\d+)/oauth/request_token$':
                  request_token},
             {'https://api.dropbox.com/(\d+)/oauth/access_token':
                  access_token},
             {'https://api.dropbox.com/(\d+)/oauth2/token':
                  oauth2_token}]

