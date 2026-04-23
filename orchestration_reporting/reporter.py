import json
from datetime import datetime

class Reporter:
    """
    نظام توليد التقارير (Automated Professional Reporting)
    توليد تقارير بصيغة JSON و Markdown (قابلة للتحويل لـ PDF).
    """
    def __init__(self, target: str, results: dict):
        self.target = target
        self.results = results
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_json_report(self, filename: str):
        """
        توليد تقرير بصيغة JSON
        """
        report_data = {
            "target": self.target,
            "scan_time": self.timestamp,
            "vulnerabilities": self.results
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        return filename

    def generate_markdown_report(self, filename: str):
        """
        توليد تقرير بصيغة Markdown احترافية
        """
        md_content = f"# 🛡️ CyberSentinel Security Report\n\n"
        md_content += f"**Target:** {self.target}\n"
        md_content += f"**Scan Date:** {self.timestamp}\n\n"
        md_content += "--- \n\n"
        md_content += "## 🔍 Summary of Findings\n\n"
        
        for category, findings in self.results.items():
            md_content += f"### {category}\n"
            if not findings:
                md_content += "No vulnerabilities found.\n\n"
            else:
                for finding in findings:
                    md_content += f"- **Finding:** {finding}\n"
                md_content += "\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        return filename
