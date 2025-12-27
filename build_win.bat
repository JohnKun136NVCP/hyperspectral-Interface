@echo off
echo  === Building installer (Windows) ===
g++ -std=c++17 -O2 installer.cpp -o installer.exe
if %errorlevel% neq 0 (
    echo Error during compilation.
    exit /b %errorlevel%
)
echo CCompilation successful. Deploing installer.exe...
