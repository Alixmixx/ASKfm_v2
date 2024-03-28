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


#  GET%api.ask.fm:443%/token%adid%806881bc-47db-4b0e-91bc-331f246456d7%did%c7ac224006ff17cb%rt%1%ts%1709531393
#  GET%api.ask.fm:443%/token%adid%806881bc-47db-4b0e-91bc-331f246456d7%did%c7ac224006ff17cb%rt%1%ts%1709531393

#  GET%api.ask.fm:443%/config%rt%1%ts%1709519857   string to be hashed
#  CE2766AA8B74FBAC70A26CF5C83E9  key

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

#print(generate_hmac("GET", "api.ask.fm:443", "/token", {"adid": "", "did": "3049e49e18cfdcb8", "rt": "1", "ts": "1711439790"}))
