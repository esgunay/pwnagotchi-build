import shutil
import sys
import subprocess
import os
import argparse

MODE = "22000"

RULES_DIRS = ["/usr/share/doc/hashcat/rules", "~/Projects/pwnagotchi/wordlists/rules"]

def require(tool):
    if shutil.which(tool) is None:
        sys.exit(tool + " is not installed or not on PATH. Install it and retry")

def first_existing(paths):
    for p in paths:
        if p:
            p = os.path.expanduser(p)
            if os.path.isfile(p):
                return p
    return None

def rule_path(name):
    return first_existing([os.path.join(d,name) for d in RULES_DIRS])

def build_ladder():
    rockyou = first_existing(["~/Projects/pwnagotchi/wordlists/rockyou.txt"])
    big_list = first_existing(["~/Projects/pwnagotchi/wordlists/kaonashi.txt"])
    stages = []
    if rockyou:
        stages.append(("rockyou", rockyou, None))
        best64= rule_path("best64.rule")
        if best64:
            stages.append(("rockyou + best64 rules", rockyou, best64))
        onerule = rule_path("OneRuleToRuleThemStill.rule")
        if onerule:
            stages.append(("rockyou + OneRule", rockyou, onerule))
    if big_list:
        stages.append(("kaonashi (big list)", big_list, None))
    return stages

def convert(pcap, hashfile):
    print("Converting " + pcap + " -> " + hashfile)
    result = subprocess.run(["hcxpcapngtool", "-o", hashfile, pcap], capture_output = True, text = True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return os.path.isfile(hashfile) and os.path.getsize(hashfile) > 0

def crack(hashfile, wordlist, rules=None):
    cmd = ["hashcat", "-m", MODE, hashfile, wordlist]
    if rules:
        cmd += ["-r", rules]
    print(f"[*] Running: {' '.join(cmd)}\n")
    return subprocess.run(cmd).returncode

def show_results(hashfile):
    result = subprocess.run(["hashcat", "-m", MODE, hashfile, "--show", "--outfile-format", "2"], capture_output=True, text=True)
    return [line for line in result.stdout.splitlines() if line.strip()]

def run_ladder(hashfile, stages):
    for i, (label, wordlist, rules) in enumerate(stages, 1):
        print("\n" + "#" * 52)
        print(f"[*] Stage {i}/{len(stages)}: {label}")
        print("#" * 52)
        crack(hashfile, wordlist, rules)
        results = show_results(hashfile)
        if results:
            print(f"[+] Cracked on stage {i} ({label}) - stopping.")
            return results
        print(f"[-] Stage {i} exhausted, no match. Moving on...")
    return []

def main():
    parser = argparse.ArgumentParser(description = "Convert a pcap and crack it with hashcat")
    parser.add_argument("pcap", nargs="?", help = "path to the .pcap/.pcapng capture")
    parser.add_argument("-w", "--wordlist", default="", help = "wordlist (default: auto-find rockyou)")
    parser.add_argument("-r", "--rules", help = "optional hashcat rules file")
    args = parser.parse_args()

    require("hcxpcapngtool")
    require("hashcat")

    pcap = args.pcap or input("Path to capture file: ").strip()
    if not os.path.isfile(pcap):
        sys.exit("Capture not found: " + pcap)

    if args.wordlist:
        wl = os.path.expanduser(args.wordlist)
        if not os.path.isfile(wl):
            sys.exit("Wordlist not found: " + wl)
        stages = [("custom wordlist", wl, args.rules)]
    else:
        stages = build_ladder()
        if not stages:
            sys.exit("No wordlists found for the ladder.\n")
        print("[*] Ladder stages to run:")
        for i, (label, wl, rules) in enumerate(stages, 1):
            print(f"     {i}. {label}")

    base = os.path.splitext(os.path.basename(pcap))[0]
    hashfile = f"{base}.hc22000"

    ## Step 1: Convert pcap to hash

    if not convert(pcap, hashfile):
        sys.exit("No handshake or PMKID found in capture")

    ## Step 2: Cracking 🤣

    print("[+] Hash extracted. Starting hashcat...\n")
    results = run_ladder(hashfile, stages)

    ## Step 3: report results

    print("\n" + "=" * 52)
    if results:
        print("[+] CRACKED:")
        for r in results:
            print(f"     password: {r}")
    else:
        print("[-] Wordlists exhausted :(")
        print("   Try a different list")
    print("=" * 52)


if __name__ == "__main__":
    main()
