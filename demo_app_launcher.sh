cd /home/feilongbk/VENV3.8
virtualenv -p /usr/bin/python3.8 descartes_underwriting_technical_test
source descartes_underwriting_technical_test/bin/activate
sudo apt-get install python3-psycopg2
cd /home/feilongbk/Projects/descartes_underwriting_technical_test
pip3 install -r requirements.txt
python3.8 /home/feilongbk/Projects/descartes_underwriting_technical_test/application/demo_policy_user_interface/setup_demo_app.py
python3.8 /home/feilongbk/Projects/descartes_underwriting_technical_test/application/demo_policy_user_interface/application_dash.py