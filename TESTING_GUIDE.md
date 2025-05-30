# PyRai Testing Guide - Updated for Secure Testing

**ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.**

## Overview

This updated version of PyRai includes enhanced security features, testing safeguards, and comprehensive logging for controlled penetration testing environments.

## Key Security Updates

### 1. Testing Safeguards
- **TESTING_MODE**: Enabled by default to limit functionality
- **Rate Limiting**: Reduced scan speeds and connection limits
- **Target Limits**: Maximum scan targets and infection limits
- **Safe IP Ranges**: Uses RFC 3927 test ranges in testing mode
- **Localhost Binding**: Services bind to localhost in testing mode

### 2. Enhanced Security
- **Updated Dependencies**: All packages updated to secure versions
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: Robust error handling and logging
- **Thread Safety**: Thread-safe operations with proper locking
- **Timeout Controls**: Proper timeout handling for all network operations

### 3. Safety Confirmations
- **Required Authorization**: Each module requires explicit authorization
- **Self-Destruct Payloads**: Test payloads include self-destruct mechanisms
- **Comprehensive Logging**: All activities logged to files

## Installation

1. **Update Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import paramiko, cryptography, requests; print('Dependencies OK')"
   ```

## Testing Workflow

### Step 1: Start the Relay Server

```bash
python relay.py
```

**Safety Confirmation Required**: Type `AUTHORIZED` when prompted.

**Expected Output**:
```
==================================================
PyRai Relay Server - Updated for Secure Testing
ETHICAL DISCLAIMER: This tool is for authorized testing only.
==================================================

[SAFETY CONFIRMATION]
This relay will collect credentials from remote scanners.
Ensure you have proper authorization for this testing activity.
Type 'AUTHORIZED' to continue: AUTHORIZED

[18:09:50] [INFO] Starting relay on 127.0.0.1:31337
[18:09:50] [WARNING] TESTING MODE ENABLED
[18:09:50] [WARNING] Max connections limited to: 100
[18:09:50] [INFO] Relay is online!
```

### Step 2: Run the Scanner

```bash
python scanner.py
```

**Safety Confirmation Required**: Type `AUTHORIZED` when prompted.

**Expected Behavior**:
- Scans limited to 100 targets in testing mode
- Uses safe IP ranges (192.0.2.x)
- 2-second delay between scans
- Comprehensive logging to `scanner.log`

### Step 3: Monitor Credential Collection

The relay will collect any successful brute force attempts in:
- **File**: `dump/csdb.txt`
- **Format**: `username:password:ip:port:timestamp`

### Step 4: Deploy Payloads (Optional)

```bash
python loader.py dump/csdb.txt
```

**Safety Confirmation Required**: Type `AUTHORIZED` when prompted.

**Expected Behavior**:
- Starts HTTP server on port 31338
- Creates harmless test payload
- Limited to 10 infections in testing mode
- Payloads self-destruct after execution

## Configuration Options

### Testing Mode Controls

**Scanner Configuration** (`scanner.py`):
```python
TESTING_MODE = True  # Set to False for lab environments
MAX_SCAN_TARGETS = 100 if TESTING_MODE else 1000000
SCAN_DELAY = 2 if TESTING_MODE else 0.1
__THREADS__ = 5  # Reduced for testing
```

**Relay Configuration** (`relay.py`):
```python
__TESTING_MODE__ = True
__MAXCONN__ = 100  # Reduced for testing
TCP_IP = '127.0.0.1' if __TESTING_MODE__ else '0.0.0.0'
```

**Loader Configuration** (`loader.py`):
```python
__TESTING_MODE__ = True
__MAX_INFECTIONS__ = 10 if TESTING_MODE else 1000
```

### Network Configuration

**For Lab Environments** (disable testing mode):
1. Set `TESTING_MODE = False` in all modules
2. Update `__RELAY_H__` in scanner.py to relay server IP
3. Configure appropriate IP ranges in `generateIP()`

## Log Files

- **scanner.log**: Scanner activity and errors
- **relay.log**: Relay connections and credential storage
- **loader.log**: Payload deployment activities

## Security Features

### Input Validation
- IP address format validation
- Port range validation (1-65535)
- Credential format validation
- File path validation

### Rate Limiting
- Connection timeouts (10-30 seconds)
- Scan delays (2 seconds in testing mode)
- Maximum connection limits
- Infection count limits

### Error Handling
- Graceful connection failures
- Timeout handling
- File operation errors
- Thread safety

## Test Payload Details

The test payload (`test_payload.py`) performs:
1. **System Information**: Displays timestamp, system info, PID
2. **Test File Creation**: Creates `/tmp/pyrai_test.txt`
3. **Self-Destruct**: Removes itself after execution
4. **Logging**: Logs execution details

## Monitoring and Analysis

### Real-time Monitoring
```bash
# Monitor relay logs
tail -f relay.log

# Monitor scanner logs
tail -f scanner.log

# Monitor credential database
tail -f dump/csdb.txt
```

### Statistics
The relay displays statistics every 60 seconds:
- Active connections
- Total credentials stored

## Troubleshooting

### Common Issues

1. **Permission Denied**:
   ```bash
   chmod +x scanner.py relay.py loader.py
   ```

2. **Port Already in Use**:
   - Change `__PORT__` in relay.py
   - Update `__RELAY_P__` in scanner.py accordingly

3. **Connection Refused**:
   - Ensure relay is running before starting scanner
   - Check firewall settings
   - Verify IP/port configuration

### Debug Mode
Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Lab Environment Setup

For advanced testing in isolated lab environments:

1. **Disable Testing Mode**:
   ```python
   TESTING_MODE = False
   ```

2. **Configure Target Networks**:
   - Update IP generation logic
   - Set appropriate scan ranges
   - Configure relay server IP

3. **Deploy Test Targets**:
   - Set up vulnerable IoT devices
   - Configure honeypots
   - Use isolated network segments

## Ethical Guidelines

1. **Authorization Required**: Only use in authorized environments
2. **Isolated Networks**: Use air-gapped or isolated test networks
3. **Documentation**: Maintain detailed logs of all activities
4. **Cleanup**: Remove all payloads and artifacts after testing
5. **Responsible Disclosure**: Report vulnerabilities through proper channels

## Mitigation Recommendations

After testing, implement these security measures:

1. **Change Default Credentials**: Update all default passwords
2. **Disable Telnet**: Use SSH instead of telnet where possible
3. **Network Segmentation**: Isolate IoT devices
4. **Monitoring**: Implement network monitoring for suspicious activity
5. **Firmware Updates**: Keep device firmware updated

## Legal Notice

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations. Unauthorized use is strictly prohibited and may result in criminal and civil penalties.

---

**Remember**: Always obtain proper authorization before conducting any security testing activities. 