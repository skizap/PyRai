# PyRai - Mirai Python Variant (Updated for Secure Testing)

**🚨 ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited. 🚨**

## ⚠️ IMPORTANT SECURITY NOTICE

This is an **UPDATED VERSION** of PyRai with enhanced security features for controlled penetration testing environments. The original code has been significantly modified to include:

- **Testing safeguards** and rate limiting
- **Enhanced security** with updated dependencies
- **Comprehensive logging** and error handling
- **Safety confirmations** required for execution
- **Self-destruct mechanisms** in test payloads

## 🔒 Security Updates

### Key Improvements
- ✅ **Updated Dependencies**: All packages updated to secure versions (2024)
- ✅ **Testing Mode**: Enabled by default with strict limits
- ✅ **Input Validation**: Comprehensive validation of all inputs
- ✅ **Thread Safety**: Proper locking and thread management
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Rate Limiting**: Controlled scan speeds and connection limits

### Safety Features
- 🛡️ **Authorization Required**: Each module requires explicit authorization
- 🛡️ **Localhost Binding**: Services bind to localhost in testing mode
- 🛡️ **Target Limits**: Maximum scan targets and infection limits
- 🛡️ **Safe IP Ranges**: Uses RFC 3927 test ranges in testing mode
- 🛡️ **Comprehensive Logging**: All activities logged to files

## 📋 Requirements

### Updated Dependencies
```bash
pip install -r requirements.txt
```

**Key packages:**
- `paramiko>=3.4.0` (secure SSH/telnet)
- `cryptography>=41.0.0` (modern cryptography)
- `requests>=2.31.0` (secure HTTP)
- `colorama>=0.4.6` (terminal colors)

## 🚀 Quick Start (Testing Mode)

### 1. Start Relay Server
```bash
python relay.py
```
**Safety confirmation required**: Type `AUTHORIZED` when prompted.

### 2. Run Scanner
```bash
python scanner.py
```
**Safety confirmation required**: Type `AUTHORIZED` when prompted.

### 3. Deploy Payloads (Optional)
```bash
python loader.py dump/csdb.txt
```
**Safety confirmation required**: Type `AUTHORIZED` when prompted.

## 📊 Testing Limits (Default)

| Component | Testing Limit | Production Limit |
|-----------|---------------|------------------|
| Scanner Targets | 100 | 1,000,000 |
| Relay Connections | 100 | 1,000 |
| Loader Infections | 10 | 1,000 |
| Scan Delay | 2 seconds | 0.1 seconds |

## 📁 File Structure

```
PyRai-master/
├── scanner.py          # Enhanced scanner with safety features
├── relay.py           # Secure credential collection server
├── loader.py          # Payload deployment with limits
├── requirements.txt   # Updated secure dependencies
├── libs/
│   └── truecolors.py  # Terminal color utilities
├── dump/              # Credential storage (auto-created)
│   └── csdb.txt      # Credential database
├── bin/               # Payload storage (auto-created)
│   └── test_payload.py # Harmless test payload
├── README.md          # This file
└── TESTING_GUIDE.md   # Comprehensive testing guide
```

## 🔧 Configuration

### Testing Mode (Default)
```python
TESTING_MODE = True  # Safe testing with limits
```

### Lab Environment Mode
```python
TESTING_MODE = False  # Full functionality for isolated labs
```

## 📝 Log Files

- **scanner.log**: Scanner activity and errors
- **relay.log**: Relay connections and credential storage  
- **loader.log**: Payload deployment activities

## 🎯 Use Cases

### ✅ Authorized Use Cases
- **Penetration Testing**: Authorized security assessments
- **Red Team Exercises**: Controlled adversary simulations
- **Security Research**: Academic and professional research
- **Vulnerability Assessment**: IoT device security testing
- **Training**: Cybersecurity education and training

### ❌ Prohibited Use Cases
- Unauthorized access to systems
- Malicious attacks on networks
- Criminal activities
- Violation of terms of service
- Any illegal activities

## 🛡️ Security Recommendations

After testing, implement these security measures:

1. **Change Default Credentials**: Update all default passwords
2. **Disable Telnet**: Use SSH instead of telnet where possible
3. **Network Segmentation**: Isolate IoT devices
4. **Monitoring**: Implement network monitoring
5. **Firmware Updates**: Keep device firmware updated

## 📚 Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**: Comprehensive testing guide
- **[Original README](README_ORIGINAL.md)**: Original documentation (if needed)

## ⚖️ Legal Notice

This tool is provided for **educational and authorized security testing purposes only**. Users are responsible for ensuring compliance with all applicable laws and regulations. 

**Unauthorized use is strictly prohibited** and may result in:
- Criminal charges
- Civil penalties  
- Legal prosecution
- Academic/professional consequences

## 🤝 Responsible Disclosure

If you discover vulnerabilities during testing:
1. Document findings responsibly
2. Report through proper channels
3. Allow reasonable time for fixes
4. Follow coordinated disclosure practices

## 📞 Support

For questions about authorized testing:
- Review the testing guide
- Check log files for errors
- Ensure proper authorization
- Follow ethical guidelines

---

**Remember**: Always obtain proper written authorization before conducting any security testing activities. When in doubt, don't proceed without explicit permission.

**Original Mirai Research**: This tool replicates the working of the original Mirai botnet for educational and defensive security purposes only.
