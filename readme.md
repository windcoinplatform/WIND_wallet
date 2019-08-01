To build the app:
pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" T3.py

Windows:
pip install --upgrade PyQt5==5.12.2

pyinstaller -F --add-data "templates;templates" --add-data "static;static" -i static/favicon.ico --hidden-import PyQt5 --path C:\Users\bramV\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\bin TurtleNetwork.py

