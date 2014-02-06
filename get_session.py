import os
import time
import datetime
from argparse import ArgumentParser

from twisted.internet import defer
from twisted.internet import reactor
from twisted.python import log

from cli import cli, security, constants, authdata


base_api_url = constants.BASE_API_URL
domain = constants.DOMAIN

def logging_fabric(file_path):
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    msg_logger = log.LogPublisher()
    log_file = open(file_path, 'w+')
    fileobserver = log.FileLogObserver(log_file)
    msg_logger.addObserver(fileobserver.emit)
    return msg_logger

def on_pars(resp, msg_logger, user_name, email, password):
    # print 'Resp : {0}'.format(datetime.datetime.now())
    msg_logger.msg('|'.join([user_name, email, password, str(resp.get('Set-Cookie'))]))

@defer.inlineCallbacks
def main(msg_logger, sessions_num):
    # First we do Coins.get for get 'currency'.
    # import ipdb; ipdb.set_trace()
    connector = cli.ShinyClient(constants.BASE_API_URL,
                                secure_token=constants.TOKEN,
                                domain=domain
    )
    currency = yield connector.get(domain=domain)
    print currency

    connector.set_auth_aware(True)
    # Switch to 'Session' namespace
    connector.set_namespace('Session')
    start_time = time.time()
    for i in xrange(sessions_num):
        user_name = authdata.get_name()
        email = authdata.get_mail()
        password = authdata.get_password()
        hash = security.get_digital_signature(password)
        d =  connector.get(username=user_name,
                           email=email,
                           domain=domain,
                           hash=hash,
                           currency=currency[0]
        )
        d.addCallback(on_pars, msg_logger, user_name, email, password)

    # print 'done for {seconds} seconds'.format(seconds=time.time()-start_time)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s_num', '--sessions',
                        type=int,
                        default=constants.SESSIONS_NUM
    )
    parser.add_argument('-rf', '--results_file',
                        default=constants.RESULTS_FILENAME
    )
    args = parser.parse_args()
    results_file_path = os.path.abspath(os.path.join(os.getcwd(), args.results_file))
    print 'Getting {sessions} sessions into {path} .. '\
           .format(sessions=args.sessions,
                   path=results_file_path
    ),
    tx_log = logging_fabric(results_file_path)
    main(tx_log, args.sessions)
    reactor.run()

