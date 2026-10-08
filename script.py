#!/usr/bin/env python3

import argparse
import subprocess
import sys


def test_ssh(host, port, username, password, timeout=5):
    command = [
        "sshpass",
        "-p", password,
        "ssh",
        "-p", str(port),
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "HostKeyAlgorithms=+ssh-rsa",
        "-o", "ConnectTimeout=5",
        f"{username}@{host}",
        "exit"
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=timeout + 2
        )

        if result.returncode == 0:
            return True

        print(
            result.stderr.decode(errors="ignore").strip()
        )
        return False

    except subprocess.TimeoutExpired:
        print("[!] Connection timed out.")
        return False

    except FileNotFoundError:
        print("[!] sshpass is not installed.")
        print("    sudo apt install sshpass")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="SSH credential tester for an authorized lab"
    )

    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--port", type=int, default=22)
    parser.add_argument("-u", "--user", required=True)
    parser.add_argument("-P", "--password", required=True)
    parser.add_argument("--timeout", type=int, default=5)

    args = parser.parse_args()

    print("=" * 45)
    print("       SSH LAB CREDENTIAL TEST")
    print("=" * 45)
    print(f"[*] Target   : {args.target}:{args.port}")
    print(f"[*] Username : {args.user}")
    print()

    result = test_ssh(
        args.target,
        args.port,
        args.user,
        args.password,
        args.timeout
    )

    if result:
        print("[+] SUCCESS")
        print(f"[+] Username : {args.user}")
        print(f"[+] Password : {args.password}")
    else:
        print("[-] Authentication failed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Stopped.")
        sys.exit(130)
