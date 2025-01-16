#!/usr/bin/env python3
import subprocess, argparse, os, sys, csv
from datetime import datetime

# ANSI escape codes for color
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automate Hashcat analysis.")
    parser.add_argument("-hf", "--hashfile", required=True, help="Path to file containing password hashes.")
    parser.add_argument("-wl", "--wordlist", required=True, help="Path to dictionary/wordlist.")
    parser.add_argument("-hm", "--hash-mode", default="0", help="Hashcat hash mode, default 0.")
    parser.add_argument("-r", "--rules", default=None, help="Path to a Hashcat rule file.")
    parser.add_argument("-u", "--user", required=True, help="Name of User operating this Script.")
    return parser.parse_args()

def run_hashcat_attack(hashfile, wordlist, hash_mode, rules):
    command = ["hashcat", "-m", hash_mode, "-a", "0", hashfile, wordlist, "--potfile-path", "hashcat.potfile", "--force"]
    if rules:
        command[8:8] = ["-r", rules]
    print("[+] Running dictionary attack...\n")
    process = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout)
    return process.returncode in (0, 1)

def run_hashcat_show(hashfile, hash_mode):
    command = ["hashcat", "-m", hash_mode, "--potfile-path", "hashcat.potfile", "--show", "--force", hashfile]
    print("[+] Retrieving cracked hashes...\n")
    process = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout)
    lines = process.stdout.strip().splitlines()
    return lines if process.returncode in (0, 1) else None

def analyze_password_complexity(password):
    uc = sum(1 for c in password if c.isupper())
    lc = sum(1 for c in password if c.islower())
    dg = sum(1 for c in password if c.isdigit())
    sp = sum(1 for c in password if not c.isalnum())
    return {"length": len(password), "uppercase": uc, "lowercase": lc, "digits": dg, "special": sp}

def analyze_results(cracked_lines, total_hashes):
    if cracked_lines is None:
        return {"cracked": [], "summary": "No results returned (Hashcat error)."}
    cracked = []
    for line in cracked_lines:
        line = line.strip()
        if not line: continue
        parts = line.split(':', 1)
        if len(parts)==2:
            hsh, pwd = parts
            complexity_info = analyze_password_complexity(pwd)
            cracked.append((hsh, pwd, complexity_info))
    num_cracked = len(cracked)
    if num_cracked == 0:
        strength = "STRONG"
    elif num_cracked < (total_hashes / 3):
        strength = "MEDIUM"
    else:
        strength = "WEAK"
    return {"cracked": cracked, "summary": strength}

def export_to_csv(cracked_list, user, analysis_summary):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{user}_{timestamp}.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Hash", "Plaintext", "Length", "Uppercase", "Lowercase", "Digits", "Special", "Strength"])
        for (h, pwd, comp) in cracked_list:
            writer.writerow([h, pwd, comp["length"], comp["uppercase"], comp["lowercase"], comp["digits"], comp["special"], analysis_summary])
    print(f"[+] Results exported to CSV: {csv_filename}")

def main():
    args = parse_arguments()
    if not os.path.isfile(args.hashfile):
        print(f"[!] Hash file not found: {args.hashfile}")
        sys.exit(1)
    if not os.path.isfile(args.wordlist):
        print(f"[!] Wordlist file not found: {args.wordlist}")
        sys.exit(1)
    with open(args.hashfile, "r", encoding="utf-8") as f:
        total_hashes = len([ln for ln in f if ln.strip()])
    if total_hashes == 0:
        print("[!] Hash file is empty.")
        sys.exit(1)
    if not run_hashcat_attack(args.hashfile, args.wordlist, args.hash_mode, args.rules):
        sys.exit(1)
    cracked_lines = run_hashcat_show(args.hashfile, args.hash_mode)
    analysis = analyze_results(cracked_lines, total_hashes)

    # Colorize summary output
    summary_color = RESET
    if analysis['summary'] == "STRONG":
        summary_color = GREEN
    elif analysis['summary'] == "MEDIUM":
        summary_color = YELLOW
    elif analysis['summary'] == "WEAK":
        summary_color = RED

    print("\n==== Strength Analysis ====")
    print(f"Total hashes: {total_hashes}")
    print(f"Cracked hashes: {len(analysis['cracked'])})")
    print(f"Strength Summary: {summary_color}{analysis['summary']}{RESET}\n")

    if analysis['cracked']:
        print("Cracked details:")
        for (h, pwd, comp) in analysis['cracked']:
            print(f"  Hash: {h}")
            print(f"  Plaintext: {pwd}")
            print(f"  Length: {comp['length']}")
            print(f"  Uppercase: {comp['uppercase']}")
            print(f"  Lowercase: {comp['lowercase']}")
            print(f"  Digits: {comp['digits']}")
            print(f"  Special: {comp['special']}")
            print("---")
    else:
        print("[!] No hashes were cracked.")

    export_to_csv(analysis['cracked'], args.user, analysis['summary'])

if __name__ == "__main__":
    main()
