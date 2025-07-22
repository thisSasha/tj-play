import requests
import os
import shutil
import sys
from PySide6.QtWidgets import QApplication, QFileDialog

GITHUB_BASE = 'https://raw.githubusercontent.com/thisSasha/tj-play/master/client/'

def select_folder():
    app = QApplication(sys.argv)
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

def download_file(url, dest_path):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'{url} -> {dest_path}')
    except Exception as e:
        print(f'Ошибка загрузки {url}: {e}')

def update_client():
    gamepath = get_path('игры')
    modpath = os.path.join(gamepath, 'mods')
    if not os.path.exists(modpath):
        os.makedirs(modpath)

    # Resourcepacks
    isResoursePacks = input('Получить все рекомендуемые ресурс паки? (y/n): ')
    if isResoursePacks.lower() == 'y':
        print('Получение пакетов ресурсов...')
        respath = os.path.join(gamepath, 'resourcepacks')
        if not os.path.exists(respath):
            os.makedirs(respath)
        
        filelist_url = GITHUB_BASE + 'resourcepacks/.filelist'
        lines = requests.get(filelist_url).text.splitlines()
        
        for line in lines:
            line = line.strip()
            if line:
                url = GITHUB_BASE + f'resourcepacks/{line}'
                dest = os.path.join(respath, line)
                download_file(url, dest)

    print('Получение модов...')
    modlist_url = GITHUB_BASE + 'mods/.filelist'
    lines = requests.get(modlist_url).text.splitlines()
    expected_files = []

    for line in lines:
        line = line.strip()
        if line:
            expected_files.append(line)
            url = GITHUB_BASE + f'mods/{line}'
            dest = os.path.join(modpath, line)
            download_file(url, dest)

    # Удаляем лишние моды
    for filename in os.listdir(modpath):
        if filename not in expected_files:
            os.remove(os.path.join(modpath, filename))
            print(f'Удалён лишний мод: {filename}')

    # Options
    isOptions = input('Установить рекомендуемые настройки? (y/n): ')
    if isOptions.lower() == 'y':
        print('Получение настроек...')
        options_url = GITHUB_BASE + 'options.txt'
        optionspath = os.path.join(gamepath, 'options.txt')
        try:
            content = requests.get(options_url).text
            with open(optionspath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Настройки сохранены в {optionspath}')
        except Exception as e:
            print(f'Ошибка загрузки настроек: {e}')

    print('Обновление завершено')
    print('Приятной игры!')


print('Получение последней версии...')
if not os.path.exists("VERSION"):
    open('VERSION', 'w').write('-1')

VERSION = open("VERSION", "r", encoding="utf-8").read().strip()
LAST_VERSION = requests.get(f'https://raw.githubusercontent.com/thisSasha/tj-play/master/VERSION').text.strip()

print(f'{VERSION} {"->" if VERSION != LAST_VERSION else "="} {LAST_VERSION}')

if VERSION == LAST_VERSION:
    print('Версия актуальна')
    exit()

print('Обновление...')
update_client()
open('VERSION', 'w').write(LAST_VERSION)
