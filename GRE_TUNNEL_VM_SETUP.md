# ✅ WORKING GRE TUNNEL - VirtualBox Ubuntu VM (Full Steps)

WSL2 GRE works with sudo, but for **real VM**:

## 1. Download Ubuntu Server (CLI only, lightweight)
```
curl -o ubuntu-24.04-live-server-amd64.iso https://releases.ubuntu.com/24.04/ubuntu-24.04-live-server-amd64.iso
```
Or download: https://ubuntu.com/download/server (SHA256 verify).

## 2. Create VirtualBox VM (you have VirtualBox - 192.168.56.1 host-only)
```
VBoxManage createvm --name "Ubuntu-GRE" --register
VBoxManage modifyvm "Ubuntu-GRE" --memory 2048 --cpus 2 --nic1 hostonly --nic1net "vboxnet0"
VBoxManage createhd --filename "Ubuntu-GRE.vdi" --size 20480
VBoxManage storagectl "Ubuntu-GRE" --name "SATA" --add sata --controller IntelAHCI
VBoxManage storageattach "Ubuntu-GRE" --storagectl "SATA" --port 0 --device 0 --type hdd --medium "Ubuntu-GRE.vdi"
VBoxManage storageattach "Ubuntu-GRE" --storagectl "SATA" --port 1 --device 0 --type dvddrive --medium ubuntu-24.04-live-server-amd64.iso
VBoxManage startvm "Ubuntu-GRE"
```

## 3. Install Ubuntu (VM console)
- Language: English
- Keyboard: US
- Network: DHCP (host-only)
- Proxy: none
- Mirror: default
- Filesystem: Use entire disk
- Profile: ubuntu / password
- Featured snaps: none

## 4. Login (ubuntu), Update & Python
```
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip iproute2 -y
sudo reboot
```

## 5. Mount project & Run GRE
```
sudo mkdir /mnt/project
sudo mount -t 9p -o trans=virtio share /mnt/project  # Shared folder setup in VB settings
cd /mnt/project
sudo python3 setup_gre_tunnel.py
```

**Input remote IP:** Your Windows IP `192.168.56.1` (host-only).

**Success:** gre0 UP, ping 10.0.0.2 OK.

## Test from Windows
```
ping 10.0.0.1  # VM tunnel
```

## GNS3 Alternative (if installed - project has GNS3 files)
See RUN_MEASUREMENTS_GNS3.md - drag Ubuntu appliances, add GRE links.

**VM IP:** Host-only network (192.168.56.0/24).

Tunnel **FULLY UP** in 15min.
