🛡️ Mini SIEM Attack Simulator & Dashboard

A lightweight Security Information and Event Management (SIEM) simulation platform that generates, streams, and visualizes cyber attack logs in real-time.

Built for learning SOC workflows, detection logic, and log analysis — without requiring heavy infrastructure or cloud services.

---

## ⚠️ Disclaimer

This project is strictly for **educational and demonstration purposes only**.

* This tool does NOT perform real attacks.
* All logs are **synthetically generated**.
* No real systems are targeted or exploited.
* Do NOT use similar techniques on systems without proper authorization.

---

## 🧠 Project Overview

This project simulates a mini SOC environment:

Attack Simulation → Log Generation → Analysis → Dashboard Visualization

It helps understand how real SIEM systems:

* Process logs
* Detect suspicious activity
* Display alerts in real time

---

## 🔥 Features

* Simulated attack types:

  * Brute Force
  * Port Scanning
  * SQL Injection
  * Privilege Escalation
  * Lateral Movement
  * Reconnaissance

* Structured logs (JSONL format)

* Local API endpoint (/logs)

* Real-time dashboard (HTML + JS)

* Live log stream with severity filtering

* Alert panel for critical events

* Attack distribution statistics

* Manual attack trigger controls

---

## 🧱 Architecture

Attack Generator (Python)
↓
Log Pipeline (JSONL + Memory Buffer)
↓
HTTP API (localhost:5000/logs)
↓
Dashboard (HTML + JavaScript)

---

## 📁 Project Structure

mini-siem/
│
├── siem_simulator.py
├── siem_logs.jsonl
├── dashboard.html
├── README.md
└── LICENSE

---

## ⚙️ Installation & Setup

### 1. Requirements

* Python 3.8+

### 2. Run the simulator

python siem_simulator.py

You should see:
[*] SIEM API running at http://localhost:5000/logs

---

### 3. Open dashboard

Open dashboard.html in your browser.

---

## 🧪 Simulated Attack Examples

### Brute Force

* Multiple failed login attempts
* High request rate from single IP

### Port Scan

* Large number of ports probed in short time

### SQL Injection

* Suspicious payloads (' OR 1=1, SLEEP())

### Privilege Escalation

* SUID abuse
* Unauthorized system file modification

---

## 🔍 Detection Logic (Conceptual)

### Brute Force Detection

* Track repeated login failures from same IP
* Threshold-based alerting

### SQL Injection Detection

* Pattern matching on known payloads

### Port Scan Detection

* High number of connection attempts in short time

### Privilege Escalation

* Suspicious system-level actions (e.g., /etc/passwd modification)

---

## 📊 Dashboard Capabilities

* Live log stream
* Severity-based filtering (LOW → CRITICAL)
* Alert panel for high-risk events
* Attack distribution visualization
* Manual attack simulation controls

---

## 🚀 Future Improvements

* Detection engine with rule-based alerts
* IP correlation tracking
* MITRE ATT&CK mapping
* Persistent storage (database)
* Integration with real SIEM tools like Wazuh

---

## 🧠 Learning Outcomes

* Log generation & normalization
* Basic SIEM architecture
* Attack simulation techniques
* Detection logic design
* API-based data pipelines
* Real-time monitoring dashboards

---

## 👤 Author

CyberPhantom
Cybersecurity Enthusiast | SOC Aspirant | Python Developer

---

## 📜 License

MIT License
