# Milesight Camera Autoconfigurator

Automated configuration tool for Milesight cameras - sets password, security questions, and IP address without manual browser intervention.

**Available in:** PowerShell & Python

---

## Features

✅ **Automatic Camera Detection** - Finds camera on initial IP  
✅ **Password Setup** - Sets admin password automatically  
✅ **Security Questions** - Configures all 3 security questions (Q, A, Z)  
✅ **Network Configuration** - Changes IP address automatically  
✅ **Verification** - Confirms camera responds on new IP  
✅ **No Manual Steps** - Fully automated, no browser interaction needed  

---

## Requirements

### PowerShell Version
- **Windows 10/11**
- **PowerShell 5.0+** (Run as Administrator)
- Network adapter connected to camera via Ethernet

### Python Version
- **Python 3.6+**
- **requests library** (`pip install requests`)
- Network connection to camera

---

## Quick Start

### PowerShell

```powershell
# Run as Administrator
.\milesight-camera-config.ps1

# Or with custom parameters
.\milesight-camera-config.ps1 -CameraInitialIP "192.168.5.190" `
                               -FinalCameraIP "192.168.100.101" `
                               -AdminPassword "wordbypass"
```

### Python

```bash
# Basic usage (uses default values)
python3 milesight-camera-config.py

# With custom parameters
python3 milesight-camera-config.py \
    --initial-ip 192.168.5.190 \
    --final-ip 192.168.100.101 \
    --password "wordbypass" \
    --q1-answer "Q" \
    --q2-answer "A" \
    --q3-answer "Z"
```

---

## Default Configuration

| Parameter | Default Value |
|-----------|---------------|
| Initial IP | `192.168.5.190` |
| Final IP | `192.168.100.101` |
| Subnet Mask | `255.255.255.0` |
| Gateway | `192.168.100.1` |
| Admin Password | `wordbypass` |
| Security Q1 Answer | `Q` |
| Security Q2 Answer | `A` |
| Security Q3 Answer | `Z` |

---

## PowerShell Usage

### Basic
```powershell
.\milesight-camera-config.ps1
```

### With Custom IP Addresses
```powershell
.\milesight-camera-config.ps1 -CameraInitialIP "192.168.5.100" `
                               -FinalCameraIP "192.168.100.50"
```

### With All Custom Parameters
```powershell
.\milesight-camera-config.ps1 -CameraInitialIP "192.168.5.190" `
                               -FinalCameraIP "192.168.100.101" `
                               -AdminPassword "MySecurePass123" `
                               -SecurityQ1Answer "Q" `
                               -SecurityQ2Answer "A" `
                               -SecurityQ3Answer "Z"
```

---

## Python Usage

### Basic
```bash
python3 milesight-camera-config.py
```

### With Custom IP Addresses
```bash
python3 milesight-camera-config.py --initial-ip 192.168.5.100 --final-ip 192.168.100.50
```

### With Custom Password and Security Answers
```bash
python3 milesight-camera-config.py \
    --password "MySecurePass123" \
    --q1-answer "Question1" \
    --q2-answer "Question2" \
    --q3-answer "Question3"
```

### Skip Final Verification
```bash
python3 milesight-camera-config.py --no-verify
```

### View All Options
```bash
python3 milesight-camera-config.py --help
```

---

## Configuration Steps

The script performs these steps automatically:

1. **Network Adapter Selection** (PowerShell only) - Choose which network adapter to use
2. **Camera Detection** - Pings initial IP to confirm camera is reachable
3. **Camera Initialization** - Sets admin password via API
4. **Security Configuration** - Sets 3 security questions and answers
5. **Network Configuration** - Updates IP, subnet mask, and gateway
6. **Verification** - Confirms camera responds on new IP address

---

## Network Setup

Before running the script, ensure your PC is configured correctly:

### Option 1: Static IP (Recommended)
- Set your PC's IP to `192.168.5.100` (or similar in `192.168.5.x` range)
- Subnet Mask: `255.255.255.0`
- Connect Ethernet cable to camera

### Option 2: DHCP
- Camera will receive IP `192.168.5.190` via DHCP
- Ensure your DHCP server is configured for this range

---

## Troubleshooting

### PowerShell: "Script execution policy" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python: "requests not found"
```bash
pip install requests
# or
pip3 install requests
```

### Camera not detected at initial IP
- Verify Ethernet cable is connected
- Check your PC's IP is in `192.168.5.x` range
- Power cycle the camera and retry
- Try manual ping: `ping 192.168.5.190` (PowerShell) or `ping 192.168.5.190` (Terminal)

### Camera doesn't respond on new IP
- Camera may still be rebooting after IP change
- Wait 30-60 seconds and manually verify with: `ping 192.168.100.101`
- Check if IP was saved correctly in camera's web interface
- Try script again if initial attempt partially failed

### Connection timeout errors
- Ensure no firewall is blocking HTTP traffic to port 80
- Verify camera's web API is enabled
- Check that you're using the correct initial IP

---

## API Endpoints Used

- `GET /api/v1/status` - Get camera status
- `POST /api/v1/user/init` - Initialize camera and set password
- `POST /api/v1/user/security` - Configure security questions
- `POST /api/v1/network/ipv4` - Configure network settings

---

## Security Considerations

⚠️ **Important:**
- Default password `wordbypass` should be changed after configuration
- Security answers are basic examples - customize for your needs
- Use HTTPS when accessing camera remotely
- Store credentials securely
- Change default credentials before deploying to production

---

## License

MIT License - Feel free to modify and distribute

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify camera is in factory reset state
3. Check Milesight camera documentation for specific model details
4. Ensure your firmware version supports the API endpoints used

---

## Changelog

### v1.0 (Initial Release)
- PowerShell and Python implementations
- Automatic password setup
- Security questions configuration
- IP address configuration
- Network verification

---

**Last Updated:** 2026-09-09
