import json
from datetime import datetime

import os

class Reporter:
    """
    نظام توليد التقارير (Automated Professional Reporting)
    توليد تقارير بصيغة JSON و Markdown مع حفظها في مجلد مخصص.
    """
    def __init__(self, target: str, results: dict, author: str = "Monkey-D-Dragon-Oficall"):
        self.target = target
        self.results = results
        self.author = author
        self.github = "https://github.com/Monkey-D-Dragon-Oficall"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def display_live_report(self):
        """
        عرض النتائج مباشرة في الواجهة بشكل منسق
        """
        print(f"\n\033[92m" + "="*60)
        print(f"📊 LIVE SECURITY REPORT FOR: {self.target}")
        print(f"👤 Author: {self.author}")
        print(f"📅 Date: {self.timestamp}")
        print("="*60 + "\033[0m")
        
        for category, findings in self.results.items():
            print(f"\n\033[1m[ {category} ]\033[0m")
            if not findings:
                print("  - No findings in this category.")
            else:
                for finding in findings:
                    print(f"  \033[94m»\033[0m {finding}")
        print(f"\n\033[92m" + "="*60 + "\033[0m\n")

    def generate_json_report(self, filename: str, custom_path: str = None):
        """
        توليد تقرير بصيغة JSON مع خيار مسار مخصص
        """
        save_dir = custom_path if custom_path else self.report_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            
        filepath = os.path.join(save_dir, filename)
        report_data = {
            "target": self.target,
            "scan_time": self.timestamp,
            "author": self.author,
            "github": self.github,
            "vulnerabilities": self.results
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        return filepath

    def generate_markdown_report(self, filename: str, custom_path: str = None):
        """
        توليد تقرير بصيغة Markdown احترافية مع خيار مسار مخصص
        """
        save_dir = custom_path if custom_path else self.report_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        filepath = os.path.join(save_dir, filename)
        md_content = f"# 🛡️ CyberSentinel Security Report\n\n"
        md_content += f"**Target:** {self.target}\n"
        md_content += f"**Scan Date:** {self.timestamp}\n"
        md_content += f"**Developed by:** {self.author}\n"
        md_content += f"**GitHub:** {self.github}\n\n"
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
