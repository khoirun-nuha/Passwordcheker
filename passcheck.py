import curses
import re
import secrets
import string
import os
from datetime import datetime
from cryptography.fernet import Fernet

# ================== LOGIC ==================
def check_password(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[!@#$%^&*()]", password): score += 1
    return score

def strength_label(score):
    return ["SANGAT LEMAH","SANGAT LEMAH", "LEMAH","SEDANG","KUAT","SANGAT KUAT"][score]

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(chars) for _ in range(16))

def save_generated_password(pwd):
    with open("generated_passwords.txt", "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {pwd}\n")

# --- BARU: Fungsi untuk menyimpan hasil enkripsi ---
def save_encrypted_password(token):
    with open("password_enkripsi.txt", "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{ts}] {token}\n")
# ---------------------------------------------------

def load_key():
    if not os.path.exists("secret.key"):
        with open("secret.key", "wb") as f:
            f.write(Fernet.generate_key())
    return open("secret.key", "rb").read()

def encrypt_pwd(pwd):
    return Fernet(load_key()).encrypt(pwd.encode()).decode()

def decrypt_pwd(token):
    return Fernet(load_key()).decrypt(token.encode()).decode()

# ================== ASCII ART ==================
PASSCHECK_ART = [
"██████╗  █████╗ ███████╗███████╗ ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗",
"██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝",
"██████╔╝███████║███████╗███████╗██║     ███████║█████╗  ██║     █████╔╝ ",
"██╔═══╝ ██╔══██║╚════██║╚════██║██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ",
"██║     ██║  ██║███████║███████║╚██████╗██║  ██║███████╗╚██████╗██║  ██╗",
"╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝",
]

BY_NUH4_ART = [
"██████╗ ██╗   ██╗    ███╗   ██╗██╗   ██╗██╗  ██╗ ██╗  ██╗",
"██╔══██╗╚██╗ ██╔╝    ████╗  ██║██║   ██║██║  ██║ ██║  ██║",
"██████╔╝ ╚████╔╝     ██╔██╗ ██║██║   ██║███████║ ███████║",
"██╔══██╗  ╚██╔╝      ██║╚██╗██║██║   ██║██╔══██║      ██║",
"██████╔╝   ██║       ██║ ╚████║╚██████╔╝██║  ██║      ██║",
"╚═════╝    ╚═╝       ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝      ╚═╝",
]

SUBTITLE = "PASSWORD SECURITY TOOL"

# ================== COLORS ==================
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

# ================== UI ==================
def draw_header(stdscr):
    h, w = stdscr.getmaxyx()
    TOP = 2

    for i, line in enumerate(PASSCHECK_ART):
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(i + TOP, 4, line)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    base_x = 4 + len(PASSCHECK_ART[0]) + 3
    for i, line in enumerate(BY_NUH4_ART):
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(i + TOP, base_x, line)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    sub_y = TOP + len(PASSCHECK_ART) + 1
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(sub_y, 4, SUBTITLE)
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    stdscr.addstr(sub_y + 1, 0, "=" * (w - 1), curses.color_pair(4))
    stdscr.attron(curses.color_pair(5) | curses.A_DIM)
    stdscr.addstr(h - 2, w - 18, "© Khoirun Nuha")
    stdscr.attroff(curses.color_pair(5) | curses.A_DIM)

    return sub_y + 1

def draw_menu(stdscr, start_y):
    menu = [
        "1. Cek Password",
        "2. Generate Password",
        "3. Enkripsi Password",
        "4. Dekripsi Password",
        "5. Keluar"
    ]
    y = start_y + 2
    for i, item in enumerate(menu):
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(y + i * 2, 4, item)
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)

    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(y + len(menu) * 2 + 1, 4, "Pilih menu: ")
    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
    return y + len(menu) * 2 + 1

def inline_input(stdscr, y, x, prompt, maxlen=200):
    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(y, x, prompt)
    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
    stdscr.move(y, x + len(prompt))
    curses.echo()
    val = stdscr.getstr(y, x + len(prompt), maxlen).decode()
    curses.noecho()
    return val

def log_line(stdscr, y, x, text, color=5):
    stdscr.attron(curses.color_pair(color))
    stdscr.addstr(y, x, text)
    stdscr.attroff(curses.color_pair(color))

def clear_log_area(stdscr, start_y):
    h, _ = stdscr.getmaxyx()
    for y in range(start_y, h - 3):
        stdscr.move(y, 0)
        stdscr.clrtoeol()

# ================== MAIN ==================
def main(stdscr):
    curses.curs_set(1)
    init_colors()

    stdscr.clear()
    header_end = draw_header(stdscr)
    menu_y = draw_menu(stdscr, header_end)

    base_x = 4
    log_start_y = menu_y + 2
    log_y = log_start_y

    while True:
        curses.echo()
        stdscr.attron(curses.A_BOLD)
        choice = stdscr.getstr(menu_y, 16, 1).decode()
        stdscr.attroff(curses.A_BOLD)
        curses.noecho()

        clear_log_area(stdscr, log_start_y)
        log_y = log_start_y

        if choice == "1":
            pwd = inline_input(stdscr, log_y, base_x, "Masukkan password: ")
            log_y += 1
            log_line(stdscr, log_y, base_x, "[*] Checking password...", 4)
            log_y += 1
            score = check_password(pwd)
            color = 2 if score <= 2 else 3 if score == 3 else 1
            log_line(stdscr, log_y, base_x, f"[+] Skor   : {score}/5", color)
            log_y += 1
            log_line(stdscr, log_y, base_x, f"[+] Status : {strength_label(score)}", color)
            log_y += 2

        elif choice == "2":
            log_line(stdscr, log_y, base_x, "[*] Generating password...", 4)
            log_y += 1
            pwd = generate_password()
            save_generated_password(pwd)
            log_line(stdscr, log_y, base_x, f"[+] Password : {pwd}", 1)
            log_y += 1
            log_line(stdscr, log_y, base_x, "[+] Saved to generated_passwords.txt", 3)
            log_y += 2

        elif choice == "3":
            pwd = inline_input(stdscr, log_y, base_x, "Password untuk dienkripsi: ")
            log_y += 1
            log_line(stdscr, log_y, base_x, "[*] Encrypting...", 4)
            log_y += 1
            
            # --- UPDATE LOGIKA ENKRIPSI DISINI ---
            encrypted_token = encrypt_pwd(pwd)
            save_encrypted_password(encrypted_token) # Simpan ke file
            
            log_line(stdscr, log_y, base_x, f"[+] Encrypted: {encrypted_token}", 1)
            log_y += 1
            log_line(stdscr, log_y, base_x, "[+] Saved to password_enkripsi.txt", 3)
            log_y += 2

        elif choice == "4":
            token = inline_input(stdscr, log_y, base_x, "Masukkan encrypted password: ")
            log_y += 1
            log_line(stdscr, log_y, base_x, "[*] Decrypting...", 4)
            log_y += 1
            try:
                log_line(stdscr, log_y, base_x, f"[+] Decrypted: {decrypt_pwd(token)}", 1)
            except:
                log_line(stdscr, log_y, base_x, "[!] GAGAL DEKRIPSI!", 2)
            log_y += 2

        elif choice == "5":
            break

        stdscr.refresh()

curses.wrapper(main)
