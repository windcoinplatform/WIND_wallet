To build the app:
 pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" TurtleNetwork.py

Windows:
pip install --upgrade PyQt5==5.12.2

pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" --hidden-import PyQt5 --path C:\Users\bramV\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\bin TurtleNetwork.py

