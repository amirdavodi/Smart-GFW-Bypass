#!/usr/bin/python3
import os
import subprocess
import uuid
import json
import random
import sys
import urllib.parse

# Function to print colored and Persian text
def print_status(text):
    print(f"\n\033[1;34m[+]\033[0m \033[1;32m{text}\033[0m")

def run_cmd(command):
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

def main():
    if os.geteuid() != 0:
        print("خطا: لطفاً اسکریپت را با sudo اجرا کنید.")
        sys.exit(1)

    os.system('clear')
    print("""
    ==============================================
       Ghost-Net v1.0 | Smart-GFW-Bypass
       طراحی شده برای عبور از فیلترینگ لایه ۷
    ==============================================
    """)

    # دریافت اطلاعات از کاربر
    admin_user = input("نام کاربری برای پنل مدیریت: ")
    admin_pass = input("رمز عبور برای پنل مدیریت: ")
    
    print_status("انتخاب پورت استراتژیک (غیرقابل مسدودسازی):")
    print("1. پورت 443 (استاندارد وب)")
    print("2. پورت 123 (NTP - حیاتی)")
    print("3. پورت 3478 (STUN - تماس تصویری)")
    p_choice = input("انتخاب (1-3): ")
    ports = {"1": "443", "2": "123", "3": "3478"}
    target_port = ports.get(p_choice, "443")

    # نصب پیش‌نیازها و هسته
    print_status("در حال نصب هسته Xray...")
    os.system('bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)"')

    # تولید پارامترهای Reality
    print_status("در حال تولید کلیدهای اختصاصی ضد‌شناسایی...")
    key_data = run_cmd("xray x25519")
    priv_key = key_data.splitlines()[0].split(": ")[1]
    pub_key = key_data.splitlines()[1].split(": ")[1]
    u_id = str(uuid.uuid4())
    s_id = os.urandom(4).hex()
    ip = run_cmd("curl -s ifconfig.me")

    # بهینه‌سازی شبکه BBR
    print_status("فعال‌سازی BBR برای پایداری در شبکه ایران...")
    os.system('echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf')
    os.system('echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf')
    os.system("sysctl -p")

    # نصب پنل Sanaei x-ui
    print_status("در حال نصب پنل x-ui...")
    os.system(f'bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh) <<EOF\ny\n{admin_user}\n{admin_pass}\n2053\nEOF')

    # ساخت لینک VLESS هوشمند
    tag = urllib.parse.quote(f"Ghost-Net-{ip}")
    vless_link = f"vless://{u_id}@{ip}:{target_port}?security=reality&encryption=none&pbk={pub_key}&headerType=none&fp=chrome&spx=%2F&type=tcp&sni=www.microsoft.com&sid={s_id}&flow=xtls-rprx-vision#{tag}"

    os.system('clear')
    print("==============================================")
    print("✅ نصب و پیکربندی با موفقیت انجام شد!")
    print(f"آدرس پنل شما: http://{ip}:2053")
    print(f"یوزر: {admin_user} | پسورد: {admin_pass}")
    print("----------------------------------------------")
    print("🚀 لینک اتصال مستقیم (در نرم‌افزار Paste کنید):")
    print(f"\n\033[1;33m{vless_link}\033[0m\n")
    print("----------------------------------------------")
    print("⚠️ نکته: حتماً در پنل یک Inbound با پروتکل VLESS و مشخصات بالا بسازید.")
    
    # پاکسازی ردپا
    os.system("history -c")

if __name__ == "__main__":
    main()
