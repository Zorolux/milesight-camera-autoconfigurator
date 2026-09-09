#!/usr/bin/env python3
# ============================================================
# MILESIGHT CAMERA CONFIGURATOR - PYTHON
# Automated Configuration (No Browser Manual Intervention)
# ============================================================

import requests
import time
import socket
import argparse
import sys
import json
from typing import Dict, Optional, Tuple

# Color codes for terminal output
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_color(message: str, color: str = Colors.WHITE) -> None:
    """Print colored message to console"""
    print(f"{color}{message}{Colors.RESET}")

def print_header() -> None:
    """Print script header"""
    print_color("=" * 50, Colors.CYAN)
    print_color("      MILESIGHT CAMERA CONFIGURATOR", Colors.CYAN)
    print_color("            (Automated - Python)", Colors.CYAN)
    print_color("=" * 50, Colors.CYAN)
    print()

def test_camera_connection(ip_address: str, max_attempts: int = 10) -> bool:
    """Test connection to camera IP address"""
    for attempt in range(1, max_attempts + 1):
        try:
            socket.create_connection((ip_address, 80), timeout=2)
            return True
        except (socket.timeout, socket.error):
            print_color(f"  Attempt {attempt}/{max_attempts}...", Colors.YELLOW)
            time.sleep(1)
    return False

def invoke_camera_api(
    ip_address: str, 
    endpoint: str, 
    data: Dict = None, 
    method: str = "POST",
    timeout: int = 10
) -> Optional[Dict]:
    """Call camera API endpoint"""
    url = f"http://{ip_address}/api{endpoint}"
    
    try:
        headers = {"Content-Type": "application/json"}
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=timeout)
        else:
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print_color(f"API Error on {endpoint}: {e}", Colors.RED)
        return None

def get_camera_status(ip_address: str) -> Optional[Dict]:
    """Get camera status"""
    try:
        response = requests.get(
            f"http://{ip_address}/api/v1/status",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print_color(f"Cannot get camera status: {e}", Colors.YELLOW)
        return None

def initialize_camera(
    ip_address: str,
    admin_password: str
) -> bool:
    """Initialize camera and set password"""
    print_color("[3] Initializing camera and setting password...", Colors.YELLOW)
    
    init_data = {
        "username": "admin",
        "password": admin_password,
        "confirmPassword": admin_password
    }
    
    response = invoke_camera_api(ip_address, "/v1/user/init", init_data)
    
    if response:
        print_color("Camera initialized with password set", Colors.GREEN)
        return True
    else:
        print_color("Warning: Could not initialize via API, camera may already be initialized", Colors.YELLOW)
        return False

def set_security_questions(
    ip_address: str,
    admin_password: str,
    q1_answer: str,
    q2_answer: str,
    q3_answer: str
) -> bool:
    """Set security questions and answers"""
    print_color("[4] Setting security questions...", Colors.YELLOW)
    
    security_data = {
        "username": "admin",
        "password": admin_password,
        "question1": 1,
        "answer1": q1_answer,
        "question2": 2,
        "answer2": q2_answer,
        "question3": 3,
        "answer3": q3_answer
    }
    
    response = invoke_camera_api(ip_address, "/v1/user/security", security_data)
    
    if response:
        print_color("Security questions set successfully", Colors.GREEN)
        return True
    else:
        print_color("Warning: Security questions setup returned no response", Colors.YELLOW)
        return False

def configure_network(
    ip_address: str,
    new_ip: str,
    subnet_mask: str = "255.255.255.0",
    gateway: str = "192.168.100.1"
) -> bool:
    """Configure camera network settings"""
    print_color(f"[5] Configuring new IP address: {new_ip}...", Colors.YELLOW)
    
    network_data = {
        "ipAddress": new_ip,
        "subnetMask": subnet_mask,
        "gateway": gateway,
        "dhcp": False
    }
    
    response = invoke_camera_api(ip_address, "/v1/network/ipv4", network_data)
    
    if response:
        print_color("IP configuration updated", Colors.GREEN)
        return True
    else:
        print_color("Warning: IP configuration returned no response", Colors.YELLOW)
        return False

def verify_final_ip(ip_address: str, max_attempts: int = 20) -> bool:
    """Verify camera is responding on final IP"""
    print()
    print_color(f"[6] Verifying camera response on new IP ({ip_address})...", Colors.YELLOW)
    
    for attempt in range(1, max_attempts + 1):
        sys.stdout.write(f"Verification {attempt}/{max_attempts}...")
        sys.stdout.flush()
        
        if test_camera_connection(ip_address, max_attempts=1):
            print_color(" CAMERA RESPONDING ON NEW IP!", Colors.GREEN)
            return True
        
        print(" waiting...")
        time.sleep(1)
    
    return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Milesight Camera Automated Configurator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 milesight-camera-config.py
  python3 milesight-camera-config.py --initial-ip 192.168.5.190 --final-ip 192.168.100.101
  python3 milesight-camera-config.py --password "mypassword" --q1-answer "custom_answer"
        """
    )
    
    parser.add_argument(
        "--initial-ip",
        default="192.168.5.190",
        help="Initial camera IP address (default: 192.168.5.190)"
    )
    
    parser.add_argument(
        "--final-ip",
        default="192.168.100.101",
        help="Final camera IP address (default: 192.168.100.101)"
    )
    
    parser.add_argument(
        "--password",
        default="wordbypass",
        help="Admin password to set (default: wordbypass)"
    )
    
    parser.add_argument(
        "--q1-answer",
        default="Q",
        help="Answer to security question 1 (default: Q)"
    )
    
    parser.add_argument(
        "--q2-answer",
        default="A",
        help="Answer to security question 2 (default: A)"
    )
    
    parser.add_argument(
        "--q3-answer",
        default="Z",
        help="Answer to security question 3 (default: Z)"
    )
    
    parser.add_argument(
        "--subnet",
        default="255.255.255.0",
        help="Subnet mask (default: 255.255.255.0)"
    )
    
    parser.add_argument(
        "--gateway",
        default="192.168.100.1",
        help="Gateway IP (default: 192.168.100.1)"
    )
    
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip final verification on new IP"
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # ============================================================
    # Step 1: Check initial connection
    # ============================================================
    
    print_color("[1] Checking connection to camera at initial IP...", Colors.YELLOW)
    print_color(f"    Target IP: {args.initial_ip}", Colors.WHITE)
    
    if not test_camera_connection(args.initial_ip, max_attempts=10):
        print()
        print_color("CANNOT REACH CAMERA AT " + args.initial_ip, Colors.RED)
        print_color("Make sure your PC has IP in 192.168.5.x range and cable is connected.", Colors.YELLOW)
        sys.exit(1)
    
    print_color("CAMERA DETECTED!", Colors.GREEN)
    print()
    
    # ============================================================
    # Step 2: Initialize camera
    # ============================================================
    
    time.sleep(1)
    if not initialize_camera(args.initial_ip, args.password):
        print_color("Continuing despite initialization warning...", Colors.YELLOW)
    
    time.sleep(2)
    
    # ============================================================
    # Step 3: Set security questions
    # ============================================================
    
    if not set_security_questions(
        args.initial_ip,
        args.password,
        args.q1_answer,
        args.q2_answer,
        args.q3_answer
    ):
        print_color("Continuing despite security questions warning...", Colors.YELLOW)
    
    time.sleep(2)
    
    # ============================================================
    # Step 4: Configure network
    # ============================================================
    
    if not configure_network(
        args.initial_ip,
        args.final_ip,
        args.subnet,
        args.gateway
    ):
        print_color("Continuing despite network configuration warning...", Colors.YELLOW)
    
    time.sleep(3)
    
    # ============================================================
    # Step 5: Verify final IP
    # ============================================================
    
    if not args.no_verify:
        if not verify_final_ip(args.final_ip, max_attempts=20):
            print()
            print_color("Camera not responding at " + args.final_ip + " yet.", Colors.RED)
            print_color("It may still be rebooting. Please wait and verify manually.", Colors.YELLOW)
            sys.exit(1)
        
        # Verify camera status
        print_color("")
        print_color("[7] Verifying camera configuration...", Colors.YELLOW)
        
        time.sleep(2)
        
        final_status = get_camera_status(args.final_ip)
        if final_status:
            print_color("Camera status retrieved successfully", Colors.GREEN)
    
    # ============================================================
    # Success!
    # ============================================================
    
    print()
    print_color("=" * 50, Colors.GREEN)
    print_color(" CONFIGURATION COMPLETED SUCCESSFULLY!", Colors.GREEN)
    print_color("=" * 50, Colors.GREEN)
    print()
    print_color("Camera Details:", Colors.CYAN)
    print_color(f"  IP Address: {args.final_ip}", Colors.WHITE)
    print_color(f"  Username: admin", Colors.WHITE)
    print_color(f"  Password: {args.password}", Colors.WHITE)
    print()
    print_color(f"Access at: http://{args.final_ip}", Colors.CYAN)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_color("\nScript interrupted by user", Colors.YELLOW)
        sys.exit(0)
    except Exception as e:
        print()
        print_color(f"Error: {e}", Colors.RED)
        sys.exit(1)
