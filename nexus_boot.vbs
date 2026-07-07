Set WshShell = CreateObject("WScript.Shell")
strCommand = "cmd /c cd /d ""C:\Users\ashut\Enigm0"" && venv\Scripts\pythonw.exe api_server.py"
WshShell.Run strCommand, 0, False