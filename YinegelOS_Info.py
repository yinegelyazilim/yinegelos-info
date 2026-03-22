# Copyright (C) 2026 Abdullah Yiğit KARAKUŞ
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import customtkinter as ctk
import subprocess
import platform

# ------------------ yardımcı fonksiyon ------------------
def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except:
        return "Bilgi alınamadı"

# ------------------ OS bilgisi güvenli okuma ------------------
def get_os_info():
    try:
        output = subprocess.check_output(
            "cat /etc/os-release | grep PRETTY_NAME",
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        if '"' in output:
            return output.split('"', 1)[1].rsplit('"', 1)[0]
        else:
            return output.replace("PRETTY_NAME", "").strip()
    except:
        return "Bilinmiyor"

# ------------------ sistem bilgileri ------------------
os_info = get_os_info()
kernel_info = run_cmd("uname -r")
arch_info = run_cmd("uname -m")
hostname_info = run_cmd("hostname")
user_info = run_cmd("whoami")
uptime_info = run_cmd("uptime -p")

cpu_info = run_cmd(
    "grep 'model name' /proc/cpuinfo | head -n1 | cut -d: -f2"
).strip()

ram_info = run_cmd(
    "free -h | awk '/Mem:/ {print $2 \" toplam, \" $3 \" kullanılıyor\"}'"
)

disk_info = run_cmd(
    "df -h / | awk 'NR==2 {print $2 \" toplam, \" $3 \" kullanılıyor\"}'"
)

python_info = platform.python_version()

raw_de = run_cmd("echo $XDG_CURRENT_DESKTOP")
desktop_env = raw_de.split(":")[0] if raw_de else "Bilinmiyor"

# ------------------ bilgi metni ------------------
info_text = f"""Dağıtım: {os_info}
Kernel: {kernel_info}
Mimari: {arch_info}
Bilgisayar Adı: {hostname_info}
Kullanıcı: {user_info}
Masaüstü Ortamı: {desktop_env}
CPU: {cpu_info}
RAM: {ram_info}
Disk: {disk_info}
Çalışma Süresi: {uptime_info}
Python: {python_info}
Arayüz: CustomTkinter
"""

# ------------------ arayüz ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YinegelOS Hakkında")
app.geometry("600x540")
app.resizable(False, False)

# Başlık
ctk.CTkLabel(
    app, text="🐧 YinegelOS",
    font=ctk.CTkFont(size=32, weight="bold")
).pack(pady=(20, 5))

ctk.CTkLabel(
    app, text="Hakkında",
    font=ctk.CTkFont(size=18)
).pack(pady=(0, 15))

# Bilgi kutusu
frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(fill="both", expand=True, padx=20, pady=10)

textbox = ctk.CTkTextbox(
    frame,
    wrap="word",
    font=ctk.CTkFont(size=14)
)
textbox.pack(fill="both", expand=True, padx=15, pady=15)

textbox.insert("1.0", info_text)
textbox.configure(state="disabled")  # seçilebilir ama düzenlenemez

# Alt bilgi
ctk.CTkLabel(
    app,
    text="© 2026 YinegelOS Projesi",
    font=ctk.CTkFont(size=12),
    text_color="gray"
).pack(pady=(0, 12))

app.mainloop()
