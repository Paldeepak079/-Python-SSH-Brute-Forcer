# Python SSH Lab Credential Tester & Metasploitable 2

Educational security-lab project documenting an SSH credential-validation exercise and service enumeration against an intentionally vulnerable Metasploitable 2 VM.

> **Authorized use only:** use these materials only on systems you own or have explicit permission to test.

## Lab
- Attacker: Kali Linux
- Target: Metasploitable 2
- SSH service: TCP/22
- Objective: validate SSH access, troubleshoot legacy SSH compatibility, and enumerate exposed services.

## Workflow
1. Configure Metasploitable 2 in an isolated VMware network.
2. Validate connectivity from Kali.
3. Discover SSH with Nmap.
4. Validate SSH access and document legacy RSA compatibility.
5. Enumerate exposed services with Nmap.
6. Inspect FTP, SMB, NFS and web resources in the isolated lab.

## Evidence
See the enumeration notes and screenshots directory.

## Safety
This repository should not contain real-world credentials, private keys, sensitive wordlists, or data taken from systems outside the lab.