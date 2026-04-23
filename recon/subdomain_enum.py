import asyncio
import aiohttp
import re
from typing import List, Set

class SubdomainEnum:
    """
    محرك استخراج النطاقات الفرعية (Subdomain Enumeration Engine)
    يجمع بين البحث السلبي عبر crt.sh والتحقق النشط.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.subdomains: Set[str] = set()

    async def fetch_from_crtsh(self) -> List[str]:
        """
        استخراج النطاقات الفرعية من شهادات SSL عبر crt.sh
        """
        if not self.domain or "." not in self.domain:
            return []
            
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=20) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            for entry in data:
                                name = entry.get('name_value', '')
                                sub_list = name.split('\n')
                                for sub in sub_list:
                                    if sub.endswith(self.domain) and "*" not in sub:
                                        self.subdomains.add(sub.strip().lower())
                        except Exception:
                            # أحياناً crt.sh يعيد نصاً بدلاً من JSON عند الضغط العالي
                            pass
        except Exception as e:
            print(f"[!] Error fetching from crt.sh: {e}")
        return list(self.subdomains)

    async def check_alive(self, subdomain: str) -> bool:
        """
        التحقق مما إذا كان النطاق الفرعي نشطاً
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{subdomain}", timeout=5) as response:
                    return True
        except:
            return False

    async def run(self):
        print(f"[*] Starting Subdomain Enumeration for: {self.domain}")
        await self.fetch_from_crtsh()
        print(f"[+] Found {len(self.subdomains)} subdomains from crt.sh")
        return list(self.subdomains)
