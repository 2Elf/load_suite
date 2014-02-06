import hashlib


def get_digital_signature(_password):
    passw_hash = hashlib.sha256(_password).hexdigest()
    return hashlib.sha256(
        '{passw_hash}.{passw_hash}'.format(passw_hash=passw_hash)
    ).hexdigest()