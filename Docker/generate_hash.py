import hmac
import hashlib
from urllib.parse import quote
from typing import Dict

    # Generate a HMAC-SHA1 hash based on the method, host, path, and parameters.

    # This is the python translation of the Java code in the Signature.java file.

    # method: HTTP method
    # host: Host name
    # path: Path of the request
    # params: Additional parameters as a dictionary
    # key: Secret key for hashing
    # :return: HMAC-SHA1 hash

def generate_hmac(method: str, host: str, path: str, params: Dict[str, str], key: str = "CE2766AA8B74FBAC70A26CF5C83E9") -> str:
    serialized_params = serialize_params(params)
    raw_string = f"{method}%{host}%{path}%{serialized_params}"
    return "HMAC " + sha1(raw_string, key)

def sha1(s: str, key_string: str) -> str:
    hashed = hmac.new(key_string.encode(), s.encode(), hashlib.sha1)
    return hashed.hexdigest().lower()

def serialize_params(params: Dict[str, str]) -> str:
    pairs = []
    for key, value in params.items():
        if value is not None:
            pairs.append(f"{encode(key)}%{encode(value)}")
    pairs.sort()
    return "%".join(pairs)


def encode(s: str) -> str:
    return quote(s, safe='').replace('+', '%20').replace('!', '%21').replace("'", '%27').replace('(', '%28').replace(')', '%29').replace('~', '%7E')
