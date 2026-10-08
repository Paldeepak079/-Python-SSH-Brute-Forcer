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
# Metasploitable 2 SSH Lab — Step-by-Step
<img width="1061" height="582" alt="image" src="https://github.com/user-attachments/assets/d30d17b1-aa0c-4ade-979c-c908a4ee82fa" />
<img width="1193" height="584" alt="image" src="https://github.com/user-attachments/assets/7a9cd0c3-5c76-4a8e-a45a-e1e0617e4d80" />
<img width="1236" height="655" alt="image" src="https://github.com/user-attachments/assets/8782de96-9d28-4da1-8cac-2d41262f8531" />



## 1. VMware setup
Run Kali Linux and Metasploitable 2 on an isolated lab network. Do not expose Metasploitable 2 to an untrusted network.

## 2. Find the target IP
On Metasploitable:
```bash
ifconfig
```
Example used in this lab: `192.168.207.131`
<img width="568" height="188" alt="image" src="https://github.com/user-attachments/assets/a2c76041-6782-464f-9a7b-f24e86e3e92b" />

## 3. Validate connectivity
From Kali: <img width="555" height="234" alt="image" src="https://github.com/user-attachments/assets/b4ecf817-82b9-4f14-af29-944b85546b89" />

```bash
ping -c 4 192.168.207.131
```

## 4. Discover SSH
```bash
nmap -p 22 192.168.207.131
<img width="752" height="418" alt="image" src="https://github.com/user-attachments/assets/92f0516f-ceb4-4248-bc47-c511a13c8935" />
```

## 5. Handle legacy SSH
Metasploitable 2 is an old training VM. For its legacy RSA host key:
```bash
ssh -o HostKeyAlgorithms=+ssh-rsa msfadmin@192.168.207.131
```
<img width="752" height="418" alt="image" src="https://github.com/user-attachments/assets/5fc68f26-0c03-4cf0-aa15-546fc724763a" />


## 6. Validate the known lab credential
Credential used by the Metasploitable training VM:
`msfadmin / msfadmin`

```bash
sshpass -p 'msfadmin' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o HostKeyAlgorithms=+ssh-rsa -o ConnectTimeout=5 msfadmin@192.168.207.131
```

## 7. Install sshpass
```bash
sudo apt update
sudo apt install sshpass
```
<img width="1233" height="292" alt="image" src="https://github.com/user-attachments/assets/23e6f1da-a840-4d36-9b7b-9b9c0627c4c9" />

## 8. Run the Python tool
```bash
python3 scripts/ssh_lab_credential_test.py -t 192.168.207.131 -p 22 -u msfadmin -P msfadmin
```
<img width="644" height="266" alt="image" src="https://github.com/user-attachments/assets/f521b6bd-3883-4adf-bacf-fae0c0211b38" />

Expected:
```text
[+] SUCCESS
[+] Username : msfadmin
[+] Password : msfadmin
```

## 9. Full enumeration
```bash
nmap -sC -sV -O 192.168.207.131
```

## 10. FTP
```bash
ftp 192.168.207.131
```
<img width="429" height="266" alt="image" src="https://github.com/user-attachments/assets/5bcb1777-f091-4a3f-bc57-b072d063a6b9" />

Anonymous access was confirmed in the lab.

## 11. SMB
```bash
smbclient -L //192.168.207.131 -N
```
<img width="1138" height="439" alt="image" src="https://github.com/user-attachments/assets/0a9ebe65-1969-4254-a9d0-1c45b2e985d3" />

Observed shares included `print$`, `tmp`, `opt`, `IPC$`, and `ADMIN$`.

## 12. NFS
```bash
showmount -e 192.168.207.131
sudo mount -t nfs -o vers=3 192.168.207.131:/ /mnt
ls -la /mnt
sudo umount /mnt
```
<img width="898" height="442" alt="image" src="https://github.com/user-attachments/assets/cb15101a-af2c-4cdf-b18e-08c6acf68b2a" />

Do not modify target data.

## 13. Web enumeration
Open:
- http://192.168.207.131/
- http://192.168.207.131/dvwa/
- http://192.168.207.131/mutillidae/
- http://192.168.207.131/phpMyAdmin/
- http://192.168.207.131/phpinfo.php
<img width="577" height="787" alt="image" src="https://github.com/user-attachments/assets/96a5d1f9-d141-42e6-b9f4-7e6b86ebad7f" />

Optional:
```bash
nikto -h http://192.168.207.131
