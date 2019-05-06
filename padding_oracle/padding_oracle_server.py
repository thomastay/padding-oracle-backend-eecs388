from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
from base64 import b16encode, b16decode
import argparse

class PaddingOracle:
    """
    implements a AES encryption / decryption engine
    that is vulnerable to padding oracle attacks
    WARNING:
        For obvious reasons, you should not use this
        in production code.
        IT IS VULNERABLE TO A KNOWN ATTACK
        That said, the pycryptodome lib is really good
    """
    class DecryptBehavior:
        INVALID_PADDING = 0
        INVALID_VALIDATION = 1
        VALID_VALIDATION = 1
        OTHER_ERROR = 3

    def __init__(self, key):
        self.key = key

    @staticmethod
    def genHash(m, sender, recipient):
        return ":" + sender + ":" + recipient

    def encrypt(self, sender, recipient, plain_text):
        """
        Generates an AES encrypted cipher
        Padded with PCKS-7
        Hash is the string ":sender:recipient" with sender and
            recipient as in the function parameter
        IV is generated at random
        Block size is 16 Bytes [same as PyCrypto]
        """
        hashed_pt = plain_text + self.genHash(sender, recipient)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(Padding.pad(hashed_pt, AES.block_size))
        cipher_text = b16encode(cipher.iv) + b16encode(ct_bytes)
        return cipher_text

    def decrypt(self, sender, recipient, cipher_text):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("-e", "--encrypt", help = "[FROM] [TO] [MESSAGE] [KEY]",
                        nargs = 4)
    group.add_argument("-d", "--decrypt", help = "[FROM] [TO] [MESSAGE] [KEY]",
                        nargs = 4)
    args = parser.parse_args()



