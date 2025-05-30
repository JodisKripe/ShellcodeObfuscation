import os

# This script is used to read a binary file and puts the shellcode through caesar cipher shift.


# Caesar cipher shift
def caesar_cipher(data, shift):
    return bytearray((byte + shift) % 256 for byte in data)

with open('shell_org.bin',"rb") as f:
    shell_org = f.read()
    print(shell_org)

# Shift value
shift_value = 15

# Encrypt the shellcode
shell_encrypted = caesar_cipher(shell_org, shift_value)
# Write the encrypted shellcode to a file
with open('shell.bin', 'wb') as f:
    f.write(shell_encrypted)
