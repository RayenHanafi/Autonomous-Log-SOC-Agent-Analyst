import re
from collections import defaultdict

class AuthLogParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ip_activity = defaultdict(lambda: {
            "failed": 0,
            "success": 0,
            "bruteforce": 0,
            "weird_activity": 0,
            "connections": 0,
            "suspicious_login": False
        })
        self.sudo_activity = []
        self.cron_jobs = 0

    def parse(self):
        with open(self.file_path, "r") as f:
            for line in f:
                self._parse_line(line)
        return self._build_summary()

    def _parse_line(self, line):
        # Extract IP if exists
        ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
        ip = ip_match.group(1) if ip_match else None

        # Failed login
        if "Failed password" in line and ip:
            self.ip_activity[ip]["failed"] += 1

        # Successful login
        elif "Accepted" in line and ip:
            self.ip_activity[ip]["success"] += 1

        # Bruteforce detection
        elif "maximum authentication attempts exceeded" in line and ip:
            self.ip_activity[ip]["bruteforce"] += 1

        # Weird SSH behavior
        elif "Bad protocol version" in line and ip:
            self.ip_activity[ip]["weird_activity"] += 1

        # Connection tracking
        elif "Connection" in line and ip:
            self.ip_activity[ip]["connections"] += 1

        # SUDO activity
        if "sudo:" in line:
            user_match = re.search(r'sudo:\s+(\w+)', line)
            command_match = re.search(r'COMMAND=(.*)', line)
            if user_match:
                user = user_match.group(1)
                command = command_match.group(1) if command_match else "unknown"
                self.sudo_activity.append({
                    "user": user,
                    "command": command.strip()
                })

        # CRON activity
        if "CRON" in line:
            self.cron_jobs += 1

        # Suspicious login check
        if ip:
            if self.ip_activity[ip]["weird_activity"] > 0 and self.ip_activity[ip]["success"] > 0:
                self.ip_activity[ip]["suspicious_login"] = True

    def _build_summary(self):
        return {
            "ip_activity": dict(self.ip_activity),
            "sudo_activity": self.sudo_activity,
            "cron_jobs": self.cron_jobs
        }