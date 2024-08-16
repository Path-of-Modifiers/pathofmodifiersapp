import bcrypt


def create_hashed_ip(request_data_ip: str) -> str:
    """
    IPs are hashed to protect user privacy.
    They are used to secure the turnstile endpoint from abuse.
    """
    salt = bcrypt.gensalt()

    encoded_ip = request_data_ip.encode("utf-8")

    hashed_ip = bcrypt.hashpw(encoded_ip, salt)

    hashed_ip = hashed_ip.decode("utf-8")

    return hashed_ip
