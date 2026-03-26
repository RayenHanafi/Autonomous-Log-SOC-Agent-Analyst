import requests
from google import genai
import json

def get_prompt_gemini(log_summary):
    """Complex prompt for capable cloud-based models like Gemini"""
    prompt = f"""
        You are an autonomous SOC analyst. Analyze the following parsed auth log data
        and produce a detailed incident report. Include:
        - Threat type
        - Source IPs
        - Severity
        - Summary
        - Recommendations
        Given the following log summary, provide your analysis and insights as a .html report.

        The generated HTML report must follow this exact CSS and structure.
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <title>Incident Report - Authentication Log Analysis</title>
          <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            * {{ box-sizing: border-box; margin: 0; padding: 0; }}

            body {{
                font-family: 'Inter', Arial, sans-serif;
                line-height: 1.6;
                background: #0f1117;
                color: #e2e8f0;
                padding: 30px 20px;
            }}

            .report-container {{
                max-width: 1100px;
                margin: 0 auto;
                background: #1a1d27;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            }}

            .report-header {{
                background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 100%);
                padding: 36px 40px;
                border-bottom: 1px solid #2d3748;
            }}

            .report-header h1 {{
                font-size: 1.6rem;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: -0.3px;
            }}

            .report-header .meta {{
                margin-top: 8px;
                font-size: 0.85rem;
                color: #90a4b7;
            }}

            .report-body {{ padding: 32px 40px; }}

            h2 {{
                font-size: 1rem;
                font-weight: 600;
                color: #7eb3ff;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                margin-bottom: 16px;
                padding-bottom: 8px;
                border-bottom: 1px solid #2d3748;
            }}

            .section {{
                margin-bottom: 32px;
                background: #20243a;
                border: 1px solid #2d3748;
                border-radius: 10px;
                padding: 24px;
            }}

            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 8px;
            }}

            .summary-card {{
                background: #1a1d27;
                border: 1px solid #2d3748;
                border-radius: 8px;
                padding: 16px;
            }}

            .summary-card .label {{
                font-size: 0.75rem;
                color: #90a4b7;
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }}

            .summary-card .value {{
                font-size: 1.25rem;
                font-weight: 700;
                color: #e2e8f0;
                margin-top: 4px;
            }}

            .severity-high {{ color: #fc8181; font-weight: 600; }}
            .severity-medium {{ color: #f6ad55; font-weight: 600; }}
            .severity-low {{ color: #68d391; font-weight: 600; }}

            p {{ color: #a0aec0; margin-bottom: 12px; font-size: 0.95rem; }}

            ul, ol {{ padding-left: 20px; color: #a0aec0; font-size: 0.95rem; }}
            li {{ margin-bottom: 8px; }}
            li strong {{ color: #e2e8f0; }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 12px;
                font-size: 0.9rem;
            }}

            thead tr {{
                background: #0f2744;
            }}

            th {{
                padding: 12px 14px;
                text-align: left;
                font-weight: 600;
                color: #7eb3ff;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-bottom: 1px solid #2d3748;
            }}

            td {{
                padding: 11px 14px;
                border-bottom: 1px solid #2a2f45;
                color: #cbd5e0;
            }}

            tbody tr:hover {{ background: #252a40; transition: background 0.15s; }}
            tbody tr:last-child td {{ border-bottom: none; }}

            code {{
                background: #0f1117;
                color: #7eb3ff;
                padding: 2px 7px;
                border-radius: 4px;
                font-size: 0.85rem;
                font-family: 'Courier New', monospace;
            }}
            </style>         
        </head>
        <body>
          <div class="report-container">
            <h1>Security Incident Report: Authentication Log Analysis</h1>
            <!-- Sections: Incident Overview, Summary of Findings, Source IPs of Interest (table), System Activity Context, Recommendations -->
          </div>
        </body>
        </html>

        Data:
        {json.dumps(log_summary, indent=2)}
        """
    return prompt

def get_prompt_ollama(log_summary):
    prompt = f"""Generate a complete HTML report analyzing authentication logs DATA . Output ONLY valid HTML code.
    this is the data:
    {json.dumps(log_summary, indent=2)}
    The HTML report should include:
    - Threat type
    - Source IPs
    - Severity
    - Summary
    - Recommendations
    
    Output ONLY raw HTML code. No markdown. No backticks. No explanations. No comments. Just continue the HTML below and close it properly. 

"""
    
    return prompt

class GeminiBackend:
    def __init__(self, api_key, model):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def analyze_log_summary(self, log_summary):
        prompt = get_prompt_gemini(log_summary)
        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt)
            return response.text
        except Exception as e:
            return f"AI analysis failed: {str(e)}"

class OllamaBackend:
    def __init__(self, model, url="http://localhost:11434"):
        self.model = model
        self.url = url.rstrip('/')

    def analyze_log_summary(self, log_summary):
        prompt = get_prompt_ollama(log_summary)
        try:
            response = requests.post(f"{self.url}/api/generate", json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.ConnectionError:
            print(f"[ERROR] Cannot connect to Ollama at {self.url}. Is it running?")
            exit(1)
        except Exception as e:
            return f"AI analysis failed: {str(e)}"
