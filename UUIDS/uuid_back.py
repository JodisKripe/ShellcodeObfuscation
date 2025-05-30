with open("d:/Tools/ShellcodeObfuscation/UUIDS/shellcode_uuid.txt", "r") as file:
    UUIDS = file.readlines()
UUIDS = [uuid.strip() for uuid in UUIDS]

def UUIDtoShellcode(UUIDS):
    """
    Convert UUID format back to shellcode.
    """
    shellcode = bytearray()
    for uuid in UUIDS:
        parts = uuid.split('-')
        if len(parts) != 5:
            continue  # Skip invalid UUIDs
        firstblock = bytes.fromhex(parts[0])[::-1]
        secondblock = bytes.fromhex(parts[1])
        thirdblock = bytes.fromhex(parts[2])[::-1]
        fourthblock = bytes.fromhex(parts[3])
        fifthblock = bytes.fromhex(parts[4])
        
        tempshellcode = firstblock + secondblock + thirdblock + fourthblock + fifthblock
        shellcode.extend(tempshellcode)
    
    return shellcode

with open("shellcode_recovered.bin", "wb") as file:
    shellcode = UUIDtoShellcode(UUIDS)
    file.write(shellcode)
    print(f"Recovered shellcode length: {len(shellcode)} bytes")