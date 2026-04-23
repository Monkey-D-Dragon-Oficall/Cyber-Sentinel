import asyncio
import aiohttp
import re
from typing import List, Set

class SubdomainEnum:
    """
    CyberSentinel 2050 - Intelligent Recon Engine
    نظام استطلاع ذكي يجمع بين المصادر السلبية والنشطة بدقة متناهية.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.subdomains: Set[str] = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def fetch_from_crtsh(self) -> List[str]:
        """
        استخراج النطاقات الفرعية من شهادات SSL مع معالجة ذكية للأخطاء
        """
        if not self.domain or "." not in self.domain:
            return []
            
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        try:
                            data = await response.json()
                            for entry in data:
                                name = entry.get('name_value', '')
                                sub_list = name.split('\n')
                                for sub in sub_list:
                                    sub = sub.strip().lower()
                                    if sub.endswith(self.domain) and "*" not in sub:
                                        self.subdomains.add(sub)
                        except:
                            # fallback to regex if json fails
                            text = await response.text()
                            matches = re.findall(r'<td>([a-z0-9.-]+\.' + re.escape(self.domain) + r')</td>', text)
                            for match in matches:
                                self.subdomains.add(match.lower())
        except Exception as e:
            print(f"    \033[91m[!] Recon Error (crt.sh): {e}\033[0m")
        return list(self.subdomains)

    async def run(self):
        print(f"    \033[94m[*] Initiating Deep Recon for: {self.domain}\033[0m")
        await self.fetch_from_crtsh()
        # إضافة مصادر أخرى مستقبلاً هنا
        return sorted(list(self.subdomains))
