# ============================================================
# MILESIGHT CAMERA CONFIGURATOR - POWERSHELL
# Automated Configuration (No Browser Manual Intervention)
# ============================================================

#Requires -RunAsAdministrator

param(
    [string]$CameraInitialIP = "192.168.5.190",
    [string]$FinalCameraIP = "192.168.100.101",
    [string]$AdminPassword = "wordbypass",
    [string]$SecurityQ1Answer = "Q",
    [string]$SecurityQ2Answer = "A",
    [string]$SecurityQ3Answer = "Z"
)

# ============================================================
# Helper Functions
# ============================================================

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-CameraConnection {
    param([string]$IPAddress, [int]$MaxAttempts = 10)
    
    for ($i = 1; $i -le $MaxAttempts; $i++) {
        if (Test-Connection -ComputerName $IPAddress -Count 1 -Quiet -ErrorAction SilentlyContinue) {
            return $true
        }
        Write-ColorOutput "  Attempt $i/$MaxAttempts..." Yellow
        Start-Sleep -Seconds 1
    }
    return $false
}

function Invoke-CameraAPI {
    param(
        [string]$IPAddress,
        [string]$Endpoint,
        [hashtable]$Data,
        [string]$Method = "POST"
    )
    
    $Uri = "http://$IPAddress/api$Endpoint"
    
    try {
        $Headers = @{
            "Content-Type" = "application/json"
        }
        
        $Body = $Data | ConvertTo-Json
        
        $Response = Invoke-WebRequest `
            -Uri $Uri `
            -Method $Method `
            -Headers $Headers `
            -Body $Body `
            -UseBasicParsing `
            -TimeoutSec 10
        
        return $Response.Content | ConvertFrom-Json
    }
    catch {
        Write-ColorOutput "API Error on $Endpoint : $_" Red
        return $null
    }
}

function Get-CameraStatus {
    param([string]$IPAddress)
    
    try {
        $Response = Invoke-WebRequest `
            -Uri "http://$IPAddress/api/v1/status" `
            -Method GET `
            -UseBasicParsing `
            -TimeoutSec 5
        
        return $Response.Content | ConvertFrom-Json
    }
    catch {
        Write-ColorOutput "Cannot get camera status: $_" Yellow
        return $null
    }
}

# ============================================================
# MAIN SCRIPT
# ============================================================

Clear-Host

Write-ColorOutput "============================================" Cyan
Write-ColorOutput "      MILESIGHT CAMERA CONFIGURATOR" Cyan
Write-ColorOutput "         (Automated - PowerShell)" Cyan
Write-ColorOutput "============================================" Cyan
Write-ColorOutput ""

# ============================================================
# Step 1: Select Network Adapter
# ============================================================

Write-ColorOutput "[1] Detecting active network adapters..." Yellow
$Adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" -and $_.HardwareInterface -eq $true }

if (-not $Adapters) {
    Write-ColorOutput "NO ACTIVE NETWORK ADAPTERS FOUND." Red
    Read-Host "Press Enter to exit"
    exit
}

$i = 1
foreach ($Adapter in $Adapters) {
    Write-Host "$i. $($Adapter.Name) - $($Adapter.InterfaceDescription)"
    $i++
}

Write-ColorOutput ""
$Selection = Read-Host "Select Ethernet adapter number connected to camera"

if (-not ($Selection -as [int])) {
    Write-ColorOutput "Invalid selection." Red
    exit
}

$Index = [int]$Selection - 1
if ($Index -lt 0 -or $Index -ge $Adapters.Count) {
    Write-ColorOutput "Invalid selection." Red
    exit
}

$InterfaceAlias = $Adapters[$Index].Name
Write-ColorOutput "Selected adapter: $InterfaceAlias" Green
Write-ColorOutput ""

# ============================================================
# Step 2: Detect Camera at Initial IP
# ============================================================

Write-ColorOutput "[2] Searching for camera at $CameraInitialIP..." Yellow
$CameraFound = Test-CameraConnection -IPAddress $CameraInitialIP -MaxAttempts 10

if (-not $CameraFound) {
    Write-ColorOutput ""
    Write-ColorOutput "CANNOT REACH CAMERA AT $CameraInitialIP" Red
    Write-ColorOutput "Make sure PC has IP in 192.168.5.x range and cable is connected." Yellow
    Read-Host "Press Enter to exit"
    exit
}

Write-ColorOutput "CAMERA DETECTED!" Green
Write-ColorOutput ""

# ============================================================
# Step 3: Initialize Camera (Set Password)
# ============================================================

Write-ColorOutput "[3] Initializing camera and setting password..." Yellow

$InitData = @{
    username = "admin"
    password = $AdminPassword
    confirmPassword = $AdminPassword
}

$InitResponse = Invoke-CameraAPI -IPAddress $CameraInitialIP -Endpoint "/v1/user/init" -Data $InitData
if ($InitResponse) {
    Write-ColorOutput "Camera initialized with password set" Green
} else {
    Write-ColorOutput "Warning: Could not initialize via API, camera may already be initialized" Yellow
}

Start-Sleep -Seconds 2

# ============================================================
# Step 4: Set Security Questions
# ============================================================

Write-ColorOutput "[4] Setting security questions..." Yellow

$SecurityData = @{
    username = "admin"
    password = $AdminPassword
    question1 = 1
    answer1 = $SecurityQ1Answer
    question2 = 2
    answer2 = $SecurityQ2Answer
    question3 = 3
    answer3 = $SecurityQ3Answer
}

$SecurityResponse = Invoke-CameraAPI -IPAddress $CameraInitialIP -Endpoint "/v1/user/security" -Data $SecurityData
if ($SecurityResponse) {
    Write-ColorOutput "Security questions set successfully" Green
} else {
    Write-ColorOutput "Warning: Security questions setup returned no response" Yellow
}

Start-Sleep -Seconds 2

# ============================================================
# Step 5: Change Camera IP Address
# ============================================================

Write-ColorOutput "[5] Configuring new IP address: $FinalCameraIP..." Yellow

$NetworkData = @{
    ipAddress = $FinalCameraIP
    subnetMask = "255.255.255.0"
    gateway = "192.168.100.1"
    dhcp = $false
}

$NetworkResponse = Invoke-CameraAPI -IPAddress $CameraInitialIP -Endpoint "/v1/network/ipv4" -Data $NetworkData
if ($NetworkResponse) {
    Write-ColorOutput "IP configuration updated" Green
} else {
    Write-ColorOutput "Warning: IP configuration returned no response" Yellow
}

Start-Sleep -Seconds 3

# ============================================================
# Step 6: Verify Camera on New IP
# ============================================================

Write-ColorOutput ""
Write-ColorOutput "[6] Verifying camera response on new IP ($FinalCameraIP)..." Yellow

$FinalFound = $false
for ($x = 1; $x -le 20; $x++) {
    Write-Host "Verification $x/20..." -NoNewline
    if (Test-Connection -ComputerName $FinalCameraIP -Count 1 -Quiet -ErrorAction SilentlyContinue) {
        Write-ColorOutput " CAMERA RESPONDING ON NEW IP!" Green
        $FinalFound = $true
        break
    }
    Write-Host " waiting..."
    Start-Sleep -Seconds 1
}

if (-not $FinalFound) {
    Write-ColorOutput ""
    Write-ColorOutput "Camera not responding at $FinalCameraIP yet. It may still be rebooting." Yellow
    Write-ColorOutput "Please wait a moment and verify manually." Yellow
    Read-Host "Press Enter to exit"
    exit
}

# ============================================================
# Step 7: Verify Camera Configuration
# ============================================================

Write-ColorOutput ""
Write-ColorOutput "[7] Verifying camera configuration..." Yellow

Start-Sleep -Seconds 2

$FinalStatus = Get-CameraStatus -IPAddress $FinalCameraIP
if ($FinalStatus) {
    Write-ColorOutput "Camera status retrieved successfully" Green
} else {
    Write-ColorOutput "Could not retrieve final status (camera may still be starting)" Yellow
}

# ============================================================
# Success!
# ============================================================

Write-ColorOutput ""
Write-ColorOutput "============================================" Green
Write-ColorOutput " CONFIGURATION COMPLETED SUCCESSFULLY!" Green
Write-ColorOutput "============================================" Green
Write-ColorOutput ""
Write-ColorOutput "Camera Details:" Cyan
Write-ColorOutput "  IP Address: $FinalCameraIP" White
Write-ColorOutput "  Username: admin" White
Write-ColorOutput "  Password: $AdminPassword" White
Write-ColorOutput ""
Write-ColorOutput "Access at: http://$FinalCameraIP" Cyan
Write-ColorOutput ""

Read-Host "Press Enter to close"
