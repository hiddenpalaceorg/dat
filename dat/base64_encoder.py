import base64


class UnpaddedBase64Encoder(object):
    """A base64 encoder that ignores padding (=) at the end.

    This is friendlier to wiki syntax.
    """

    @staticmethod
    def encode(data):
        return base64.b64encode(data).rstrip(b"=")

    @staticmethod
    def decode(data):
        return base64.b64decode(data + b"==")
