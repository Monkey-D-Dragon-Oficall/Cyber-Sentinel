import aiohttp
import asyncio

class AssetDiscovery:
    """
    محرك اكتشاف الأصول (Asset Discovery & Fingerprinting)
    التعرف على التقنيات المستخدمة في الموقع المستهدف.
    """
    def __init__(self, target_url: str):
        self.target_url = target_url

    async def get_fingerprint(self):
        """
        تحليل رؤوس الاستجابة (Headers) للتعرف على الخادم والتقنيات
        """
        fingerprint = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.target_url, timeout=10) as response:
                    headers = response.headers
                    fingerprint['Server'] = headers.get('Server', 'Unknown')
                    fingerprint['X-Powered-By'] = headers.get('X-Powered-By', 'Unknown')
                    fingerprint['Content-Type'] = headers.get('Content-Type', 'Unknown')
                    
                    # محاولة بسيطة للتعرف على CMS
                    body = await response.text()
                    if "wp-content" in body:
                        fingerprint['CMS'] = "WordPress"
                    elif "drupal" in body.lower():
                        fingerprint['CMS'] = "Drupal"
                    else:
                        fingerprint['CMS'] = "Unknown"
                        
        except Exception as e:
            print(f"[!] Error fingerprinting: {e}")
        return fingerprint

    async def run(self):
        print(f"[*] Fingerprinting target: {self.target_url}")
        return await self.get_fingerprint()
