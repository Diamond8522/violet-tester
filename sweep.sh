#!/bin/bash
echo "🟣 [VIOLET-SWEEP]: Initiating laboratory-wide audit..."
echo "----------------------------------------------------"

for file in payloads/*; do
    if [ -f "$file" ]; then
        python3 scrub.py "$file"
        echo "----------------------------------------------------"
    fi
done

echo "🏁 Audit Complete."
