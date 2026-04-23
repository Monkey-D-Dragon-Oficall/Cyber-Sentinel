import asyncio
import argparse
import sys
from recon.subdomain_enum import SubdomainEnum
from recon.asset_discovery import AssetDiscovery
from recon.js_secret_finder import JSSecretFinder
from vulnerability_scanner.web_fuzzer import WebFuzzer
from ai_evasion.evasion_system import EvasionSystem
from orchestration_reporting.reporter import Reporter

BANNER = """
🛡️ CyberSentinel: Advanced Security Orchestration Framework
---------------------------------------------------------
"""

from urllib.parse import urlparse

def clean_target(target: str):
    """
    تنظيف المدخلات لاستخراج النطاق والرابط الصحيح
    """
    parsed = urlparse(target)
    if not parsed.scheme:
        # إذا لم يتم إدخال بروتوكول، نفترض أنه نطاق
        domain = target.split('/')[0]
        url = f"https://{domain}"
    else:
        domain = parsed.netloc
        url = f"{parsed.scheme}://{domain}"
    
    return domain, url

from core.interface import CyberInterface

async def run_scan(target_input: str, mode="full"):
    interface = CyberInterface()
    target_domain, target_url = clean_target(target_input)
    
    interface.show_status(f"Target Domain: {target_domain}")
    interface.show_status(f"Target URL: {target_url}\n")

    all_results = {}

    # 1. Recon Phase
    if mode in ["full", "recon"]:
        interface.show_status("Phase 1: Reconnaissance", "success")
        sub_enum = SubdomainEnum(target_domain)
        subdomains = await sub_enum.run()
        
        asset_disc = AssetDiscovery(target_url)
        fingerprint = await asset_disc.run()
        interface.show_status(f"Fingerprint: {fingerprint}")
        
        js_finder = JSSecretFinder(target_url)
        secrets = await js_finder.run()
        interface.show_status(f"Found {len(secrets)} potential secrets in JS files")
        
        all_results.update({
            "Subdomains": subdomains,
            "Fingerprint": [str(fingerprint)],
            "JS Secrets": [str(s) for s in secrets]
        })

    # 2. Vulnerability Scanning Phase
    if mode in ["full", "vuln"]:
        interface.show_status("\nPhase 2: Vulnerability Scanning", "success")
        fuzzer = WebFuzzer(target_url)
        fuzz_results = await fuzzer.run()
        interface.show_status(f"Fuzzing complete. Found {len(fuzz_results)} sensitive paths")
        
        all_results.update({
            "Sensitive Paths": [str(p) for p in fuzz_results]
        })

    # 3. Reporting Phase
    interface.show_status("\nPhase 3: Generating Reports", "success")
    reporter = Reporter(target_domain, all_results)
    
    # عرض التقرير المباشر فوراً
    reporter.display_live_report()
    
    # تخيير المستخدم حول الحفظ
    print("\033[93m[?] How would you like to save the report?\033[0m")
    print("1. Save with default name in 'reports/' folder")
    print("2. Save with custom name and path")
    print("3. Don't save, just show on screen")
    
    save_choice = input("\nSelect option (1-3): ")
    
    if save_choice == '1':
        safe_filename = target_domain.replace(".", "_").replace(":", "_")
        json_file = reporter.generate_json_report(f"{safe_filename}_report.json")
        md_file = reporter.generate_markdown_report(f"{safe_filename}_report.md")
        interface.show_status(f"Reports saved successfully in 'reports/' folder.", "success")
    elif save_choice == '2':
        custom_name = input("Enter custom filename (without extension): ")
        custom_path = input("Enter custom directory path (press Enter for current dir): ")
        if not custom_path: custom_path = "."
        
        json_file = reporter.generate_json_report(f"{custom_name}.json", custom_path)
        md_file = reporter.generate_markdown_report(f"{custom_name}.md", custom_path)
        interface.show_status(f"Reports saved in: {os.path.abspath(custom_path)}", "success")
    else:
        interface.show_status("Report not saved to disk.", "warning")

async def interactive_main():
    interface = CyberInterface()
    while True:
        choice = interface.show_menu()
        
        if choice == '1':
            target = interface.get_target()
            await run_scan(target, mode="full")
            input("\nPress Enter to return to menu...")
        elif choice == '2':
            target = interface.get_target()
            await run_scan(target, mode="recon")
            input("\nPress Enter to return to menu...")
        elif choice == '3':
            target = interface.get_target()
            await run_scan(target, mode="vuln")
            input("\nPress Enter to return to menu...")
        elif choice == '4':
            print("\n[ Saved Reports ]")
            if os.path.exists("reports"):
                files = os.listdir("reports")
                for f in files:
                    if f != ".gitkeep":
                        print(f" - {f}")
            else:
                print("No reports found.")
            input("\nPress Enter to return to menu...")
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Try again.")
            await asyncio.sleep(1)

def main():
    if len(sys.argv) > 1:
        # CLI Mode
        parser = argparse.ArgumentParser(description="CyberSentinel: Advanced Security Framework")
        parser.add_argument("-d", "--domain", help="Target domain to scan", required=True)
        args = parser.parse_args()
        try:
            asyncio.run(run_scan(args.domain))
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted.")
            sys.exit(0)
    else:
        # Interactive Mode
        try:
            asyncio.run(interactive_main())
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()
