import os
import subprocess
import uuid
import json
import random
import sys

def print_farsi(text):
    print(f"\n[+] {text}")

def run_command(command):
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

def setup():
    if os.geteuid() != 0:
        print("لطفاً اسکریپت را با دسترسی root (sudo) اجرا کنید.")
        sys.exit(1)

    os.system('clear')
    print("==============================================")
    print("   Ghost-Net v1.0: Advanced GFW Bypass      ")
    print("   طراحی شده برای عبور از فیلترینگ هوشمند   ")
    print("==============================================")

    # مرحله ۱: اطلاعات ورود
    admin_user = input("نام کاربری پنل مدیریت: ")
    admin_pass = input("رمز عبور پنل مدیریت: ")
    
    # مرحله ۲: انتخاب پورت استراتژیک
    print_farsi("انتخاب پورت غیرقابل مسدودسازی (Stealth Port):")
    print("1. پورت 443 (استاندارد HTTPS - پیشنهاد اول)")
    print("2. پورت 123 (NTP - حیاتی)")
    print("3. پورت 3478 (STUN - ویدیو کنفرانس)")
    port_choice = input("گزینه (1-3): ")
    ports = {"1": "443", "2": "123", "3": "3478"}
    final_port = ports.get(port_choice, "443")

    # مرحله ۳: نصب هسته Xray (برای تولید کلیدها الزامی است)
    print_farsi("در حال نصب هسته Xray...")
    os.system('bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)"')

    # مرحله ۴: تولید پارامترهای Reality
    print_farsi("در حال تولید کلیدهای اختصاصی ضد‌شناسایی...")
    key_output = run_command("xray x25519")
    priv_key = key_output.splitlines()[0].split(": ")[1]
    pub_key = key_output.splitlines()[1].split(": ")[1]
    u_id = str(uuid.uuid4())
    short_id = os.urandom(4).hex()
    server_ip = run_command("curl -s ifconfig.me")

    # مرحله ۵: بهینه‌سازی TCP BBR
    print_farsi("بهینه‌سازی شبکه (BBR)...")
    with open("/etc/sysctl.conf", "a") as f:
        f.write("\nnet.core.default_qdisc=fq\nnet.ipv4.tcp_congestion_control=bbr\n")
    os.system("sysctl -p")

    # مرحله ۶: نصب پنل x-ui (نسخه Sanaei)
    print_farsi("در حال نصب پنل مدیریت...")
    # نصب با تنظیمات خودکار یوزر و پسورد
    os.system(f'bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh) <<EOF\ny\n{admin_user}\n{admin_pass}\n2053\nEOF')

    os.system('clear')
    print("==============================================")
    print("✅ تبریک! سیستم با موفقیت راه‌اندازی شد.")
    print("==============================================")
    print(f"آدرس پنل: http://{server_ip}:2053")
    print(f"یوزر: {admin_user} | پسورد: {admin_pass}")
    print("\n🚀 اطلاعات لازم برای ساخت Inbound در پنل:")
    print(f"- پروتکل: vless")
    print(f"- پورت: {final_port}")
    print(f"- آی‌دی (UUID): {u_id}")
    print(f"- جریان (Flow): xtls-rprx-vision")
    print(f"- شبکه: tcp")
    print(f"- امنیت: reality")
    print(f"- (uTLS) اثرانگشت: chrome یا safari")
    print(f"- Dest/SNI: www.microsoft.com:443 / www.microsoft.com")
    print(f"- Private Key: {priv_key}")
    print(f"- Public Key: {pub_key}")
    print(f"- Short ID: {short_id}")
    print("==============================================")

if __name__ == "__main__":
    setup()
