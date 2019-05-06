# Usage
TODO


# Installing

To setup, you need to install [PyCryptoDome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html).

*Warning*: PyCryptoDome comes with two versions. This project uses **pycryptodomex**. You MUST install it in a virtual environment. 
Here is my setup on Linux:

```
python3 -m venv venv/
source venv/bin/active
pip install pycryptodomex
python -m Cryptodome.SelfTest
```

