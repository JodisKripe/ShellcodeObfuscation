# This script is used to read a binary file and puts the shellcode through a multibyte key XOR cipher.

def xor_cipher(data, key):
    """Encrypts or decrypts data using XOR cipher with a given key."""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

with open('shell_org.bin', "rb") as f:
    shell_org = f.read()
    print(shell_org)

# Multibyte key
key = [15, 27, 42, 58]  # Example key, can be any byte values

# Encrypt the shellcode
shell_encrypted = xor_cipher(shell_org, key)
# Write the encrypted shellcode to a file
with open('shell.bin', 'wb') as f:
    f.write(shell_encrypted)