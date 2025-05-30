# read shellcode

def ShellcodetoUUID(shellcode):
    """
    Convert shellcode to UUID format.
    """
    blocksize = 16
    shellcode = bytearray(shellcode)
    shellcode += b'\x90' * (blocksize - len(shellcode) % blocksize)
    # format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    UUIDS = []
    UUID_SIZE= 16
    for i in range(0, len(shellcode), UUID_SIZE):
        tempshellcode = shellcode[i:i + UUID_SIZE]
        if len(tempshellcode) < UUID_SIZE:
            tempshellcode += b'\x90' * (UUID_SIZE - len(tempshellcode))
        firstblock = tempshellcode[:4][::-1]
        secondblock = tempshellcode[4:6]
        thirdblock = tempshellcode[6:8][::-1]
        fourthblock = tempshellcode[8:10]
        fifthblock = tempshellcode[10:16]
        UUID = f"{firstblock.hex()}-{secondblock.hex()}-{thirdblock.hex()}-{fourthblock.hex()}-{fifthblock.hex()}"
        UUIDS.append(UUID)

    return UUIDS

with open("shell_org.bin", "rb") as file:
    shellcode = file.read()

UUIDS = ShellcodetoUUID(shellcode)

with open("shellcode_uuid.txt", "w") as file:
    for i, uuid in enumerate(UUIDS):
        print(f"{uuid}")
        file.write(f"{uuid}\n")
