# Autonomous SOC Analyst - CLI Tool

An intelligent command-line tool that analyzes authentication logs and generates comprehensive security incident reports using AI-powered backends (Google Gemini or Ollama).

## Overview

This tool automates the analysis of authentication logs by parsing security events and leveraging AI to detect threats, identify suspicious patterns, and generate professional incident reports in HTML format. It's designed for security operations center (SOC) analysts to quickly understand and respond to authentication-related security incidents.

## Features

- **Dual AI Backend Support**
  - Google Gemini API (cloud-based, highly capable)
  - Ollama (local models, no API key required)

- **Comprehensive Log Analysis**
  - Failed login detection and aggregation
  - Successful authentication tracking
  - Brute-force attack identification
  - Unusual SSH behavior detection
  - Connection attempt tracking
  - Suspicious login pattern recognition

- **Activity Tracking**
  - SUDO command execution logging
  - CRON job activity monitoring
  - Per-IP threat scoring and classification

- **Professional Report Generation**
  - HTML-formatted incident reports with dark theme
  - Threat severity classification (High/Medium/Low)
  - Source IP analysis and risk assessment
  - Actionable recommendations
  - Timestamp and metadata tracking

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- For Ollama: Ollama installed and running (see [Installation](#-installation))
- For Gemini: Valid Google Gemini API key

### Installation

1. **Clone or download the project:**

   ```bash
   cd "Autonomous SOC Analyst - CLI version"
   ```

2. **Install required Python packages:**

   ```bash
   pip install google-genai requests
   ```

3. **For Ollama users:** Download and install Ollama from [ollama.ai](https://ollama.ai)

## Usage

### Running the Tool

```bash
python soc_cli.py
```

### Backend Selection

When you run the tool, you'll be prompted to select an AI backend:

#### Option 1: Google Gemini (Cloud-based)

```
[1] Google Gemini  (requires API key)
```

- Enter your Gemini API key (get one from [Google AI Studio](https://aistudio.google.com))
- Choose a model:
  - `gemini-flash-lite-latest` - Fast, lightweight (recommended for quick analysis)
  - `gemini-flash-latest` - Balanced performance and capability
  - `gemini-pro-latest` - Most capable (slower, higher quality analysis)

#### Option 2: Ollama (Local)

```
[2] Ollama         (local model, no API key needed)
```

- Enter your desired Ollama model name (e.g., `llama3`, `mistral`, `phi3`)
- Optionally specify custom Ollama URL (defaults to `http://localhost:11434`)

### Log File Input

The tool will prompt for an authentication log file path:

**Examples:**

- Linux/macOS: `/var/log/auth.log` or `/var/log/secure`
- Windows with WSL: `./auth.log`
- Local test file: `./auth.log`

### Output

The tool generates:

- Console output with parsing statistics
- HTML report file named: `soc_report_YYYYMMDD_HHMMSS.html`
- Automatically opens the report in your default web browser

## Configuration

### Ollama Configuration

**Default URL:** `http://localhost:11434`

**Custom URL:** During tool execution, when prompted for Ollama settings, enter your custom URL if Ollama is running on a different host or port.

**Example URLs:**

- Local: `http://localhost:11434`
- Remote server: `http://192.168.1.100:11434`
- Docker container: `http://ollama:11434`

### Starting Ollama

```bash
# Install Ollama first from ollama.ai

# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama3
```

## Backend-Specific Optimization

### Ollama (Local Models)

- Uses an **optimized simplified prompt** for better compatibility with smaller models
- Directly generates valid HTML with embedded data
- Works reliably with models like: `llama2`, `mistral`, `neural-chat`, `phi`
- Recommended for consistent results: **llama2** or **mistral**
- No dependency on model's instruction-following complexity

### Google Gemini (Cloud API)

- Uses the **original detailed prompt** for superior analysis
- Takes full advantage of Gemini's advanced reasoning capabilities
- Generates more sophisticated and detailed threat assessments
- Better for critical incident analysis requiring deep insights

---

## Project Structure

```
├── soc_cli.py           # Main CLI application entry point
├── backends.py          # AI backend implementations (Gemini, Ollama)
├── parser.py            # Authentication log parser
├── logs/                # Directory for log files (optional)
├── README.md            # This file
└── soc_report_*.html    # Generated incident reports
```

### File Descriptions

**soc_cli.py**

- Main entry point for the application
- Handles user prompts and backend selection
- Orchestrates log parsing and report generation
- Manages HTML report output and browser opening

**backends.py**

- `GeminiBackend` - Interface to Google Gemini API
- `OllamaBackend` - Interface to local Ollama models
- `get_prompt_gemini()` - Detailed prompt for capable cloud-based models (Gemini)
- `get_prompt_ollama()` - Optimized prompt for local Ollama models with direct HTML generation
- Backend-specific prompt optimization for better compatibility and results

**parser.py**

- `AuthLogParser` - Parses authentication log files
- Extracts and aggregates security events
- Builds data summary for AI analysis
- Detects patterns and suspicious activities

## Example Workflow

```bash
# 1. Start the tool
python soc_cli.py

# 2. Select backend
============================================================
        Autonomous SOC Analyst - CLI Tool
============================================================

[*] Select AI backend:
  [1] Google Gemini  (requires API key)
  [2] Ollama         (local model, no API key needed)

Enter choice [1/2]: 2

# 3. Enter model and URL
Enter Ollama model name (e.g. llama3, mistral, phi3): llama3
Enter Ollama URL [default: http://localhost:11434]:

# 4. Provide log file
Enter path to auth.log file (e.g. /var/log/auth.log or ./auth.log): ./auth.log

# 5. View results
[+] Parsed: 45 unique IPs, 128 cron events, 23 sudo commands
[*] Sending data to AI backend (ollama) ...
[*] Generating HTML report ...
[+] Report saved: soc_report_20260326_143022.html
[*] Opening report in browser...
```

## Report Sections

Generated HTML reports include:

- **Incident Overview** - Executive summary and severity level
- **Summary of Findings** - Key metrics and statistics
  - Unique source IPs analyzed
  - Failed authentication attempts
  - Brute-force indicators
  - Suspicious patterns detected
- **Source IPs of Interest** - Detailed table with:
  - IP address
  - Threat level
  - Failed/successful login counts
  - Attack indicators
- **System Activity Context**
  - SUDO command execution logs
  - CRON job insights
  - Behavioral anomalies
- **Recommendations** - Actionable remediation steps

## Log Analysis Capabilities

The parser automatically detects:

| Detection           | Pattern                                    |
| ------------------- | ------------------------------------------ |
| Failed Logins       | "Failed password" entries                  |
| Successful Auth     | "Accepted" login events                    |
| Brute Force         | "maximum authentication attempts exceeded" |
| SSH Anomalies       | "Bad protocol version" errors              |
| Connection Tracking | "Connection" events                        |
| SUDO Usage          | "sudo:" commands with user and command     |
| CRON Activities     | "CRON" scheduled job entries               |

## Troubleshooting

### Ollama Connection Error

```
[ERROR] Cannot connect to Ollama at http://localhost:11434. Is it running?
```

**Solution:**

- Ensure Ollama is running: `ollama serve`
- Check the URL is correct
- Verify firewall isn't blocking the port
- For remote Ollama, use the correct IP/hostname

### File Not Found

```
[ERROR] File not found: /path/to/auth.log
```

**Solution:**

- Verify the file path is correct
- Use absolute path or ensure relative path is from script directory
- Check file permissions

### Gemini API Error

```
AI analysis failed: [error message]
```

**Solution:**

- Verify API key is valid and active
- Check your Google Cloud quota limits
- Ensure you have internet connectivity
- Verify model name is correct

### No Model Available in Ollama

```
Error: model not found
```

**Solution:**

```bash
# Pull the model first
ollama pull llama3
```

### HTML Report Not Opening

- The report file is still created even if the browser doesn't open automatically
- **For Ollama:** The optimized prompt now generates direct HTML, ensuring valid output
- If still experiencing issues:
  - Try a different Ollama model: `ollama pull mistral` or `ollama pull neural-chat`
  - Switch to Google Gemini backend for guaranteed quality
  - Manually open the generated `soc_report_*.html` file in your browser
  - Check browser console for any rendering issues

**Note:** The Ollama backend uses an optimized prompt that directly generates HTML, which is more reliable than expecting models to follow complex formatting instructions.

## Development

### Adding New AI Backends

To add a new backend:

1. Create a new class in `backends.py` inheriting from a base backend pattern
2. Implement the `analyze_log_summary()` method
3. Create backend-specific prompt functions (`get_prompt_<backend>()`) if needed
4. Add backend selection option in `soc_cli.py`

### Extending Log Parser

To detect new log patterns:

1. Add pattern matching in `AuthLogParser._parse_line()`
2. Store results in the appropriate data structure
3. Include in the summary returned by `_build_summary()`
4. Update the prompt in `backends.py` to highlight the new data

## Dependencies

```
google-genai      # Google Gemini API client
requests          # HTTP library for Ollama API calls
```

Install with:

```bash
pip install google-genai requests
```

## License

[Add your license information here]

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancements.

## Support

For issues or questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing logs in the `logs/` directory
3. Ensure all prerequisites are installed correctly

## Key Design Principles

- **Modular Architecture** - Easy to extend with new backends or parsers
- **AI-Powered Analysis** - Leverages cutting-edge AI for intelligent threat detection
- **Backend Optimization** - Tailored prompts for each AI backend (Gemini vs Ollama) for best results
- **User-Friendly** - Clear prompts and informative console output
- **Professional Output** - High-quality HTML reports suitable for stakeholder presentation
- **Flexible** - Support for multiple AI providers and customizable configurations
- **Local-First Option** - Ollama integration allows analysis without external API calls

---

**Version:** 1.0  
**Last Updated:** March 26, 2026
