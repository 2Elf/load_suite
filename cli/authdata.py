import random

import constants


def get_random_word(wordLen, seq=constants.CHOICE_SEQUENCE):
    word = ''
    for i in range(wordLen):
        word += random.choice(seq)
    return word

def get_name():
    firsn_len = random.randint(5, 8)
    first_name = get_random_word(
        firsn_len,constants.LETTERS).capitalize()
    last_len = random.randint(5, 8)
    last_name = get_random_word(
        last_len,constants.LETTERS).capitalize()
    return '{first_name} {last_name}'\
           .format(last_name=last_name,
                    first_name=first_name
           )

def get_password():
    passw_len = random.randint(5, 8)
    return get_random_word(passw_len)

def get_mail():
    login_len = random.randint(6, 8)
    login = get_random_word(login_len)
    domain = random.choice(constants.MAIL_DOMAIN_NAMES)
    return '{login}@{domain}'\
            .format(login=login,
                    domain=domain
    )

