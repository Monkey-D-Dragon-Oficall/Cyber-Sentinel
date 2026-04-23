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

async def run_scan(target_domain: str):
    print(BANNER)
    target_url = f"http://{target_domain}"
    
    # 1. Recon Phase
    print("[+] Phase 1: Reconnaissance")
    sub_enum = SubdomainEnum(target_domain)
    subdomains = await sub_enum.run()
    
    asset_disc = AssetDiscovery(target_url)
    fingerprint = await asset_disc.run()
    print(f"[+] Fingerprint: {fingerprint}")
    
    js_finder = JSSecretFinder(target_url)
    secrets = await js_finder.run()
    print(f"[+] Found {len(secrets)} potential secrets in JS files")

    # 2. Vulnerability Scanning Phase
    print("\n[+] Phase 2: Vulnerability Scanning")
    fuzzer = WebFuzzer(target_url)
    fuzz_results = await fuzzer.run()
    print(f"[+] Fuzzing complete. Found {len(fuzz_results)} sensitive paths")

    # 3. Reporting Phase
    print("\n[+] Phase 3: Generating Reports")
    all_results = {
        "Subdomains": subdomains,
        "Fingerprint": [str(fingerprint)],
        "JS Secrets": [str(s) for s in secrets],
        "Sensitive Paths": [str(p) for p in fuzz_results]
    }
    
    reporter = Reporter(target_domain, all_results)
    json_file = reporter.generate_json_report(f"{target_domain}_report.json")
    md_file = reporter.generate_markdown_report(f"{target_domain}_report.md")
    
    print(f"[✔] Scan Complete! Reports saved to:\n - {json_file}\n - {md_file}")

def main():
    parser = argparse.ArgumentParser(description="CyberSentinel: Advanced Security Framework")
    parser.add_argument("-d", "--domain", help="Target domain to scan", required=True)
    args = parser.parse_args()

    try:
        asyncio.run(run_scan(args.domain))
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
