import hashlib


SUPPORTED = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


def generate(text, hash_type="md5"):
    """
    Generate hash from plain text.
    Returns hex digest or None if unsupported.
    """
    hash_type = hash_type.lower()

    if hash_type not in SUPPORTED:
        return None

    h = hashlib.new(hash_type)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def supported_types():
    return SUPPORTED
