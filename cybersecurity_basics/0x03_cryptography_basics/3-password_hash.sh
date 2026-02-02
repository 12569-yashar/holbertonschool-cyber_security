#!/bin/bash
echo -n "$(openssl rand -hex 8)$1" | openssl dgst -sha512 > 3_hash.txt
