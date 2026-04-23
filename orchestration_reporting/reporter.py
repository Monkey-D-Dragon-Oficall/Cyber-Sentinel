import json
import os
from datetime import datetime

class Reporter:
    """
    CyberSentinel Omni-Edition - Structural Reporting Engine
    نظام تقارير هيكلي ينشئ مجلداً خاصاً لكل هدف يحتوي على نتائج مفصلة.
    """
    def __init__(self, target: str, results: dict, author: str = "Monkey-D-Dragon-Oficall"):
        self.target = target
        self.results = results
        self.author = author
        self.github = "https://github.com/Monkey-D-Dragon-Oficall"
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # إنشاء هيكل المجلدات: core/storage/reports/target_name/timestamp/
        safe_target = target.replace(".", "_").replace(":", "_").replace("/", "")
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "storage", "reports", safe_target)
        self.session_dir = os.path.join(self.base_dir, self.timestamp)
        
        os.makedirs(self.session_dir, exist_ok=True)

    def display_live_report(self):
        """ عرض حي للنتائج """
        print(f"\n\033[1;92m[+] REPORT GENERATED FOR: {self.target}\033[0m")
        print(f"\033[1;94m[+] STORAGE PATH: {self.session_dir}\033[0m\n")
        
        for category, findings in self.results.items():
            print(f"\033[1;93m[{category.upper()}]\033[0m")
            if not findings:
                print("  └─ No data.")
            else:
                for finding in findings[:10]: # عرض أول 10 نتائج فقط لتجنب الزحام
                    print(f"  └─ {finding}")
                if len(findings) > 10:
                    print(f"  └─ ... and {len(findings)-10} more (check full report)")

    def save_all(self):
        """ حفظ النتائج بشكل مفصل في ملفات منفصلة """
        # 1. حفظ التقرير الشامل JSON
        with open(os.path.join(self.session_dir, "full_report.json"), 'w') as f:
            json.dump({"target": self.target, "author": self.author, "results": self.results}, f, indent=4)
            
        # 2. حفظ كل فئة في ملف نصي منفصل لسهولة القراءة
        for category, findings in self.results.items():
            cat_file = category.lower().replace(" ", "_") + ".txt"
            with open(os.path.join(self.session_dir, cat_file), 'w') as f:
                f.write(f"--- {category} for {self.target} ---\n")
                for item in findings:
                    f.write(f"{item}\n")
                    
        # 3. حفظ ملف Markdown ملخص
        with open(os.path.join(self.session_dir, "summary.md"), 'w') as f:
            f.write(f"# Security Scan Summary: {self.target}\n\n")
            f.write(f"- **Author:** {self.author}\n- **Date:** {self.timestamp}\n\n")
            for category, findings in self.results.items():
                f.write(f"## {category}\n- Total Findings: {len(findings)}\n\n")
                
        return self.session_dir
