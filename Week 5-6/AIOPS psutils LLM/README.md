
# �️ System Monitor with LLM Integration

An intelligent system monitoring tool that combines real-time system metrics collection with LLM-powered analysis and reporting capabilities. This project uses psutil for metrics collection and local LLMs for automated system analysis.

## ✨ Key Features

- Collects live system metrics using `psutil`
- Sends the snapshot to a local LLM via Ollama API
- Returns a clean, human-readable report
- Works on Windows & Linux
- CLI + Streamlit UI support
- Logging + Export to file supported

## 🔧 Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Install and run Ollama:**

- [Ollama installation](https://ollama.com/download)
- Start the server:

```bash
ollama serve
```

3. **Pull a small LLM model:**

```bash
ollama pull phi3
# or: ollama pull gemma:2b
```

4. **Run from CLI:**

```bash
python debugger.py --json sysinfo.json --report report.txt
```

5. **Run UI:**

```bash
streamlit run streamlit_app.py
```

## 📁 File Structure

| File             | Purpose                          |
|------------------|----------------------------------|
| `debugger.py`     | CLI tool                        |
| `streamlit_app.py`| Streamlit UI                    |
| `system_info.py`  | Collects system stats via psutil|
| `llm_interface.py`| Interacts with local LLM        |

## 🚀 Packaging

# Additional Features

## 📊 Metrics Collected

- CPU usage and core information
- Memory utilization (RAM & swap)
- Disk usage and I/O
- Network statistics
- Process information
- System uptime

## 🤖 LLM Features

- Automated system health analysis
- Natural language reporting
- Anomaly detection
- Root cause analysis
- Performance recommendations

## 🔒 Security & Privacy

- Local LLM processing only
- No external API dependencies
- Secure data handling

## 🛠️ Dependencies

- psutil
- streamlit
- requests
- fpdf
- apscheduler
- python-dotenv
