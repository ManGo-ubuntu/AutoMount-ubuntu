#!/usr/bin/env python3
import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QListWidget,
                            QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
import psutil
import pyudev

class AutoMountApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoMount Ubuntu")
        self.setMinimumSize(600, 400)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title = QLabel("Выберите диски для автомонтирования")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Список дисков
        self.disk_list = QListWidget()
        layout.addWidget(self.disk_list)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Обновить список")
        self.refresh_button.clicked.connect(self.refresh_disks)
        self.save_button = QPushButton("Сохранить настройки")
        self.save_button.clicked.connect(self.save_settings)
        
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)
        
        # Инициализация списка дисков
        self.refresh_disks()
    
    def refresh_disks(self):
        self.disk_list.clear()
        partitions = psutil.disk_partitions(all=True)
        context = pyudev.Context()
        
        for partition in partitions:
            if partition.device.startswith('/dev/'):
                device = pyudev.Device.from_device_file(context, partition.device)
                if device.get('ID_TYPE') == 'disk' or device.get('ID_FS_TYPE'):
                    item_text = f"{partition.device} - {partition.mountpoint or 'Не примонтирован'}"
                    if partition.fstype:
                        item_text += f" ({partition.fstype})"
                    
                    item = QCheckBox(item_text)
                    item.setChecked(self.is_in_fstab(partition.device))
                    
                    list_item = self.disk_list.addItem("")
                    self.disk_list.setItemWidget(self.disk_list.item(
                        self.disk_list.count() - 1), item)
    
    def is_in_fstab(self, device):
        try:
            with open('/etc/fstab', 'r') as f:
                return any(device in line for line in f.readlines())
        except:
            return False
    
    def save_settings(self):
        selected_devices = []
        for i in range(self.disk_list.count()):
            item = self.disk_list.item(i)
            checkbox = self.disk_list.itemWidget(item)
            if checkbox.isChecked():
                device = checkbox.text().split(' - ')[0]
                selected_devices.append(device)
        
        try:
            # Создаем резервную копию fstab
            subprocess.run(['sudo', 'cp', '/etc/fstab', '/etc/fstab.backup'])
            
            # Добавляем выбранные устройства в fstab
            for device in selected_devices:
                mount_point = f"/media/automount{len(selected_devices)}"
                subprocess.run(['sudo', 'mkdir', '-p', mount_point])
                fstab_line = f"{device} {mount_point} auto nosuid,nodev,nofail,x-gvfs-show,user 0 0"
                with open('/tmp/fstab_entry', 'w') as f:
                    f.write(fstab_line + '\n')
                subprocess.run(['sudo', 'bash', '-c', 'cat /tmp/fstab_entry >> /etc/fstab'])
            
            QMessageBox.information(self, "Успех", 
                                  "Настройки автомонтирования успешно сохранены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", 
                               f"Произошла ошибка при сохранении настроек: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoMountApp()
    window.show()
    sys.exit(app.exec()) 