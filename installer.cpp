#include <iostream>
#include <cstdlib>

#if defined(_WIN32) || defined(_WIN64)
#define WINDOWS true
#else
#define WINDOWS false
#endif
using namespace std;

bool isVirtualEnv() {
    const char* venv = getenv("VIRTUAL_ENV");
    return venv != nullptr;
}

int main() {
    cout << "=== Hyp-GUI Installer ===" << std::endl;

    if (isVirtualEnv()) {
        cout << "[OK] Virtual Enviroment detected." << std::endl;
    } else {
        cout << "[!] Warning: Virtual Enviroment not installed." << std::endl;
        if (WINDOWS) {
            cout << "Running script for Windows..." << std::endl;
            int ret = system("install_win.bat");
            if (ret!= 0){
                cerr<<"Error to run install_win.bat";
                return -1;
            }
        } else {
            cout<< "Running script for Linux/MacOSX" << std::endl;
            int ret = system("bash install.sh");
            if (ret!=0){
                cerr<< "Error to run install.sh"<<endl;
                return -1;
            }
        }
    }

    cout << "Do you want to install AI features? (y/n): ";
    char choice;
    cin >> choice;

    if (choice == 'y' || choice == 'Y') {
        cout << "Checking AI capabilities..." << endl;
        int ret = system("python check_ai.py");
        if (ret != 0) {
            cerr << "Your system does not meet the AI requirements." << endl;
            return 1;
        }
        ret = system("pip3 install -r requirements_ai.txt");
        if (ret != 0) {
            cerr << "Error installing AI requirements." << endl;
            return 1;
        }
    }

    return 0;
}