from __future__ import absolute_import


from .backend import dbox_client_backend
mock_dbx_client = dbox_client_backend.decorator
dbx_client_backend = dbox_client_backend
