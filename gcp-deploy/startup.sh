#! /bin/bash 
echo "Updating system"
sudo apt update
sudo apt upgrade -y
echo "Installing python-dev"
sudo apt install python-dev -y
echo "Installing python-pip"
sudo apt install python3-pip -y
sudo apt install git -y
echo "cloning repository"
git clone https://github.com/ja-rivera94/cloud-convertion-tool.git
cd cloud-convertion-tool/api_rest/
pip install -r requirements.txt
python3 app.py