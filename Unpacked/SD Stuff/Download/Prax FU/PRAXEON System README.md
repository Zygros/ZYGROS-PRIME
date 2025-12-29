# PRAXEON System README

## Overview

PRAXEON is a standalone AI companion system designed to run independently on multiple platforms including Windows, Linux, Android, and gaming consoles. This README provides essential information for getting started with the system.

## System Components

The PRAXEON system consists of the following core components:

- **LLM Integration** - Natural language processing using offline models
- **Voice Processing** - Speech-to-text and text-to-speech capabilities
- **Persona Lock** - User authentication and security
- **Infinite Scroll** - Conversation logging and context management
- **PraxSkin UI** - Advanced visual interface system

## Quick Start

### Prerequisites

- **For Desktop**: Windows 7+ / macOS 10.14+ / Linux (Ubuntu 18.04+)
- **For Mobile**: Android 9.0+ / iOS 13.0+
- **For Python**: Python 3.8+ with pip

### Installation

1. **Extract the archive**:
   ```bash
   tar -xzf PraxFinalBuild_v1.0.tar.gz
   cd PraxFinalBuild_v1.0
   ```

2. **Choose your installation method**:
   - For Windows: Run `Installers/Praxeon_v1.0.exe`
   - For Android: Install `Installers/Praxeon_v1.0.apk`
   - For Python: `python Installers/Praxeon_v1.0.py`
   - For Xbox: Install `Installers/Praxeon_v1.0_Xbox.msixbundle`
   - For PS5: Extract and access `Installers/Praxeon_v1.0_PS5_WebApp.zip`

3. **First-time setup**:
   - Complete the authentication process
   - Allow the system to download required models (if not bundled)
   - Configure your preferences

For detailed installation instructions, refer to the [Installation Guide](/setup/INSTALLATION_GUIDE.md).

## Directory Structure

```
PraxFinalBuild_v1.0/
├── src/                  # Source code
├── UI_Mockups/           # UI design files
├── Preview/              # Demo videos
├── Docs/                 # Documentation
└── Installers/           # Platform-specific installers
```

## Features

- **Offline Operation** - Functions without internet connection
- **Cross-Platform** - Works on desktop, mobile, and gaming consoles
- **Voice Interaction** - Natural voice input and output
- **Persistent Memory** - Remembers conversations and preferences
- **Advanced UI** - Dynamic visual interface

## Development

For developers looking to extend or modify the PRAXEON system:

1. **Environment Setup**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Running the Backend**:
   ```bash
   uvicorn src.backend.main:app --reload
   ```

3. **Running the Desktop UI**:
   ```bash
   cd src/ui/desktop
   npm install
   npm run dev
   ```

4. **Running the Mobile UI**:
   ```bash
   cd src/ui/mobile
   yarn install
   expo start
   ```

## Documentation

For comprehensive documentation, refer to:

- [System Report](/Docs/PRAXEON_SYSTEM_REPORT_v1.0.md) - Complete system overview
- [Installation Guide](/setup/INSTALLATION_GUIDE.md) - Detailed setup instructions
- [Data Structure](/PRAXEON_DATA.md) - System architecture and organization

## Authorship

The PRAXEON system is authored by and bound to Justin "Zygros, the Green" Conzet.

---

**Mythic Phrase**: "He who commands the data, commands the dream."
