
# Tree project (Experimental)
```hyp-gui/
│
├── core/                         # Main package
│   ├── __init__.py               # Makes 'core' a package
|   ├── libs.py                   # Library
|   ├── path.py                   # Separate getPath class
│   ├── algorithms/               # Subpackage with processing logic
│   │   ├── __init__.py
│   │   ├── rgb.py                # RGB class and spectral logic (including SA)
│   │   └── get_path.py           # Separate getPath class
│   │
│   ├── gui/                      # Subpackage for the graphical interface
│   │   ├── __init__.py
│   │   ├── main_window.py        # Main window (PyQt, Tkinter, etc.)
│   │   └── controllers.py        # Event controllers
│   │
│   └── utils/                    # Auxiliary functions
│       ├── __init__.py
│       └── file_utils.py
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_rgb.py
│
├── requirements.txt              # Base dependencies (numpy, PyQt5, etc.)
├── requirements_ai.txt           # AI dependencies (torch, transformers, etc.) 
├── setup.py                      # Optional package installation 
├── run.py                        # Entry script for the GUI 
│ 
├── installer.cpp                 # Main wrapper in C++ 
├── install.sh                    # Installation on Linux/MacOS 
├── install_win.bat               # Installation on Windows 
├── check_ai.py                   # AI resource verification 
│ 
├── Makefile                      # Quick compilation on Linux/MacOS 
├── CMakeLists.txt                # Cross-platform compilation with CMake 
└── build_win.bat                 # Compilation on Windows (MinGW/MSVC)
```