#!/bin/bash
echo "$1" | john --wordlist=/usr/share/worslists/rockyou.txt 4-password.txt
