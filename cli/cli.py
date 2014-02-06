import sys

from twisted.python import log

sys.path.append('../../ehlo')
from ehlo.shine import ShinyConnector



class DummySentryClient(object):

    def captureException(self, args):
        log.msg(args)


class ShinyClient(ShinyConnector):
    '''
        It implements abstract ShinyConnector that implement GLOW api
    '''

    def __init__(self, base_api_url, name_space='Coins', **kwargs):
        ShinyConnector.__init__(self, **kwargs)
        self.base_api_url = base_api_url
        self.namespace = name_space

    def set_namespace(self, namespace):
        self.namespace = namespace

    def set_token(self, session_token):
        self.session_token = session_token

    def set_auth_aware(self, auth_aware):
        self.auth_aware = auth_aware

    def base_api_url(self):
        return self.base_api_url

    def namespace(self):
        return self.namespace

    def sentry_client(self):
        return DummySentryClient()

    def secret_key(self):
        pass

    def on_error(self, _failure):
        self.sentry_client().captureException(
            (_failure.type, _failure.value, _failure.getTracebackObject())
        )
        raise failure.Failure(
            (_failure.type, errors.ShineInternalError(), _failure.getTracebackObject())
        )
