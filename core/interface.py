import os
import sys

class CyberInterface:
    """
    CyberSentinel 2050 - Neural Interface
    واجهة مستقبلية توفر تحكماً كاملاً وعرضاً داخلياً للتقارير.
    """
    def __init__(self, author="Monkey-D-Dragon-Oficall"):
        self.author = author
        self.github = "https://github.com/Monkey-D-Dragon-Oficall"
        self.version = "2050.OMNI-EDITION"
        self.banner = f"""
    \033[1;96m
    ╔══════════════════════════════════════════════════════════════════════╗
    ║  \033[1;92m██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗\033[1;96m  ║
    ║  \033[1;92m██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║\033[1;96m  ║
    ║  \033[1;92m██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║\033[1;96m  ║
    ║  \033[1;92m██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║\033[1;96m  ║
    ║  \033[1;92m╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║\033[1;96m  ║
    ║  \033[1;92m ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝\033[1;96m  ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║  \033[1;93m[>] SYSTEM VERSION: {self.version.ljust(44)}\033[1;96m ║
    ║  \033[1;93m[>] DEVELOPED BY  : {self.author.ljust(44)}\033[1;96m ║
    ║  \033[1;93m[>] GITHUB        : {self.github.ljust(44)}\033[1;96m ║
    ╚══════════════════════════════════════════════════════════════════════╝\033[0m
    """

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_menu(self):
        self.clear_screen()
        print(self.banner)
        print("\033[1;97m[ ⚡ OMNI-CONTROL CENTER ]\033[0m")
        print("\033[92m[1]\033[0m Full Omni-Scan (Recon + Ports + Vuln)")
        print("\033[92m[2]\033[0m Deep Reconnaissance (OSINT & JS)")
        print("\033[92m[3]\033[0m Deep Port Scan & Service Discovery")
        print("\033[92m[4]\033[0m Access Structural Storage (Reports)")
        print("\033[92m[5]\033[0m System Configuration")
        print("\033[91m[0]\033[0m Terminate Session")
        print("\n" + "\033[1;96m" + "═"*70 + "\033[0m")
        
        choice = input("\033[1;92m[#] CyberSentinel@2050:~\033[0m ")
        return choice

    def get_target(self):
        print("\n" + "\033[1;93m[?]\033[0m Enter Target Vector (Domain/URL): ", end="")
        target = input()
        return target

    def show_status(self, message, status_type="info"):
        symbols = {
            "info": "\033[1;94m[⚡]\033[0m",
            "success": "\033[1;92m[✔]\033[0m",
            "warning": "\033[1;93m[⚠️]\033[0m",
            "error": "\033[1;91m[✘]\033[0m"
        }
        print(f"{symbols.get(status_type, '[*]')} {message}")
