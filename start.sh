gnome-terminal --title=Web_proxy -- /bin/bash -c "python3 -i src/web_proxy_launcher.py"
sleep 0.5
gnome-terminal --title=Client_proxy -- /bin/bash -c "python3 -i src/client_proxy_launcher.py"
