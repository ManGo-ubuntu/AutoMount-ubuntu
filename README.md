# AutoMount Ubuntu

Программа для автоматического монтирования дисков в Ubuntu с графическим интерфейсом.

## Возможности

- Отображение списка доступных дисков
- Выбор дисков для автоматического монтирования
- Автоматическое создание точек монтирования
- Настройка автомонтирования через /etc/fstab
- Простой и понятный интерфейс
- Интеграция с меню приложений Ubuntu

## Установка

1. Скачайте все файлы в одну директорию
2. Откройте терминал в этой директории
3. Сделайте установочный скрипт исполняемым:
```bash
chmod +x install.sh
```

4. Запустите установку:
```bash
./install.sh
```

## Использование

1. Найдите "AutoMount Ubuntu" в меню приложений Ubuntu (или нажмите Super и начните вводить "AutoMount")
2. Запустите программу (при запуске потребуются права администратора)
3. В открывшемся окне вы увидите список доступных дисков
4. Отметьте галочками диски, которые хотите автоматически монтировать
5. Нажмите "Сохранить настройки"
6. Перезагрузите компьютер для применения настроек

## Примечания

- Программа создает резервную копию файла /etc/fstab перед внесением изменений
- Точки монтирования создаются в директории /media/automount*
- Программа использует PolicyKit для получения прав администратора
- Все файлы программы устанавливаются в /opt/automount-ubuntu 