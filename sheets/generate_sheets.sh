##!/bin/bash

python scripts/prerequisites.py

echo "Generating Sheet1"
python scripts/sheet1Main.py

echo "Generating Sheet2"
python scripts/sheet2Main.py

echo "Generating Sheet4"
python scripts/sheet3Main.py

echo "Generating Sheet4"
python scripts/sheet4Main.py

echo "Generating Sheet5"
python scripts/sheet5Main.py

echo "Generating Sheet6"
python scripts/sheet6Main.py
