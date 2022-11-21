#! /bin/bash 
echo "Installing python-dev"
sudo apt install python-dev -y
echo "Installing python-pip"
sudo apt install python3-pip -y
sudo apt install git -y
sudo apt install ffmpeg -y
echo "cloning repository"
git clone https://github.com/ja-rivera94/cloud-convertion-tool.git
cd cloud-convertion-tool/worker/
pip install -r requirements.txt
export SENDGRID_API_KEY=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
set SENDGRID_API_KEY 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
python3 subscribe.py