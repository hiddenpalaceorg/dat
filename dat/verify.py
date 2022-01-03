import re
import nacl
from nacl.signing import VerifyKey

from dat.base64_encoder import UnpaddedBase64Encoder


def valid(value):
    if value:
        return "valid"
    else:
        return "invalid"


class VerificationResult:
    def __init__(self, valid_format, valid_signature):
        self.valid_format = valid_format
        self.valid_signature = valid_signature

    def __str__(self):
        return (
            f"Message format: {valid(self.valid_format)}\n"
            f"Signature: {valid(self.valid_signature)}"
        )


def verify_file(path):
    with open(path) as f:
        result = verify_message(f.read())

        print(result)


RE_PATTERN = """<!-- BEGIN SIGNED MESSAGE -->
(.*?)
<!-- BEGIN SIGNATURE -->
{{DatSignature
\| Signed by: .*?
\| Signer key: (.*?)
\| Signature: (.*?)
\| Version: .*?
}}
<!-- END SIGNATURE -->"""


def verify_message(bundle):
    match = re.search(RE_PATTERN, bundle, flags=re.DOTALL)

    if not match:
        return VerificationResult(valid_format=False, valid_signature=False)

    message, verify_key, signature = match.groups()

    key = VerifyKey(verify_key.encode(), encoder=UnpaddedBase64Encoder)

    try:
        key.verify(message.encode(), UnpaddedBase64Encoder.decode(signature.encode()))

        return VerificationResult(valid_format=True, valid_signature=True)
    except nacl.exceptions.BadSignatureError:
        return VerificationResult(valid_format=True, valid_signature=False)
