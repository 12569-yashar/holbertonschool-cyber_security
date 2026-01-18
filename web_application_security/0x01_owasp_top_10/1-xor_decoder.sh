#!/bin/bash
input=$(echo "$1" | sed 's/{xor}//')
echo "$input" | base64 -d | perl -pe '$_ ^= "_" x length'
