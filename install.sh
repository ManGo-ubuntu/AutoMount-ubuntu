#!/bin/bash

# Создаем директории для установки
sudo mkdir -p /opt/automount-ubuntu
sudo mkdir -p /usr/share/applications
sudo mkdir -p /usr/share/icons/hicolor/256x256/apps

# Копируем файлы программы
sudo cp automount.py /opt/automount-ubuntu/
sudo cp requirements.txt /opt/automount-ubuntu/
sudo cp icon.png /usr/share/icons/hicolor/256x256/apps/automount-ubuntu.png

# Устанавливаем зависимости
sudo apt-get update
sudo apt-get install -y python3-pip python3-pyqt6
sudo pip3 install -r requirements.txt

# Создаем desktop файл
cat << EOF | sudo tee /usr/share/applications/automount-ubuntu.desktop
[Desktop Entry]
Version=1.0
Name=AutoMount Ubuntu
Comment=Автоматическое монтирование дисков
Exec=pkexec /opt/automount-ubuntu/automount.py
Icon=automount-ubuntu
Terminal=false
Type=Application
Categories=System;Settings;
Keywords=disk;mount;automount;
EOF

# Создаем polkit файл для запуска с правами root
cat << EOF | sudo tee /usr/share/polkit-1/actions/com.automount.ubuntu.policy
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
<policyconfig>
  <action id="com.automount.ubuntu.run">
    <description>Run AutoMount Ubuntu</description>
    <message>Authentication is required to run AutoMount Ubuntu</message>
    <defaults>
      <allow_any>auth_admin</allow_any>
      <allow_inactive>auth_admin</allow_inactive>
      <allow_active>auth_admin</allow_active>
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/opt/automount-ubuntu/automount.py</annotate>
  </action>
</policyconfig>
EOF

# Делаем файлы исполняемыми
sudo chmod +x /opt/automount-ubuntu/automount.py

# Обновляем кэш иконок
sudo gtk-update-icon-cache /usr/share/icons/hicolor/

echo "Установка завершена. Теперь вы можете найти AutoMount Ubuntu в меню приложений." 