# Prerequisites:
# pip install google-genai requests

import os
import sys
import webbrowser
from datetime import datetime
from parser import AuthLogParser
from backends import GeminiBackend, OllamaBackend

def clean_html_response(response_text):
    text = response_text.strip()
    if text.startswith("```html"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def main():
    print("============================================================")
    print("                 Autonomous SOC Analyst - CLI Tool")
    print("""
            ┌──────────────────────────────────────────┐
            │░█▀▀░█▀█░█▀▀░░░█▀█░█▀█░█▀█░█░░░█░█░█▀▀░▀█▀│
            │░▀▀█░█░█░█░░░░░█▀█░█░█░█▀█░█░░░░█░░▀▀█░░█░│
            │░▀▀▀░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░░▀░│
            └──────────────────────────────────────────┘ 
""")

    print("============================================================")
    print()
    print("[*] Select AI backend:")
    print("  [1] Google Gemini  (requires API key)")
    print("  [2] Ollama         (local model, no API key needed)")
    print()
    
    backend_choice = input("Enter choice [1/2]: ").strip()
    
    backend = None
    if backend_choice == "1":
        api_key = input("Enter your Gemini API key: ").strip()
        print("Available Gemini models:")
        print("  [1] gemini-flash-lite-latest  (fast, lightweight)")
        print("  [2] gemini-flash-latest          (balanced)")
        print("  [3] gemini-pro-latest          (most capable)")
        model_choice = input("Enter model choice [1/2/3]: ").strip()
        
        model_name = "gemini-flash-lite-latest"
        if model_choice == "2":
            model_name = "gemini-flash-latest"
        elif model_choice == "3":
            model_name = "gemini-pro-latest"
            
        backend = GeminiBackend(api_key, model_name)
        backend_name = "gemini"
        
    elif backend_choice == "2":
        model_name = input("Enter Ollama model name (e.g. llama3, mistral, phi3): ").strip()
        url = input("Enter Ollama URL [default: http://localhost:11434]: ").strip()
        
        if not url:
            url = "http://localhost:11434"
            
        backend = OllamaBackend(model_name, url=url)
        backend_name = "ollama"
    else:
        print("[ERROR] Invalid choice. Exiting.")
        sys.exit(1)
        
    print()
    log_path = input("Enter path to auth.log file (e.g. /var/log/auth.log or ./auth.log): ").strip()
    
    if not os.path.exists(log_path):
        print(f"[ERROR] File not found: {log_path}")
        sys.exit(1)
        
    print()
    print(f"[*] Parsing log file: {log_path} ...")
    
    parser = AuthLogParser(log_path)
    parsed_data = parser.parse()
    
    unique_ips = len(parsed_data.get("ip_activity", {}))
    cron_events = parsed_data.get("cron_jobs", 0)
    sudo_commands = len(parsed_data.get("sudo_activity", []))
    
    print(f"[+] Parsed: {unique_ips} unique IPs, {cron_events} cron events, {sudo_commands} sudo commands")
    print(f"[*] Sending data to AI backend ({backend_name}) ...")
    
    report_content = backend.analyze_log_summary(parsed_data)
    
    print("[*] Generating HTML report ...")
    report_content = clean_html_response(report_content)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"soc_report_{timestamp}.html"
    
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"[+] Report saved: {report_filename}")
    print("[*] Opening report in browser...")
    
    webbrowser.open(f"file://{os.path.abspath(report_filename)}")

if __name__ == "__main__":
    main()
