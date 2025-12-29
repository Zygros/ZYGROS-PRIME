import time
import os
import sys

# Function to clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to animate text printing
def animate_line(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')

def main():
    clear_terminal()
    animate_line("✨ Rube Goldberg OS Machine: The Genesis of Data ✨\n", 0.05)
    time.sleep(1)

    # Stage 1: The Genesis of Data
    animate_line("1. Binary Cascade...", 0.05)
    for i in range(10):
        animate_line("".join(['1' if i % 2 == 0 else '0' for i in range(40)]), 0.002)
    time.sleep(1)
    clear_terminal()

    # Stage 2: The Spark of Intelligence
    animate_line("2. The Spark of Intelligence! 💥", 0.05)
    time.sleep(1)
    animate_line("Numbers Evolve: 1, 2, 3...", 0.05)
    for i in range(1, 4):
        animate_line(f"   {i} " * 5, 0.1)
    time.sleep(1)
    clear_terminal()

    # Stage 3: The Birth of Meaning
    animate_line("3. The Birth of Meaning! 💯🥳", 0.05)
    time.sleep(1)
    words = ["BOOT", "KERNEL", "INTERFACE"]
    for word in words:
        animate_line(f"> {word} ", 0.05)
        time.sleep(0.5)
    time.sleep(1)
    clear_terminal()

    # Stage 4: The Construction of Icons
    animate_line("4. The Construction of Icons...", 0.05)
    time.sleep(1)
    animate_line("The words become commands, creating icons!", 0.05)
    icon_map = {
        "FIRE": "🥵",
        "FLIGHT": "🫩",
        "SICKNESS": "🤢🤮",
        "SLEEP": "😴",
        "AWESOME": "😎"
    }
    for word, icon in icon_map.items():
        animate_line(f"[{word}] -> {icon}", 0.05)
        time.sleep(0.5)
    time.sleep(1)
    clear_terminal()

    # Stage 5: The Operating System Ascends
    animate_line("5. The OS Ascends: The Grand Finale", 0.05)
    time.sleep(1)
    final_display = " ".join(icon_map.values())
    animate_line(f"Final OS Display: {final_display}", 0.1)
    time.sleep(2)
    animate_line("\n---", 0.05)
    animate_line("OS Online.", 0.05)
    animate_line("---", 0.05)
    time.sleep(3)
    clear_terminal()
    animate_line("Mission Accomplished! 😲🤯🥳💯💥🥵🤢🤮🤕😷🫩😴😎", 0.05)

if __name__ == "__main__":
    main()
