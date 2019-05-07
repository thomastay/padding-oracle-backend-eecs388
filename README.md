# Introduction

This module implements a local version of the EECS 388 padding oracle website, which allows you to perform easy prototyping and testing for your padding oracle projects.

For those unfamiliar, a padding oracle attack is a side-channel cryptographic attack on the AES encryption cipher, in which a server that leaks information about the validity of padding information inadvertently allows a message to be decrypted. 

[EECS 388](https://eecs388.org) is the undergraduate security class at the University of Michigan - Ann Arbor.

This project is not approved or affliated with the EECS 388 department, it is an independent project.

## Why did you do this?

Because when I was working on the padding oracle for project 1, the server often was down during critical periods. Moreover, it is slow, and when doing rapid prototyping (especially in Python), it is easy to make mistakes. This wastes time and I want to fix this for future batches.

## Cool, does this mean I don't need to do the project and I can crack the ciphertext given to us?

Nope. This module does not know what the EECS388 shared key is, and even once you crack the ciphertext, AES is immune to known plaintext attacks. Do your homework, man.

# Usage

This module is meant to be a drop-in replacement for the padding oracle server. Simply define the following local version of the valid padding function instead of the server one:

```
from PaddingOracle import PaddingOracle, PaddingOracleError

def valid_padding(sender, recipient, query):
    oracle = PaddingOracle("DEADBEEFPOTATATO")    # Change this to your secret key!
    decrypt_val = oracle.decrypt(sender, recipient, query)
    if decrypt_val is PaddingOracle.DecryptBehavior.INVALID_PADDING:
        # This is a padding error
        return 0
    elif decrypt_val is PaddingOracle.DecryptBehavior.INVALID_VALIDATION:
        # Correct padding but incorrect hash.
        return 1
    elif decrypt_val is PaddingOracle.DecryptBehavior.VALID_VALIDATION:
        # Correct padding and correct hash!
        return 1
    else:
        raise PaddingOracleError("something went wrong")
```

In the above function, you need to change _DEADBEEFPOTATATO_ to your own secret key that you used for encryption (see below).

## Making your own encrypted messages to self test

Run this command in the source directory:

```
python PaddingOracle/PaddingOracle.py -e [$from] [$to] [$message] [$key]
```

where you would replace $from with whatever sender you want to

This will print an encrypted message, for instance here is my output (the dollar sign denotes my input):

```
$ python PaddingOracle/PaddingOracle.py -e thomas 388staff welovesteve DEADBEEFPOTATATO

50C76E200370B6273956BE404854B829EF889E76E8C0F10F13641D193C3B71B8689DF7B0971DA8542BEBAC43ABB17AB9
```

Now, update the secret key in the valid padding function in your own padding oracle.

Lastly, run your own padding oracle script (placed in the source folder)

```
python padding_oracle.py thomas 388staff 50C76E200370B6273956BE404854B829EF889E76E8C0F10F13641D193C3B71B8689DF7B0971DA8542BEBAC43ABB17AB9
```

Done!

_Note_: I assume you are running the padding oracle script in the folder just one level above the PaddingOracle folder.


# Installing

To setup, you need to install [PyCryptoDome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html).

This project is built in python3, but nothing about it is required for python3; it should work fine in python2.

*Warning*: PyCryptoDome comes with two versions. This project uses **pycryptodomex**. You might want to install it in a virtual environment. 

Then, git clone this project.

Here is my setup on Linux:

```
git clone git@github.com:thomastay/padding-oracle-backend-eecs388.git
cd padding-oracle-backend-eecs388
python3 -m venv venv/
source venv/bin/activate
pip install pycryptodomex
python -m Cryptodome.SelfTest
```

Lastly, copy your padding oracle.py script into the padding-oracle-eecs-388 folder, and start testing!

