#!/usr/bin/python3
"""
Script that finds a string in the heap of a running process
and replaces it with another string.
Usage: read_write_heap.py pid search_string replace_string
"""

import sys
import os


def find_heap_region(pid):
    """Find the heap memory region of a process from /proc/pid/maps."""
    maps_path = "/proc/{}/maps".format(pid)
    try:
        with open(maps_path, "r") as maps_file:
            for line in maps_file:
                if "[heap]" in line:
                    parts = line.split()
                    addr_range = parts[0].split("-")
                    heap_start = int(addr_range[0], 16)
                    heap_end = int(addr_range[1], 16)
                    return heap_start, heap_end
    except FileNotFoundError:
        print("Error: Cannot open {}. Is the PID correct?".format(maps_path))
        sys.exit(1)
    print("Error: No heap region found for PID {}.".format(pid))
    sys.exit(1)


def read_write_heap(pid, search_string, replace_string):
    """
    Read the heap of a process, find search_string,
    and replace it with replace_string.
    """
    heap_start, heap_end = find_heap_region(pid)
    heap_size = heap_end - heap_start

    mem_path = "/proc/{}/mem".format(pid)
    try:
        mem_file = open(mem_path, "rb+")
    except PermissionError:
        print("Error: Permission denied. Try running with sudo.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Cannot open {}. Is the PID correct?".format(mem_path))
        sys.exit(1)

    mem_file.seek(heap_start)
    heap_data = mem_file.read(heap_size)

    search_bytes = search_string.encode("ASCII")
    replace_bytes = replace_string.encode("ASCII")

    offset = heap_data.find(search_bytes)
    if offset == -1:
        print("Error: String '{}' not found in heap.".format(search_string))
        mem_file.close()
        sys.exit(1)

    found_addr = heap_start + offset

    if len(replace_bytes) > len(search_bytes):
        print("Error: replace_string is longer than search_string.")
        mem_file.close()
        sys.exit(1)

    replace_bytes_padded = replace_bytes + b'\x00' * (
        len(search_bytes) - len(replace_bytes))

    mem_file.seek(found_addr)
    mem_file.write(replace_bytes_padded)
    mem_file.close()

    print("SUCCESS!")


def main():
    """Main function - entry point of the script."""
    if len(sys.argv) != 4:
        print("Usage: {} pid search_string replace_string".format(sys.argv[0]))
        sys.exit(1)

    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("Error: pid must be an integer.")
        sys.exit(1)

    search_string = sys.argv[2]
    replace_string = sys.argv[3]

    if not search_string or not replace_string:
        print("Error: search_string and replace_string cannot be empty.")
        sys.exit(1)

    read_write_heap(pid, search_string, replace_string)


if __name__ == "__main__":
    main()
