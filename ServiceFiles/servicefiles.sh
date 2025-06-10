sudo cp aquarium_CO2.service /lib/systemd/system/    
sudo cp aquarium_OLED.service /lib/systemd/system/
sudo cp aquarium_lights.service /lib/systemd/system/
sudo cp aquarium_server.service /lib/systemd/system/
sudo cp aquarium_temperature.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aquarium_CO2.service
sudo systemctl enable aquarium_OLED.service
sudo systemctl enable aquarium_lights.service
sudo systemctl enable aquarium_server.service
sudo systemctl enable aquarium_temperature.service

sudo systemctl start aquarium_CO2.service
sudo systemctl start aquarium_OLED.service
sudo systemctl start aquarium_lights.service
sudo systemctl start aquarium_server.service
sudo systemctl start aquarium_temperature.service

