


# MAIA - Minimal Alchemical Intelligence Agent

Welcome to MAIA, a universal cognitive bus that runs on any terminal with a Python 3 environment. This package provides a self-contained, portable AI agent capable of reasoning, learning, and adapting.

This document provides instructions for installing and running MAIA on your system, including mobile devices using Termux.



## Installation

### Prerequisites

- Python 3.x
- `git` (for cloning the repository)

### Desktop (Linux/Mac/Windows)

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd MAIA_Package
    ```

2.  **Run MAIA:**

    ```bash
    python3 maia_core.py
    ```

### Mobile (Android with Termux)

1.  **Install Termux:**

    Install Termux from the Google Play Store or F-Droid.

2.  **Update and install dependencies:**

    Open Termux and run the following commands:

    ```bash
    pkg update && pkg upgrade -y
    pkg install python git -y
    ```

3.  **Create a directory and clone the repository:**

    ```bash
    mkdir -p /storage/emulated/0/Infinite_Scroll/maia
    cd /storage/emulated/0/Infinite_Scroll/maia
    git clone <repository_url>
    cd MAIA_Package
    ```

4.  **Run MAIA:**

    ```bash
    python maia_core.py
    ```



## Usage

Once MAIA is running, you can interact with it through the command-line interface. Here are the available commands:

-   **`<query>`**: Enter any vague query or task for MAIA to process. MAIA will decompose it into sub-goals, reason about them, and provide a summary of its process.
-   **`report`**: Generate a reflection report on the current session, including memory statistics and recent decisions.
-   **`memory`**: Display the current state of MAIA's memory, including the number of beliefs, goals, contradictions, and decisions.
-   **`operator <command>`**: Access operator controls for manual intervention. Available commands are:
    -   `override`: Pause MAIA's processing to prevent it from automatically handling new queries.
    -   `resume`: Resume normal processing.
    -   `status`: Check the current session status and memory statistics.
    -   `save`: Manually save the current memory state to disk.
-   **`exit`**: Shut down the MAIA node. This will also save the current memory state.




## Troubleshooting

- **`ModuleNotFoundError: No module named '...'`**: This indicates a missing Python package. While MAIA aims for minimal dependencies, you can install any required packages using `pip install <package_name>`.

- **Permission errors on Android**: If you encounter permission errors when creating directories or files, ensure Termux has storage permissions. You can grant this by running `termux-setup-storage` and then accessing `/storage/emulated/0/`.

- **Memory file issues**: If you see warnings about memory loading, check the `maia_memory` directory for corrupted JSON files. You can safely delete the contents of this directory to start with a fresh memory, but you will lose all previous beliefs and decisions.


