sudo cp /home/feilongbk/Projects/descartes_underwriting_technical_test/demo_app_descartes.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl restart demo_app_descartes
sudo systemctl enable demo_app_descartes