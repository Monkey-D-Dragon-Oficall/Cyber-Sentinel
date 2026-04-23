import json
import os
from datetime import datetime

class Reporter:
    """
    CyberSentinel 2050 - Advanced Reporting Engine
    نظام تقارير مستقبلي يدمج النتائج داخلياً ويوفر عرضاً حياً فائق الدقة.
    """
    def __init__(self, target: str, results: dict, author: str = "Monkey-D-Dragon-Oficall"):
        self.target = target
        self.results = results
        self.author = author
        self.github = "https://github.com/Monkey-D-Dragon-Oficall"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # المجلد الداخلي الجديد للبلاغات
        self.internal_storage = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "storage", "reports")
        if not os.path.exists(self.internal_storage):
            os.makedirs(self.internal_storage, exist_ok=True)

    def display_live_report(self):
        """
        عرض النتائج مباشرة بتنسيق مستقبلي فائق الجودة
        """
        print(f"\n\033[1;96m" + "╔" + "═"*68 + "╗")
        print(f"║ \033[1;92mCYBERSENTINEL 2050 - QUANTUM SECURITY REPORT\033[1;96m {' '*(23)} ║")
        print(f"╠" + "═"*68 + "╣")
        print(f"║ \033[1mTARGET:\033[0m {self.target.ljust(58)} ║")
        print(f"║ \033[1mAUTHOR:\033[0m {self.author.ljust(58)} ║")
        print(f"║ \033[1mSTAMP :\033[0m {self.timestamp.ljust(58)} ║")
        print(f"╚" + "═"*68 + "╝\033[0m")
        
        for category, findings in self.results.items():
            print(f"\n\033[1;93m[⚡] {category.upper()}\033[0m")
            if not findings:
                print("    \033[90m└─ No anomalies detected in this sector.\033[0m")
            else:
                for finding in findings:
                    print(f"    \033[92m└─▶\033[0m {finding}")
        print(f"\n\033[1;96m" + "═"*70 + "\033[0m\n")

    def save_report(self, filename: str, custom_path: str = None):
        """
        حفظ التقرير في المجلد الداخلي أو مسار مخصص
        """
        target_dir = custom_path if custom_path else self.internal_storage
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        json_path = os.path.join(target_dir, f"{filename}.json")
        md_path = os.path.join(target_dir, f"{filename}.md")
        
        report_data = {
            "metadata": {
                "version": "2050.1.0",
                "author": self.author,
                "github": self.github,
                "timestamp": self.timestamp,
                "target": self.target
            },
            "findings": self.results
        }
        
        # Save JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
            
        # Save Markdown
        md_content = f"# 🛡️ CyberSentinel 2050 - Security Analysis\n\n"
        md_content += f"**Target:** `{self.target}`\n"
        md_content += f"**Analyst:** {self.author}\n"
        md_content += f"**GitHub:** {self.github}\n"
        md_content += f"**Timestamp:** {self.timestamp}\n\n"
        md_content += "---\n\n## 🔍 Intelligence Summary\n\n"
        
        for category, findings in self.results.items():
            md_content += f"### ⚡ {category}\n"
            if not findings:
                md_content += "_No critical findings._\n\n"
            else:
                for finding in findings:
                    md_content += f"- {finding}\n"
                md_content += "\n"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return json_path, md_path
