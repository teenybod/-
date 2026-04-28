Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

cmd = "cmd /c cd /d " & Chr(34) & scriptDir & Chr(34) & " && venv\Scripts\python app.py"
WshShell.Run cmd, 0, False

Set fso = Nothing
Set WshShell = Nothing
