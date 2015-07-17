#define _WIN32_WINNT 0x0500
#include <windows.h>
int main()
{
    SetConsoleTitle("The Wireshark Network Analyzer");
    HWND hWnd = GetConsoleWindow();
    ShowWindow( hWnd, SW_HIDE );
    while (1 == 1) {
        Sleep(60000*60);
    }
    return 1;
}
