import re


# ═══════════════════════════════════════════════════════════════
#  HASH PATTERNS
# ═══════════════════════════════════════════════════════════════

HASH_PATTERNS = [
    # name, regex, hashlib_name, crackable
    ("MD5",        r"^[a-f0-9]{32}$",                        "md5",     True),
    ("SHA1",       r"^[a-f0-9]{40}$",                        "sha1",    True),
    ("SHA224",     r"^[a-f0-9]{56}$",                        "sha224",  True),
    ("SHA256",     r"^[a-f0-9]{64}$",                        "sha256",  True),
    ("SHA384",     r"^[a-f0-9]{96}$",                        "sha384",  True),
    ("SHA512",     r"^[a-f0-9]{128}$",                       "sha512",  True),
    ("NTLM",       r"^[a-f0-9]{32}$",                        "md4",     True),
    ("bcrypt",     r"^\$2[aby]\$\d{2}\$.{53}$",              None,      False),
    ("MD5 Crypt",  r"^\$1\$.{1,8}\$.{22}$",                  None,      False),
    ("SHA512Crypt", r"^\$6\$.{1,16}\$.{86}$",                None,      False),
    ("MySQL4",     r"^[a-f0-9]{16}$",                        None,      True),
    ("CRC32",      r"^[a-f0-9]{8}$",                         None,      True),
    ("RIPEMD160",  r"^[a-f0-9]{40}$",                        "sha1",    True),
]

# ═══════════════════════════════════════════════════════════════
#  IDENTIFY
# ═══════════════════════════════════════════════════════════════

def identify(hash_str):
    """
    Returns a list of possible hash types:
    [{"name": str, "hashlib": str|None, "crackable": bool}]
    """
    hash_str = hash_str.strip()
    results = []
    seen = set()

    for name, pattern, hashlib_name, crackable in HASH_PATTERNS:
        if re.match(pattern, hash_str, re.IGNORECASE):
            if name not in seen:
                results.append({
                    "name": name,
                    "hashlib": hashlib_name,
                    "crackable": crackable,
                    "length": len(hash_str)
                })
                seen.add(name)

    return results if results else [{"name": "Unknown", "hashlib": None, "crackable": False, "length": len(hash_str)}]


def get_strength(hash_type):
    """Returns strength rating of a hash algorithm"""
    weak   = ["MD5", "SHA1", "MySQL4", "CRC32", "NTLM", "RIPEMD160"]
    medium = ["SHA224", "SHA256", "MD5 Crypt"]
    strong = ["SHA384", "SHA512", "bcrypt", "SHA512Crypt"]

    if hash_type in weak:
        return "Weak 🔴"
    elif hash_type in medium:
        return "Medium 🟡"
    elif hash_type in strong:
        return "Strong 🟢"
    return "Unknown ⚪"
