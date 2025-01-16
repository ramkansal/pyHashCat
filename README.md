# Hashcat Automation Script

## Overview
This repository provides a Python script (`hashcat_automation.py`) that automates the process of running a Hashcat dictionary attack, analyzing password complexity, and optionally exporting the results to a CSV file. The script performs two main steps:
1. Runs Hashcat to crack password hashes and prints the full output.
2. Retrieves and analyzes cracked hashes, reporting complexity details and strength summary.

## Features
- **Automated Hashcat Execution:** Runs dictionary attacks using Hashcat with optional rule-based modifications.
- **Full Output Display:** Prints Hashcat’s standard output during attack and result retrieval.
- **Password Complexity Analysis:** For each cracked password, counts uppercase letters, lowercase letters, digits, and special characters.
- **CSV Export:** Optionally export cracked password details along with complexity statistics to a timestamped CSV file.
- **Easy Installation:** An `install.sh` script sets up dependencies, fetches the code from a remote repository, and prepares the environment.

## Requirements
- Linux (Debian/Ubuntu-based system recommended)
- [Hashcat](https://hashcat.net/hashcat/)
- Python 3.x
- `git` (if cloning the repository via the install script)

## Installation

### Using the Provided `install.sh`
If you want to automatically install dependencies and fetch the Python script from a remote repository, use the provided `install.sh`:

1. **Edit the Installation Script (Optional):**
   - Open `install.sh` and update the `REPO_URL` and `CLONE_DIR` variables to point to your repository and desired directory name, if necessary.

2. **Make the Install Script Executable and Run It:**
   ```bash
   chmod +x install.sh
   ./install.sh

## Uninstallation

To remove the cloned repository and associated scripts installed by the `install.sh` script, use the provided `uninstall.sh`:

1. Ensure you are in the same directory where `uninstall.sh` is located.
2. Make the uninstall script executable (if not already):
   ```bash
   chmod +x uninstall.sh
