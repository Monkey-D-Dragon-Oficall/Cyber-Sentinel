import aiohttp

class NotificationManager:
    """
    نظام التنبيهات الفورية (Real-time Notifications)
    إرسال تنبيهات عبر Telegram Webhooks.
    """
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send_telegram_alert(self, message: str):
        """
        إرسال تنبيه إلى تلغرام
        """
        if not self.bot_token or not self.chat_id:
            return False
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🛡️ **CyberSentinel Alert**\n\n{message}",
            "parse_mode": "Markdown"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    return response.status == 200
        except:
            return False
