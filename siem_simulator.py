import random, time, json, datetime, socket, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ─── Attack Templates ────────────────────────────────────────────
USERS = ['root','admin','ubuntu','pi','oracle','postgres','deploy','jenkins']
SERVICES = ['sshd','nginx','apache2','mysql','sudo','kernel','smb']

def rand_ip():
    return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

ATTACK_TEMPLATES = {
    "BRUTE_FORCE": {
        "severity": ["MEDIUM","HIGH","HIGH","CRITICAL"],
        "logs": [
            lambda: f"Failed password for {random.choice(USERS)} from {rand_ip()} port 22 ssh2",
            lambda: f"PAM: {random.randint(5,50)} authentication failures from {rand_ip()}",
            lambda: f"Repeated login failures — account lockout triggered for {random.choice(USERS)}",
            lambda: f"CRITICAL: Brute force threshold exceeded — {random.randint(100,500)} attempts/min from {rand_ip()}",
        ]
    },
    "PORT_SCAN": {
        "severity": ["LOW","MEDIUM","MEDIUM","HIGH"],
        "logs": [
            lambda: f"nmap: SYN scan from {rand_ip()} — {random.randint(100,1024)} ports probed",
            lambda: f"Unusual connection rate from {rand_ip()}: {random.randint(50,200)} SYNs in 5s",
            lambda: f"Stealth scan detected: FIN/NULL/XMAS packets from {rand_ip()}",
            lambda: f"Aggressive scan: OS fingerprint + version detection from {rand_ip()}",
        ]
    },
    "SQL_INJECTION": {
        "severity": ["HIGH","HIGH","CRITICAL","CRITICAL"],
        "logs": [
            lambda: f"[WAF] SQLi in GET /login?user=' OR 1=1-- from {rand_ip()}",
            lambda: f"UNION SELECT injection attempt on /api/search from {rand_ip()}",
            lambda: f"Blind SQLi: SLEEP({random.randint(3,10)}) payload from {rand_ip()}",
            lambda: f"CRITICAL: Stacked query injection — possible data exfil from {rand_ip()}",
        ]
    },
    "PRIVILEGE_ESCALATION": {
        "severity": ["HIGH","CRITICAL","CRITICAL","CRITICAL"],
        "logs": [
            lambda: f"sudo: {random.choice(USERS)} ran unauthorized command /bin/bash",
            lambda: f"AUDIT: SUID binary /usr/bin/find executed with --exec /bin/sh by UID {random.randint(1000,9999)}",
            lambda: f"CRITICAL: /etc/passwd write attempt detected from PID {random.randint(1000,9999)}",
            lambda: f"Kernel exploit pattern matched: CVE-202{random.randint(0,4)}-{random.randint(1000,9999)}",
        ]
    },
    "LATERAL_MOVEMENT": {
        "severity": ["MEDIUM","HIGH","HIGH","CRITICAL"],
        "logs": [
            lambda: f"SMB: {rand_ip()} accessing \\\\192.168.1.{random.randint(1,254)}\\ADMIN$",
            lambda: f"Pass-the-hash: NTLM relay from {rand_ip()} to internal DC",
            lambda: f"WMI remote execution from {rand_ip()} — possible C2 beacon",
            lambda: f"Mimikatz pattern: lsass.exe memory access from suspicious process",
        ]
    },
    "RECON": {
        "severity": ["LOW","LOW","MEDIUM","MEDIUM"],
        "logs": [
            lambda: f"DNS: zone transfer attempt from {rand_ip()} — refused",
            lambda: f"Nikto scanner detected from {rand_ip()} — {random.randint(50,300)} requests",
            lambda: f"Automated crawl: /.git /.env /admin accessed from {rand_ip()}",
            lambda: f"robots.txt + sitemap probe from {rand_ip()} — recon pattern",
        ]
    }
}

# ─── Log Generator ───────────────────────────────────────────────
log_buffer = []

def generate_log(attack_type=None):
    if not attack_type:
        weights = {"BRUTE_FORCE":20,"PORT_SCAN":20,"RECON":25,
                   "SQL_INJECTION":15,"LATERAL_MOVEMENT":10,"PRIVILEGE_ESCALATION":10}
        attack_type = random.choices(list(weights.keys()), weights=list(weights.values()))[0]

    atk = ATTACK_TEMPLATES[attack_type]
    idx = random.randint(0, len(atk["logs"])-1)
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "severity": atk["severity"][idx],
        "attack_type": attack_type,
        "service": random.choice(SERVICES),
        "host": f"192.168.1.{random.randint(1,10)}",
        "message": atk["logs"][idx](),
        "log_id": f"LOG-{random.randint(10000,99999)}"
    }

def write_to_file(log, path="siem_logs.jsonl"):
    with open(path, "a") as f:
        f.write(json.dumps(log) + "\n")

# ─── HTTP Server (feeds the dashboard) ───────────────────────────
class SIEMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/logs":
            data = json.dumps(log_buffer[-50:]).encode()
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *args): pass  # silence default logging

def start_server():
    server = HTTPServer(("localhost", 5000), SIEMHandler)
    print("[*] SIEM API running at http://localhost:5000/logs")
    server.serve_forever()

# ─── Main Loop ───────────────────────────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    print("[*] Log generator started. Writing to siem_logs.jsonl")
    print("[*] Press Ctrl+C to stop\n")

    try:
        while True:
            log = generate_log()
            log_buffer.append(log)
            if len(log_buffer) > 500: log_buffer.pop(0)
            write_to_file(log)

            # Pretty print to terminal
            sev_color = {"CRITICAL":"\033[91m","HIGH":"\033[93m",
                        "MEDIUM":"\033[33m","LOW":"\033[92m"}
            c = sev_color.get(log["severity"],"\033[0m")
            print(f"{c}[{log['severity']:8}]\033[0m {log['timestamp'][11:19]} "
                  f"\033[96m{log['attack_type']:22}\033[0m {log['message']}")

            time.sleep(random.uniform(0.3, 1.5))
    except KeyboardInterrupt:
        print("\n[*] SIEM stopped.")