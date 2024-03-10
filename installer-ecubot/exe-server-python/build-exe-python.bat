:: Create executable from python script
rmdir /S /Q last
mkdir last
move build last
move dist last
move *.spec last
move *.exe last

pyinstaller --onefile --add-data "images/*.png;images/" --add-data "ecuapassdocs/resources/data-cartaportes/*.txt";"ecuapassdocs/resources/data-cartaportes/" --add-data "ecuapassdocs/resources/data-manifiestos/*.txt";"ecuapassdocs/resources/data-manifiestos/" --add-data "ecuapassdocs/resources/docs/*.png";"ecuapassdocs/resources/docs/" --add-data "ecuapassdocs/resources/docs/*.pdf";"ecuapassdocs/resources/docs/" --add-data "ecuapassdocs/resources/docs/*.json";"ecuapassdocs/resources/docs/" ecuapass_server.py

copy dist\*.exe .
