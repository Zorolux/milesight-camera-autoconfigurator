# Configuration Examples

## Example 1: Default Configuration (Recommended)

### PowerShell
```powershell
.\milesight-camera-config.ps1
```

### Python
```bash
python3 milesight-camera-config.py
```

**Result:**
- Initial IP: 192.168.5.190
- Final IP: 192.168.100.101
- Password: wordbypass
- Security Answers: Q, A, Z

---

## Example 2: Custom IP Range (192.168.1.x)

### PowerShell
```powershell
.\milesight-camera-config.ps1 -CameraInitialIP "192.168.1.190" `
                               -FinalCameraIP "192.168.1.101"
```

### Python
```bash
python3 milesight-camera-config.py \
    --initial-ip 192.168.1.190 \
    --final-ip 192.168.1.101
```

---

## Example 3: Custom Password

### PowerShell
```powershell
.\milesight-camera-config.ps1 -AdminPassword "MySecurePassword123!"
```

### Python
```bash
python3 milesight-camera-config.py --password "MySecurePassword123!"
```

---

## Example 4: Custom Security Answers

### PowerShell
```powershell
.\milesight-camera-config.ps1 -SecurityQ1Answer "MyAnswer1" `
                               -SecurityQ2Answer "MyAnswer2" `
                               -SecurityQ3Answer "MyAnswer3"
```

### Python
```bash
python3 milesight-camera-config.py \
    --q1-answer "MyAnswer1" \
    --q2-answer "MyAnswer2" \
    --q3-answer "MyAnswer3"
```

---

## Example 5: Full Custom Configuration

### PowerShell
```powershell
.\milesight-camera-config.ps1 -CameraInitialIP "192.168.5.190" `
                               -FinalCameraIP "10.0.0.50" `
                               -AdminPassword "Admin@2024" `
                               -SecurityQ1Answer "Answer1" `
                               -SecurityQ2Answer "Answer2" `
                               -SecurityQ3Answer "Answer3"
```

### Python
```bash
python3 milesight-camera-config.py \
    --initial-ip 192.168.5.190 \
    --final-ip 10.0.0.50 \
    --password "Admin@2024" \
    --q1-answer "Answer1" \
    --q2-answer "Answer2" \
    --q3-answer "Answer3" \
    --subnet "255.255.255.0" \
    --gateway "10.0.0.1"
```

---

## Example 6: Multiple Cameras in Sequence

### PowerShell
```powershell
# Camera 1
.\milesight-camera-config.ps1 -FinalCameraIP "192.168.100.101"

# Camera 2
.\milesight-camera-config.ps1 -FinalCameraIP "192.168.100.102"

# Camera 3
.\milesight-camera-config.ps1 -FinalCameraIP "192.168.100.103"
```

### Python
```bash
# Camera 1
python3 milesight-camera-config.py --final-ip 192.168.100.101

# Camera 2
python3 milesight-camera-config.py --final-ip 192.168.100.102

# Camera 3
python3 milesight-camera-config.py --final-ip 192.168.100.103
```

---

## Example 7: Skip Verification (Fast Mode)

### Python Only
```bash
python3 milesight-camera-config.py --no-verify
```

This skips the final verification step if you're sure the camera will accept the configuration.

---

## Pre-Configuration Network Setup

Before running ANY example, set up your PC:

### Windows (PowerShell)
```powershell
# Check current IP
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status

# Set static IP for Ethernet adapter
New-NetIPAddress -InterfaceAlias "Ethernet" `
                 -IPAddress "192.168.5.100" `
                 -PrefixLength 24 `
                 -DefaultGateway "192.168.5.1"
```

### Linux/Mac
```bash
# Set static IP (example for eth0)
sudo ifconfig eth0 192.168.5.100 netmask 255.255.255.0
```

---

## Verify Camera After Configuration

### Ping Test
```bash
ping 192.168.100.101
```

### Access Web Interface
Open in browser:
```
http://192.168.100.101
```

Login with:
- Username: `admin`
- Password: `wordbypass` (or your custom password)

---

## Troubleshooting by Example

### Example: Camera not found
```powershell
# First, verify your PC can reach the camera's initial IP
ping 192.168.5.190

# If no response, set your PC's IP to 192.168.5.x range
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress "192.168.5.100" -PrefixLength 24
```

### Example: Script fails at IP change
```bash
# Try with verbose output (Python)
python3 milesight-camera-config.py --initial-ip 192.168.5.190 --final-ip 192.168.100.101

# Wait longer for camera to reboot, then verify manually
ping 192.168.100.101
```

### Example: Wrong password set
Re-run script with correct password:
```powershell
.\milesight-camera-config.ps1 -AdminPassword "CorrectPassword"
```

---

**Last Updated:** 2026-09-09
