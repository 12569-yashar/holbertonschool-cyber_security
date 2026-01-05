#!/bin/bash
sudo nmap $1 22,80,443 -PS -sn
