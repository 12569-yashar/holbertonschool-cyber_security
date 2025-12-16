#!/bin/bash
password=$(head -c "$1" /dev/urandom | tr -cd '[:alnum:][:punct:]')
echo -n "$password"
