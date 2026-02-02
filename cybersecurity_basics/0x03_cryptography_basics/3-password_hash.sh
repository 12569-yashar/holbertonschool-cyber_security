#!/bin/bash
salt=$(openssl rand -hex 8)
echo -n "${salt}$1" | openssl dgst -sha512 > 3_hash.txt
