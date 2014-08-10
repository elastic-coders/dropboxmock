from __future__ import absolute_import


from .backend import dbox_session_backend
mock_dbx_session = dbox_session_backend.decorator
dbx_session_backend = dbox_session_backend
