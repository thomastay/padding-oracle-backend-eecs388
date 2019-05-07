from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
from base64 import b16encode, b16decode
import argparse

class PaddingOracleError(Exception):
    def __init__(self, message):
        self.message = message

class KeyLenError(PaddingOracleError):
    pass

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
        VALID_VALIDATION = 2

    def __init__(self, key):
        KEY_SIZE = 16
        if len(key.encode()) is KEY_SIZE:
            self.key = key.encode()
        elif len(key.encode()) is 0:
            self.key = get_random_bytes(KEY_SIZE)
        else:
            raise KeyLenError("Key must be exactly 16 bytes long or empty")

    @staticmethod
    def genHash(sender, recipient):
        return ":" + sender + ":" + recipient

    @staticmethod
    def getHash(hashed_pt, hash_len):
        return hashed_pt[-hash_len:]

    def encrypt(self, sender, recipient, plain_text):
        """
        Generates an AES encrypted cipher
        Uses MAC, then Encrypt model
        Padded with PCKS-7
        Hash is the string ":sender:recipient" with sender and
            recipient as in the function parameter
        IV is generated at random
        Block size is 16 Bytes [same as PyCrypto]
        """
        hashed_pt = plain_text + self.genHash(sender, recipient)
        hashed_bytes = hashed_pt.encode()           # str to bytes
        cipher = AES.new(self.key, AES.MODE_CBC)    # IV is generated randomly
                                                    # if not specified
        ct_bytes = cipher.encrypt(Padding.pad(hashed_bytes, AES.block_size))
        cipher_text = b16encode(cipher.iv) + b16encode(ct_bytes)
        return cipher_text.decode()

    def decrypt(self, sender, recipient, cipher_text):
        """
        Decrypts an AES encrypted cipher
        """
        init_vector = b16decode(cipher_text)[:AES.block_size]
        ct_bytes = b16decode(cipher_text)[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv= init_vector)
        padded_hashed_pt = cipher.decrypt(ct_bytes)
        try:
            hashed_pt = Padding.unpad(padded_hashed_pt, AES.block_size).decode()
            hash_len = len(sender) + len(recipient) + 2 #two colons
            pt_MAC = self.getHash(hashed_pt, hash_len)
            if pt_MAC == self.genHash(sender, recipient):
                # Hash is valid
                return PaddingOracle.DecryptBehavior.VALID_VALIDATION
            else:
                return PaddingOracle.DecryptBehavior.INVALID_VALIDATION
        except ValueError:
            # Padding error
            return PaddingOracle.DecryptBehavior.INVALID_PADDING

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("-e", "--encrypt", help = "[FROM] [TO] [MESSAGE] [KEY]",
                        nargs = 4)
    group.add_argument("-d", "--decrypt", help = "[FROM] [TO] [MESSAGE] [KEY]",
                        nargs = 4)
    args = parser.parse_args()
    # Start the server and process command line arguments
    if args.encrypt:
        server = PaddingOracle(args.encrypt[3])
        encrypted = server.encrypt(args.encrypt[0], args.encrypt[1],
                                   args.encrypt[2])
        print(encrypted)
    else:
        server = PaddingOracle(args.decrypt[3])
        decrypted = server.decrypt(args.decrypt[0], args.decrypt[1],
                                   args.decrypt[2])
        print(decrypted)
