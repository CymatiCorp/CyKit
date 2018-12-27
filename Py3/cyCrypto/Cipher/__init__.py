import os

from cyCrypto.Cipher._mode_ecb import _create_ecb_cipher

_modes = { 1:_create_ecb_cipher }

def _create_cipher(factory, key, mode, *args, **kwargs):

    kwargs["key"] = key

    modes = dict(_modes)
    if kwargs.pop("add_aes_modes", False):
        pass
        
    if mode not in modes:
        raise ValueError("Mode not supported")

    if args:
        if mode in (8, 9, 10, 11, 12):
            if len(args) > 1:
                raise TypeError("Too many arguments for this mode")
            kwargs["nonce"] = args[0]
        elif mode in (2, 3, 5, 7):
            if len(args) > 1:
                raise TypeError("Too many arguments for this mode")
            kwargs["IV"] = args[0]
        elif mode == 6:
            if len(args) > 0:
                raise TypeError("Too many arguments for this mode")
        elif mode == 1:
            raise TypeError("IV is not meaningful for the ECB mode")

    return modes[mode](factory, **kwargs)
