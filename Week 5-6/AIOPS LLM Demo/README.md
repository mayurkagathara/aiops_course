# 🔍 Log Inspecto## System Requirements

| Component    | Minimum |
|--------------|---------|
| RAM          | 8 GB    |
| CPU          | Intel Core i5 or higher |
| Disk         | 256 GB SSD |
| GPU          | ❌ Not required |
| OS           | Windows 10/11, Linux, macOS |

A powerful log analysis tool that leverages Large Language Models (LLMs) to provide intelligent insights from system logs. This project uses local LLMs via Ollama for privacy-focused log analysis.

---

## 📦 Features

- Upload `.log` or `.txt` files
- Ask questions like:
  - How many errors are there?
  - What is the root cause of failure?
  - Summarize the log file.
- Powered by local **Gemma model** (runs fully on your machine)

---

## 🖥 System Requirements

| Component    | Minimum |
|--------------|---------|
| RAM          | 8 GB    |
| CPU          | Intel Core i5 or higher (you have i5-8250U ✅) |
| Disk         | 256 GB SSD (you have ✅) |
| GPU          | ❌ Not required (Gemma runs on CPU) |
| OS           | ✅ Windows 10 or 11 |

---

## 🚀 Installation (Windows Instructions)

### 1. Install Python and Pip (if not already)

Download from: <https://www.python.org/downloads/>

> Ensure `Add to PATH` is checked during installation.

### 2. Install [Ollama](https://ollama.com/download)

- Download & install for Windows (includes WSL2 setup)
- After install, verify with:

  ```powershell
  ollama --version
  ```

### 3. Pull the Qwen model

```powershell
ollama pull qwen2.5:1.5b
```

---

## 🛠 Set Up the Project

1. **Clone this repo** or extract the ZIP:

```bash
cd log_inspector
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🧠 Run the App

### Step 1: Start Ollama (in one terminal)

```powershell
ollama run qwen2.5:1.5b
```

Keep this window open!

### Step 2: Start Streamlit app (in a new terminal)

```powershell
streamlit run main.py
```

Streamlit will open in your browser. Upload a `.log` file and start asking questions!

---

## 🧪 Sample Log File

A sample is included in:

```sh
examples/sample.log
```

---

## 📁 Folder Structure

```sh
log_inspector/
├── main.py
├── requirements.txt
├── analyzer/
│   ├── parser.py
│   └── llm_interface.py
├── utils/
│   └── helpers.py
├── examples/
│   └── sample.log
└── README.md
```

---

## 🙌 Tips

- You can switch to other models like `phi`, `mistral` by changing one line in `llm_interface.py`
- To reduce response time, chunk logs to \~5–10 entries
- Works entirely offline — no API keys needed

---

## 🔐 Privacy First

All processing is local. No data is sent to the cloud. Perfect for students, sensitive logs, and offline environments.

---
