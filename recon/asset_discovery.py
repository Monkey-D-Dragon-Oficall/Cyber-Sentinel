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
            # استخدام رؤوس طلبات واقعية لتجنب الحظر
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(self.target_url, timeout=15, ssl=False) as response:
                    resp_headers = response.headers
                    fingerprint['Server'] = resp_headers.get('Server', 'Unknown')
                    fingerprint['X-Powered-By'] = resp_headers.get('X-Powered-By', 'Unknown')
                    fingerprint['Content-Type'] = resp_headers.get('Content-Type', 'Unknown')
                    
                    try:
                        body = await response.text()
                        if "wp-content" in body:
                            fingerprint['CMS'] = "WordPress"
                        elif "drupal" in body.lower():
                            fingerprint['CMS'] = "Drupal"
                        else:
                            fingerprint['CMS'] = "Unknown"
                    except:
                        fingerprint['CMS'] = "Unknown"
                        
        except Exception as e:
            print(f"[!] Error fingerprinting {self.target_url}: {e}")
        return fingerprint

    async def run(self):
        print(f"[*] Fingerprinting target: {self.target_url}")
        return await self.get_fingerprint()
