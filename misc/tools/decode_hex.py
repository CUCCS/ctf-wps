import binascii

hex_str = '4c69744354467b746169313131636f6f6c6c616161217d'

print(binascii.unhexlify(hex_str).decode('utf-8'))
