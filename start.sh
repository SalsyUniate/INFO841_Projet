gnome-terminal --title=Web_proxy -- /bin/bash -c "python3 -i web_proxy_launcher.py"
sleep 0.5
gnome-terminal --title=Client_proxy -- /bin/bash -c "python3 -i client_proxy_launcher.py"
