# This script is used to read a binary file and puts the shellcode through a aes128 function.
def aes_cipher(data, key):
    """Encrypts or decrypts data using AES cipher with a given key."""
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV for decryption

with open('shell_org.bin', "rb") as f:
    shell_org = f.read()
    print(shell_org)

# Multibyte key
key = b'ThisisThatIceCol'  # Example key, must be 16 bytes for AES-128

# Encrypt the shellcode
shell_encrypted = aes_cipher(shell_org, key)
# Write the encrypted shellcode to a file
with open('shell.bin', 'wb') as f:
    f.write(shell_encrypted)