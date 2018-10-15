Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\xampp\htdocs\flask_app\Calandria\servidor.bat" & Chr(34), 0
Set WshShell = Nothing