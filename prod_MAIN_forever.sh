#!/bin/bash
pw-metadata -n settings 0 clock.force-quantum 4080
while true; do
    python prod_main.py
    # Wait for 15 seconds
    sleep 15
    echo ""
    echo ".:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:.:"
    echo ""

done
