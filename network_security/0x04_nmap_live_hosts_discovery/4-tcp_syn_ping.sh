#!/bin/bash
sudo nmap $1 -PS 22,80,443 -sn
