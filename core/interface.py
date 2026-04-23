import os
import sys

class CyberInterface:
    """
    الواجهة التفاعلية لأداة CyberSentinel
    توفر قائمة سهلة للتحكم في الأداة.
    """
    def __init__(self, author="Monkey-D-Dragon-Oficall"):
        self.author = author
        self.github = "https://github.com/Monkey-D-Dragon-Oficall"
        self.banner = f"""
    \033[94m
    ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
    \033[92m
    🛡️ CyberSentinel: Advanced Security Framework
    \033[93mDeveloped by: {self.author}\033[0m
    \033[95mGitHub: {self.github}\033[0m
    ---------------------------------------------------------
    """

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_menu(self):
        self.clear_screen()
        print(self.banner)
        print("\033[1m[ Main Menu ]\033[0m")
        print("1. Start Full Security Scan")
        print("2. Reconnaissance Only (Subdomains, JS Secrets)")
        print("3. Vulnerability Scanning Only (Fuzzing, API)")
        print("4. View Saved Reports")
        print("5. Settings & Notifications")
        print("0. Exit")
        print("\n" + "-"*57)
        
        choice = input("\033[92m[?]\033[0m Select an option: ")
        return choice

    def get_target(self):
        print("\n" + "="*57)
        target = input("\033[92m[?]\033[0m Enter Target Domain or URL: ")
        return target

    def show_status(self, message, status_type="info"):
        colors = {
            "info": "\033[94m[*]\033[0m",
            "success": "\033[92m[+]\033[0m",
            "warning": "\033[93m[!]\033[0m",
            "error": "\033[91m[-]\033[0m"
        }
        print(f"{colors.get(status_type, '[*]')} {message}")
