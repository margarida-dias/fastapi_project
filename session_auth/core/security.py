from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def validate_token(token: str, hash_token: str) -> bool:
    """
    Validate token, comparing token in text given by the user and the hash of the token
    that is saved in DB.
    """
    return CRIPTO.verify(token, hash_token)


def create_hash_token(token: str) -> str:
    """
    Function to create and return token
    :param token:
    :return: hash_token
    """
    return CRIPTO.hash(token)
