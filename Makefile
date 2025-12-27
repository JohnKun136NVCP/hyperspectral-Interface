# Makefile for building the installer
CXX = g++
CXXFLAGS = -std=c++17 -O2
TARGET = installer

all: $(TARGET)

$(TARGET): installer.cpp
    $(CXX) $(CXXFLAGS) installer.cpp -o $(TARGET)

clean:
    rm -f $(TARGET)
