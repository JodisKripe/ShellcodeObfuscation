import os

# This script is used to read a binary file and puts the shellcode through xor shift.


# XOR shift
def xor_cipher(data, key):
    """Encrypts or decrypts data using XOR cipher with a given key."""
    return bytes([b ^ key for b in data])

with open('shell_org.bin',"rb") as f:
    shell_org = f.read()
    print(shell_org)

# Shift value
shift_value = 15

# Encrypt the shellcode
shell_encrypted = xor_cipher(shell_org, shift_value)
# Write the encrypted shellcode to a file
with open('shell.bin', 'wb') as f:
    f.write(shell_encrypted)
