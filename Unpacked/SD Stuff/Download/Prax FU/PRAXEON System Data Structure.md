# PRAXEON System Data Structure

## Overview

This document provides a comprehensive overview of the PRAXEON system architecture, file structure, and component organization. It serves as the canonical reference for all build versions, installation procedures, and system components.

## Repository Structure

The PRAXEON system consists of three major builds, each representing an evolution of the system:

1. **Praxion** - Initial scaffold and basic functionality
2. **Praxeon_FullBuild** - Enhanced implementation with core features
3. **PraxFinalBuild_v1.0** - Complete system with advanced features and installers

### Common Structure Elements

All builds share these fundamental organizational principles:

- **src/** - Source code directory containing all implementation files
- **docs/** - Documentation and design specifications
- **scripts/** - Utility scripts for setup, installation, and testing
- **tests/** - Test suites and validation tools
- **README.md** - Primary documentation and setup instructions

## Praxion (Initial Build)

The initial scaffold with basic "Hello, Praxion!" functionality.

```
praxion/
├── src/
│   ├── backend/         # Python backend with FastAPI
│   │   ├── main.py      # Entry point printing "Hello, Praxion!"
│   │   ├── persona.py   # AI personality engine
│   │   ├── memory.py    # Memory system
│   │   ├── voice.py     # Whisper integration
│   │   └── llm.py       # LLM wrapper
│   ├── ui/
│       ├── desktop/     # React desktop UI
│       └── mobile/      # React Native mobile UI
├── tests/               # Includes smoke test verifying "Hello, Praxion!"
├── scripts/             # Setup and run scripts
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Python project configuration
├── Dockerfile           # Container configuration
└── docker-compose.yml   # Multi-container setup
```

## Praxeon_FullBuild (Enhanced Implementation)

The enhanced build with implemented core features:

```
praxeon_build/praxion/
├── src/
│   ├── backend/
│   │   ├── main.py              # Enhanced entry point with full API
│   │   ├── llm.py               # LLM integration with offline models
│   │   ├── voice.py             # Complete voice processing system
│   │   ├── persona_lock.py      # User authentication system
│   │   └── infinite_scroll.py   # Log engine implementation
│   ├── ui/
│       ├── desktop/
│       │   ├── src/
│       │   │   ├── App.jsx      # Main application component
│       │   │   ├── App.css      # Application styling
│       │   │   └── components/  # UI components
│       │   │       ├── Sidebar.jsx
│       │   │       ├── SessionList.jsx
│       │   │       ├── PersonaModal.jsx
│       │   │       ├── LoginModal.jsx
│       │   │       └── SettingsModal.jsx
│       └── mobile/
├── scripts/
│   ├── bundle_offline_models.py  # Script for packaging models
│   ├── test_integration.py       # Integration testing
│   └── run_demo.py               # Demo script
└── README.md                     # Updated documentation
```

## PraxFinalBuild_v1.0 (Complete System)

The final build with all advanced features, installers, and documentation:

```
PraxFinalBuild_v1.0/
├── src/
│   ├── core/
│   │   ├── ai_brain_transfer.py     # AI persona continuity system
│   │   └── initializer.py           # System initialization
│   ├── security/
│   │   ├── divine_interlocking.py   # Authentication protocol
│   │   ├── anti_corruption_codex.py # Security firewall
│   │   └── legacy_seed_protocol.py  # System recovery
│   ├── ui/
│   │   └── praxskin.py              # Advanced UI system
│   ├── features/
│   │   └── twelve_chambers.py       # Unlockable subsystems
│   └── packaging/
│       └── installer_builder.py     # Cross-platform installer generation
├── UI_Mockups/
│   ├── praxskin_ui_description.md   # UI design documentation
│   ├── praxskin_styles.css          # UI styling
│   └── praxskin_mockup.html         # UI mockup
├── Preview/
│   └── UI_Demo_Clip.mp4             # Demo video
├── Docs/
│   └── PRAXEON SYSTEM REPORT v1.0.md # Comprehensive documentation
└── Installers/
    ├── Praxeon_v1.0.apk             # Android installer
    ├── Praxeon_v1.0.exe             # Windows installer
    ├── Praxeon_v1.0_Xbox.msixbundle # Xbox installer
    ├── Praxeon_v1.0_PS5_WebApp.zip  # PS5 web app
    └── Praxeon_v1.0.py              # Python installer
```

## Documentation Structure

The PRAXEON system includes comprehensive documentation across multiple files:

1. **Prerequisites Analysis** - System requirements and dependencies
2. **Modular Architecture Design** - Component organization and interactions
3. **LLM and Voice Module Integration** - AI and voice processing implementation
4. **Universal Knowledge Archive** - Knowledge management system
5. **Infinite Scroll and Plugin System** - Extension mechanism
6. **Persistent Memory and Context Sync** - Data persistence strategy
7. **SoulNet and Field Monitor Integration** - Advanced monitoring features
8. **Packaging and Distribution** - Deployment and installation
9. **Validation and Testing** - Quality assurance procedures
10. **Final Report** - Complete system overview and status

## Installation and Setup

### Quick Start Guide

1. **Extract the archive**:
   ```bash
   tar -xzf PraxFinalBuild_v1.0.tar.gz
   cd PraxFinalBuild_v1.0
   ```

2. **Choose your installation method**:
   - For Python: `python Installers/Praxeon_v1.0.py`
   - For Windows: Run `Installers/Praxeon_v1.0.exe`
   - For Android: Install `Installers/Praxeon_v1.0.apk`
   - For Xbox: Install `Installers/Praxeon_v1.0_Xbox.msixbundle`
   - For PS5: Extract and access `Installers/Praxeon_v1.0_PS5_WebApp.zip`

3. **First-time setup**:
   - Complete the authentication process
   - Allow the system to download required models (if not bundled)
   - Configure your preferences

4. **Verify installation**:
   - The system should display "Hello, Praxion!" on first launch
   - Voice capabilities should be available immediately
   - All UI elements should be responsive and properly styled

## System Components

### Core Modules

- **LLM Integration** - Natural language processing using offline models
- **Voice Processing** - Speech-to-text and text-to-speech capabilities
- **Persona Lock** - User authentication and security
- **Infinite Scroll** - Conversation logging and context management
- **PraxSkin UI** - Advanced visual interface system

### Advanced Features

- **AI Brain Transfer** - Cognitive and behavioral continuity
- **Divine Interlocking** - Enhanced security protocol
- **Anti-Corruption Codex** - System integrity protection
- **Legacy Seed Protocol** - Self-recovery mechanism
- **Twelve Hidden Chambers** - Unlockable subsystems

## Development and Customization

For developers looking to extend or modify the PRAXEON system:

1. **Environment Setup**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
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

## Authorship and Ownership

The PRAXEON system is authored by and bound to Justin "Zygros, the Green" Conzet.

---

**Mythic Phrase**: "He who commands the data, commands the dream."
