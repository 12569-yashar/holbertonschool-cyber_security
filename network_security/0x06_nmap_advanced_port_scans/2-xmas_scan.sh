#!/bin/bash
sudo nmap $1 -sX --open --reason --packet-trace -p440,450
