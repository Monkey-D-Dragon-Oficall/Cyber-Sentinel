import asyncio
import argparse
import sys
import os
from urllib.parse import urlparse
from recon.subdomain_enum import SubdomainEnum
from recon.asset_discovery import AssetDiscovery
from recon.js_secret_finder import JSSecretFinder
from vulnerability_scanner.web_fuzzer import WebFuzzer
from ai_evasion.evasion_system import EvasionSystem
from orchestration_reporting.reporter import Reporter
from core.interface import CyberInterface

def clean_target(target: str):
    """
    تنظيف المدخلات لاستخراج النطاق والرابط الصحيح بدقة 2050
    """
    target = target.strip()
    if not target: return None, None
    
    parsed = urlparse(target)
    if not parsed.scheme:
        domain = target.split('/')[0]
        url = f"https://{domain}"
    else:
        domain = parsed.netloc
        url = f"{parsed.scheme}://{domain}"
    
    return domain, url

async def run_scan(target_input: str, mode="full"):
    interface = CyberInterface()
    target_domain, target_url = clean_target(target_input)
    
    if not target_domain:
        interface.show_status("Invalid target input.", "error")
        return

    interface.show_status(f"Target Vector: {target_domain}")
    interface.show_status(f"Access URL: {target_url}\n")

    all_results = {}

    # 1. Recon Phase
    if mode in ["full", "recon"]:
        interface.show_status("Initiating Phase 1: Deep Reconnaissance", "success")
        sub_enum = SubdomainEnum(target_domain)
        subdomains = await sub_enum.run()
        
        asset_disc = AssetDiscovery(target_url)
        fingerprint = await asset_disc.run()
        interface.show_status(f"Fingerprint Analysis: {fingerprint}")
        
        js_finder = JSSecretFinder(target_url)
        secrets = await js_finder.run()
        interface.show_status(f"JS Intelligence: Found {len(secrets)} potential secrets")
        
        all_results.update({
            "Subdomains Detected": subdomains,
            "System Fingerprint": [f"{k}: {v}" for k, v in fingerprint.items()],
            "JS Intelligence (Secrets)": [f"[{s['type']}] {s['value']}" for s in secrets]
        })

    # 2. Vulnerability Scanning Phase
    if mode in ["full", "vuln"]:
        interface.show_status("\nInitiating Phase 2: Hyper-Vulnerability Fuzzing", "success")
        fuzzer = WebFuzzer(target_url)
        fuzz_results = await fuzzer.run()
        interface.show_status(f"Fuzzing complete. {len(fuzz_results)} sensitive vectors identified.")
        
        all_results.update({
            "Vulnerability Vectors (Fuzzing)": fuzz_results
        })

    # 3. Reporting Phase
    interface.show_status("\nInitiating Phase 3: Intelligence Synthesis", "success")
    reporter = Reporter(target_domain, all_results)
    
    # عرض التقرير المباشر
    reporter.display_live_report()
    
    # نظام الحفظ الذكي 2050
    print("\033[1;93m[?] SELECT STORAGE PROTOCOL:\033[0m")
    print("1. Internal Secure Storage (core/storage/reports/)")
    print("2. External Custom Export (Choose path)")
    print("3. Volatile Session (No save)")
    
    save_choice = input("\n[#] Protocol: ")
    
    if save_choice in ['1', '2']:
        safe_filename = target_domain.replace(".", "_").replace(":", "_")
        custom_path = None
        if save_choice == '2':
            custom_path = input("[?] Enter export directory path: ")
            if not custom_path: custom_path = "."
        
        json_file, md_file = reporter.save_report(f"{safe_filename}_report", custom_path)
        interface.show_status(f"Intelligence saved to: {os.path.abspath(json_file)}", "success")
    else:
        interface.show_status("Session terminated without data persistence.", "warning")

async def interactive_main():
    interface = CyberInterface()
    while True:
        choice = interface.show_menu()
        
        if choice == '1':
            target = interface.get_target()
            await run_scan(target, mode="full")
            input("\n[!] Press Enter to return to Neural Center...")
        elif choice == '2':
            target = interface.get_target()
            await run_scan(target, mode="recon")
            input("\n[!] Press Enter to return to Neural Center...")
        elif choice == '3':
            target = interface.get_target()
            await run_scan(target, mode="vuln")
            input("\n[!] Press Enter to return to Neural Center...")
        elif choice == '4':
            print("\n\033[1;97m[ INTERNAL STORAGE ACCESS ]\033[0m")
            report_dir = os.path.join(os.path.dirname(__file__), "core", "storage", "reports")
            if os.path.exists(report_dir):
                files = [f for f in os.listdir(report_dir) if f != ".gitkeep"]
                if not files:
                    print("    \033[90m└─ Storage is empty.\033[0m")
                for f in files:
                    print(f"    \033[92m└─▶\033[0m {f}")
            else:
                print("    \033[91m└─ Storage offline.\033[0m")
            input("\n[!] Press Enter to return to Neural Center...")
        elif choice == '0':
            print("\n\033[1;91m[!] Session Terminated. Goodbye, Commander.\033[0m")
            break
        else:
            print("\n\033[91m[!] Invalid Input Sequence.\033[0m")
            await asyncio.sleep(1)

def main():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="CyberSentinel 2050")
        parser.add_argument("-d", "--domain", help="Target domain", required=True)
        args = parser.parse_args()
        try:
            asyncio.run(run_scan(args.domain))
        except KeyboardInterrupt:
            print("\n[!] Session Aborted.")
            sys.exit(0)
    else:
        try:
            asyncio.run(interactive_main())
        except KeyboardInterrupt:
            print("\n[!] Session Aborted.")
            sys.exit(0)

if __name__ == "__main__":
    main()
