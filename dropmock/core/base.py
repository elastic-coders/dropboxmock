import functools
import re

from httpretty import HTTPretty


class MockDropbox(object):
    _count = 0

    def __init__(self, backend):
        self.backend = backend

    def __call__(self, func):
        return self.decorate_callable(func)

    def __enter__(self):
        self.start_mocking()

    def __exit__(self, *args):
        self.stop_mocking()

    def start_mocking(self):
        self.__class__._count += 1
        self.backend.reset()

        if not HTTPretty.is_enabled():
            HTTPretty.enable()

        for method in HTTPretty.METHODS:
            # mock all url to dropbox for any module....
            for key, value in self.backend.urls.iteritems():
                HTTPretty.register_uri(
                    method=method,
                    uri=re.compile(key),
                    body=value,
                )
                
    def stop_mocking(self):
        self.__class__._count -= 1

        if self.__class__._count < 0:
            raise RuntimeError('can\'t stop() before start().')

        if self.__class__._count == 0:
            HTTPretty.disable()

    def decorate_callable(self, func):
        def wrapper(*args, **kwargs):
            with self:
                result = func(*args, **kwargs)
            return result
        functools.update_wrapper(wrapper, func)
        wrapper.__wrapped__ = func
        return wrapper


class BaseBackend(object):

    def reset(self):
        self.__dict__ = {}
        self.__init__()

    @property
    def _url_module(self):
        backend_module = self.__class__.__module__
        backend_urls_module_name = backend_module.replace("backend", "urls")
        backend_urls_module = __import__(backend_urls_module_name, 
                                         fromlist=['url_paths'])
        return backend_urls_module

    @property
    def urls(self):
        """
        we retrieve a dict containing all the url to be mocked and 
        handler to manage mocked call
        """

        urls = {}
        for url_item in self._url_module.url_paths:
            for url_path, handler in url_item.iteritems():
                urls[url_path] = handler

        return urls

    @property
    def url_paths(self):
        """
        A dictionary of the paths of the urls to be mocked with this service and
        the handlers that should be called in their place
        """
        unformatted_paths = self._url_module.url_paths

        paths = {}
        for unformatted_path, handler in unformatted_paths.iteritems():
            path = unformatted_path.format("")
            paths[path] = handler

        return paths


    def decorator(self, func=None):
        if not func:
            return MockDropbox(self)
        return MockDropbox(self)(func)
            
