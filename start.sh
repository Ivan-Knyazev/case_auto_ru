#!/bin/bash

echo "Customization virtual environment..."
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
# echo "+ Virtual environment was activated!"

echo "Create DataBase..."
python3 init_db.py
# echo "DataBase was created! ..."

echo "Application start..."
python3 main.py
echo "-------------------------"
echo "Follow the 127.0.0.1:8000"