# #!/usr/bin/env python
# -*- coding: utf-8 -*-

from .responses import (token_from_oauth1,
                        disable_access_token,
                        account_info,
                        get_token,
                        get_delta,
                        sandbox)

# the (\d+) parameter in urls is the api version info

url_paths = [{'https://api.dropbox.com/(\d+)/oauth2/token_from_oauth1$':
                  token_from_oauth1},
             {'https://api.dropbox.com/(\d+)/disable_access_token':
                  disable_access_token},
             {'https://api.dropbox.com/(\d+)/account/info':
                  account_info},
             {'https://api.dropbox.com/(\d+)/oauth2/token':
                  get_token},
             {'https://api.dropbox.com/(\d+)/delta':
                  get_delta},
             {'https://api.dropbox.com/(\d+)/metadata/sandbox':
                  sandbox},]

