import sys
import hashlib
import json
import requests

sys.path.append('../ehlo')
from ehlo.shine import BaseShinyClient
from twisted.internet import reactor

url = 'http://glow.ebti.co/api/Coins'
base_api_url = 'http://glow.ebti.co'
domain = 'qa.ebti.co'
coins_request = {
    'domain': domain
}

class ShinyClient(BaseShinyClient):
    '''
        It derive BaseShinyClient that implement GLOW api
    '''

    def __init__(self, base_api_url, name_space, session_token=None):
        BaseShinyClient.__init__(self, session_token)
        self.base_api_url = base_api_url
        self.namespace = name_space

    def set_namespace(self, namespace):
        self.namespace = namespace

    def set_token(self, session_token):
        self.session_token = session_token

    def base_api_url(self):
        return self.base_api_url

    def namespace(self):
        return self.namespace

    def sentry_client(self):
        psss



def get_api_request(method, data):
    '''
        It returns body of api request
        with passed method and data.
    '''
    api_request = {
    'action': method,
    'data' : data
    }
    return json.dumps(api_request)

def get_authorize_data(name, email, password,
                       domain=domain, currency='currency'):
    '''
        It returns
    '''
    authorize_request = {
      'username': name,
      'email' : email,
      'domain': domain,
      'hash': hashlib.sha256(password).hexdigest(),
      'currency': currency
    }
    return json.dumps(authorize_request)

if __name__ == '__main__':
    r = requests.post(url, data=json.dumps({"action": "get", "data": {"domain": "qa.ebti.co"}}),
                      headers={'content-type': 'application/json'})
    currency = json.loads(r.text)['data'][0]
    print currency

    # for user in users:
    cli = ShinyClient(base_api_url, 'Session')
    cli.get(username='test_user1', email='test_email@gmail.com', domain=domain,
            hash=str(hashlib.sha256('Password01').hexdigest), currency='PRZ')

    reactor.run()

