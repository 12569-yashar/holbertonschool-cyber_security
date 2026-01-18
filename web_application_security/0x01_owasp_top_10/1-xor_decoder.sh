#!/bin/bash

password="$1"

password="${password#'{xor}'}"

decoded_password=$(echo -n "$password" | openssl enc -base64 -d)

output=""

for ((i = 0; i < ${#decoded_password}; i++)); do
    # Récupère le caractère à la position actuelle
    char="${decoded_password:$i:1}"
    # Convertit le caractère en son code ASCII et effectue l'opération XOR avec 95
    xor_result=$(( $(printf "%d" "'$char") ^ 95 ))
    # Ajoute le résultat à la variable de sortie
    output+=$(printf "\\$(printf '%03o' $xor_result)")
done

echo "$output"
