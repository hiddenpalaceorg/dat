from xml.etree.ElementTree import XML
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
from dat.keys import load_secret_key
from dat.version import version_string

WIKI_SIGNATURE_FORMAT = """<!-- BEGIN SIGNED MESSAGE -->
{message}
<!-- BEGIN SIGNATURE -->
{{{{datsignature|
Signed by: {signed_by}
Signer key: {signer_key}
Signature: {signature}
Version: {version}
}}}}
<!-- END SIGNATURE -->"""

XML_SIGNATURE_FORMAT = """---- BEGIN SIGNED MESSAGE ----
{message}
---- BEGIN SIGNATURE ----
Signed by: {signed_by}
Signer key: {signer_key}
Signature: {signature}
Version: {version}
---- END SIGNATURE ----"""


def signature_format(format):
    if format == "wiki":
        return WIKI_SIGNATURE_FORMAT
    elif format == "xml":
        return XML_SIGNATURE_FORMAT


def sign_message(message, format):
    key_info = load_secret_key()

    print(sign_message_using_key(message, format, key_info.key, key_info.user_name))


def sign_message_using_key(message, format, key, user_name):
    signed = key.sign(message.encode(), encoder=Base64Encoder)
    signer_key = key.verify_key.encode(encoder=Base64Encoder).decode()
    signature = signed.signature.decode()

    return signature_format(format).format(
        version=version_string(),
        message=message,
        signed_by=user_name,
        signer_key=signer_key,
        signature=signature,
    )
