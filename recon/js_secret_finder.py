import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class JSSecretFinder:
    """
    محرك استخراج الأسرار من ملفات Javascript (JS Secret Finder)
    يقوم بتحليل ملفات JS للبحث عن مفاتيح API وروابط حساسة.
    """
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.secrets_patterns = {
            "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "S3 Bucket": r"s3\.amazonaws\.com[/][a-z0-9_-]+",
            "Generic Secret": r"(?i)(key|secret|password|auth|token)[\s:=]+['\"]([0-9a-zA-Z-_]{16,})['\"]",
            "Firebase URL": r"https://.*\.firebaseio\.com"
        }

    async def get_js_files(self) -> list:
        """
        استخراج كافة روابط ملفات JS من الصفحة الرئيسية
        """
        js_files = []
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(self.target_url, timeout=15, ssl=False) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        for script in soup.find_all('script'):
                            src = script.get('src')
                            if src:
                                js_files.append(urljoin(self.target_url, src))
        except Exception as e:
            print(f"[!] Error finding JS files on {self.target_url}: {e}")
        return js_files

    async def scan_js_file(self, js_url: str):
        """
        فحص ملف JS واحد بحثاً عن الأسرار
        """
        found_secrets = []
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(js_url, timeout=15, ssl=False) as response:
                    if response.status == 200:
                        content = await response.text()
                        for name, pattern in self.secrets_patterns.items():
                            matches = re.findall(pattern, content)
                            if matches:
                                for match in matches:
                                    found_secrets.append({"type": name, "value": str(match)})
        except:
            pass
        return found_secrets

    async def run(self):
        print(f"[*] Scanning JS files for secrets at: {self.target_url}")
        js_files = await self.get_js_files()
        all_secrets = []
        for js_file in js_files:
            secrets = await self.scan_js_file(js_file)
            if secrets:
                all_secrets.extend(secrets)
        return all_secrets
