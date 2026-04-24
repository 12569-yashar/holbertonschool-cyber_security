#!/bin/bash
nmap -sV --script nmap-vulners/ $1 -p80,443
