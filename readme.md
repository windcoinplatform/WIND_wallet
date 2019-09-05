Azure DevOps pipeline:

Linux build status: [![Build Status](https://dev.azure.com/BlackTurtleBVBA/TurtleNetwork/_apis/build/status/BlackTurtle123.PythonTNWallet?branchName=master)](https://dev.azure.com/BlackTurtleBVBA/TurtleNetwork/_build/latest?definitionId=3&branchName=master)

Windows build status: [![Build Status](https://dev.azure.com/BlackTurtleBVBA/TurtleNetwork/_apis/build/status/BlackTurtle123.PythonTNWallet.Windows?branchName=master)](https://dev.azure.com/BlackTurtleBVBA/TurtleNetwork/_build/latest?definitionId=6&branchName=master)

SonarCloud status: [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=T3&metric=alert_status)](https://sonarcloud.io/dashboard?id=T3)

To run tests:
pytest tests --doctest-modules --junitxml=junit/test-results.xml


To build the app:
pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" T3.py

Windows:
pip install --upgrade PyQt5==5.12.2

pyinstaller --onedir --add-data "templates;templates" --add-data "static;static" -i static/favicon.ico --hidden-import PyQt5 --path C:\Users\bramV\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\PyQt5\Qt\bin T3.py

