:: Create executable from python script
rmdir /S /Q last
mkdir last
move build last
move dist last
move *.spec last
move *.exe last

pyinstaller --onefile --add-data "images/*.png;images/" ecuapass_server.py

copy dist\*.exe .
