import requests
import os
import zipfile
import io
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

GITHUB_BASE = 'https://raw.githubusercontent.com/thisSasha/tj-play/main/'  # поправьте на свой URL

def update_client():
    gamepath = get_path('игры')
    # Папки mods и resourcepacks
    modpath = os.path.join(gamepath, 'mods')
    respath = os.path.join(gamepath, 'resourcepacks')
    os.makedirs(modpath, exist_ok=True)
    os.makedirs(respath, exist_ok=True)

    # Скачиваем и распаковываем mods.zip
    print('Получение архива модов...')
    mods_zip_url = GITHUB_BASE + 'mods.zip'
    resp = requests.get(mods_zip_url, stream=True)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        print(f'Распаковка модов в {modpath}...')
        z.extractall(path=modpath)

    # Ресурспаки по выбору
    isResoursePacks = input('Получить все рекомендуемые ресурс паки? (y/n): ')
    if isResoursePacks.strip().lower() == 'y':
        print('Получение архива ресурс-паков...')
        res_zip_url = GITHUB_BASE + 'resourcepacks.zip'
        resp = requests.get(res_zip_url, stream=True)
        resp.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            print(f'Распаковка ресурс-паков в {respath}...')
            z.extractall(path=respath)

    # Настройки по выбору
    isOptions = input('Установить рекомендуемые настройки? (y/n): ')
    if isOptions.strip().lower() == 'y':
        print('Получение options.txt...')
        options_url = GITHUB_BASE + 'options.txt'
        optionspath = os.path.join(gamepath, 'options.txt')
        try:
            content = requests.get(options_url).text
            with open(optionspath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Настройки сохранены в {optionspath}')
        except Exception as e:
            print(f'Ошибка загрузки настроек: {e}')

    print('Обновление завершено.')
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
