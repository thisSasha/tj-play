import requests
import os
import shutil
import sys
from PySide6.QtWidgets import QApplication, QFileDialog

def select_folder():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    
    if dialog.exec():
        selected = dialog.selectedFiles()
        return selected[0] if selected else None
    return None

def get_path(to='игры'):
    path = 'None'
    if os.path.exists('.path'):
        path = open('.path', 'r', encoding='utf-8').read()
    else:
        print(f'Поиск каталога {to}...')
        while True:
            if not os.path.exists(path):
                print('Каталог не найден')
                print(f'Выберите путь к папке {to}')
                path = select_folder()
                open('.path', 'w', encoding='utf-8').write(path)
            else:
                break

    return path

def update_client():
    gamepath = get_path('игры')
    modpath = os.path.join(gamepath, 'mods')
    if not os.path.exists(modpath):
        os.makedirs(modpath)
    
    isResoursePacks = input('Хотели бы вы получить все рекомендуемые ресурс паки? (y/n): ')
    if isResoursePacks == 'y':
        print('Получение пакетов ресурсов...')
        respath = os.path.join(gamepath, 'resourcepacks')
        if not os.path.exists(respath):
            os.makedirs(respath)
        
        file = requests.get('https://raw.githubusercontent.com/thisSasha/tj-play/master/client/resourcepacks/.filelist').text

        for line in file:
            line = line.strip() 
            if line:
                print(line)
                print(f'{line} -> {os.path.join(respath, line)}')   
                shutil.copy(os.path.join(respath, line), os.path.join(respath, line))

    print('Получение модов...')
    
    file = requests.get('https://raw.githubusercontent.com/thisSasha/tj-play/master/client/mods/.filelist').text
    for line in file:
        line = line.strip() 
        if line:    
            print(f'{line} -> {os.path.join(modpath, line)}')   
            shutil.copy(os.path.join(modpath, line), os.path.join(modpath, line))
    
    isOptions = input('Хотели бы вы получить все рекомендуемые настройки? (y/n): ')
    if isOptions == 'y':
        print('Получение настроек...')
        optionspath = os.path.join(gamepath, 'options.txt')
        if not os.path.exists(optionspath):
            os.makedirs(optionspath)
        
        file = requests.get('https://raw.githubusercontent.com/thisSasha/tj-play/master/client/options.txt').text
        with open(optionspath, 'w', encoding='utf-8') as file:
            file.write(file)
    
    print('Обновление завершено')
    print('Приятной игры!')




print('Получение последней версии...')
VERSION = open("VERSION", "r", encoding="utf-8").read()
LAST_VERSION = requests.get(f'https://raw.githubusercontent.com/thisSasha/tj-play/master/VERSION').text
print(f'{VERSION} {"->" if VERSION != LAST_VERSION else "="} {LAST_VERSION}')

if VERSION == LAST_VERSION:
    print('Версия актуальна')
    exit()

print('Обновление...')
update_client()
