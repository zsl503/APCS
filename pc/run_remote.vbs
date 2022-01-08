set ws=WScript.CreateObject("WScript.Shell")
ws.Run "cmd /k python C:\AutoStartPy\remote.py",0
ws.Run "cmd /k frp_0.37.1_windows_amd64\frpc -c frp_0.37.1_windows_amd64\frpc.ini",0