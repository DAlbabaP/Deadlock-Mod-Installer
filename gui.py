import os
import json
import locale
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from installer import Installer
from config import MODS, MEDIA_DIR
from translations import get_translation
from descriptions import get_mod_description
import sys
import codecs

VERSION = "1.0.0"

def get_resource_path(relative_path):
    """ Получить абсолютный путь к ресурсу """
    if getattr(sys, 'frozen', False):
        # Если запущено через PyInstaller
        base_path = sys._MEIPASS
        print(f"Running from PyInstaller bundle. Base path: {base_path}")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Running from source. Base path: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"Full resource path: {full_path}")
    return full_path

class ModInstallerGUI:
    def __init__(self, root):
        self.root = root
        
        # Настройка цветов и стилей
        self.colors = {
            'bg': '#231f20',  # Основной фон
            'text': '#ffffff',  # Белый текст
            'button': '#f0dfbf',  # Цвет для кнопок
            'warning': '#dc3545',  # Красный для кнопки удаления
            'dark_bg': '#1a1617',  # Темный фон для блоков скинов
            'darker_bg': '#141112',  # Еще более темный фон для блоков героев
        }
        
        # Настройка стиля
        style = ttk.Style()
        style.theme_use('clam')  # или 'alt', 'default', 'classic'
        
        # Конфигурация стилей кнопок
        style.configure('TButton', 
                       padding=6, 
                       relief="flat",
                       background=self.colors['button'],
                       foreground="black")
        
        style.map('TButton',
                 background=[('active', '#d9c9ac')],
                 foreground=[('active', 'black')])
        
        # Стиль для поля ввода
        style.configure('TEntry',
                       fieldbackground="white",
                       foreground="black")
        
        # Стиль для метки пути
        style.configure('Path.TLabel',
                       background=self.colors['bg'],
                       foreground="white")
        
        # Загружаем сохраненный язык или определяем по системе
        try:
            config_path = get_resource_path("config.json")
            if os.path.exists(config_path):
                with codecs.open(config_path, 'r', 'utf-8') as f:
                    config = json.load(f)
                    self.lang = config.get('language', 'en')
            else:
                current_locale = locale.getdefaultlocale()[0]
                self.lang = 'ru' if current_locale and 'ru' in current_locale.lower() else 'en'
        except:
            self.lang = 'en'
        
        # Загружаем переводы
        self.t = get_translation(self.lang)
        print(f"Loaded translations. english_names = {self.t.get('english_names')}")
        print(f"All translations: {self.t}")
        
        # Устанавливаем заголовок окна
        self.root.title(self.t['window_title'])
        
        # Устанавливаем окно на весь экран
        self.root.state('zoomed')
        
        # Настройка шрифтов
        self.fonts = {
            'default': ('Segoe UI', 11),  # Основной шрифт
            'header': ('Segoe UI Semibold', 12),  # Шрифт для заголовков
            'title': ('Segoe UI Semibold', 30),  # Большой заголовок
            'warning': ('Segoe UI', 10, 'bold')  # Жирный шрифт для предупреждений
        }
        
        # Создаем переменные
        self.install_path = tk.StringVar()
        self.selected_mods = {
            'About': {},  # Добавляем категорию About первой
            'Interface': {},
            'Game': {},
            'Sounds': {},
            'Post-processing': {},
            'Skins': {},
            'Other': {}
        }
        
        # Добавляем функции для локализации
        self.original_loc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'original_localization')
        self.new_loc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new_localization')
        
        # Путь к локальной директории с модами
        self.local_mods_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mods")
        if not os.path.exists(self.local_mods_dir):
            self.local_mods_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mods")
        
        # Основные стили
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('Skins.TFrame', background=self.colors['dark_bg'])
        style.configure('Character.TFrame', background=self.colors['darker_bg'])
        
        # Стиль для вкладок
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', 
            background=self.colors['bg'],
            foreground=self.colors['text'],
            padding=[10, 5]
        )
        
        # Стиль для активной вкладки
        style.map('TNotebook.Tab',
            background=[('selected', self.colors['dark_bg'])],
            foreground=[('selected', self.colors['text'])]
        )
        
        # Стиль для радиокнопок в категории скинов
        style.configure('Skins.TRadiobutton', 
            background=self.colors['darker_bg'],
            foreground=self.colors['text']
        )
        style.map('Skins.TRadiobutton',
            background=[('active', self.colors['darker_bg']),
                       ('selected', self.colors['darker_bg'])]
        )
        
        # Стиль для меток
        style.configure('TLabel',
            background=self.colors['bg'],
            foreground=self.colors['text']
        )
        
        # Стиль для кнопок
        style.configure('TButton',
            background=self.colors['button'],
            foreground="black"
        )
        
        # Стиль для кнопки установки
        style.configure('Accent.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для кнопки удаления
        style.configure('Warning.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для кнопок языка
        style.configure('Lang.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       padding=3,
                       width=3,
                       font=self.fonts['default'])
                       
        # Стиль для чекбоксов
        style.configure('TCheckbutton',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
                       
        # Стиль для полей ввода
        style.configure('TEntry',
                       background="white",
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для комбобоксов
        style.configure('TCombobox',
                       background=self.colors['button'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['button'],
                       font=self.fonts['default'])
                       
        # Настройка вкладок
        style.configure('TNotebook.Tab',
                       background=self.colors['button'],
                       foreground=self.colors['text'],
                       padding=[10, 2],
                       font=self.fonts['default'])
                       
        # Настройка выбранной вкладки
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['button'])],
                 foreground=[('selected', self.colors['text'])])
        
        # Стиль для заголовков
        style.configure('Header.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['header'])
        
        # Стиль для предупреждений
        style.configure('Warning.TLabel',
                       background=self.colors['bg'],
                       foreground='red',
                       font=self.fonts['warning'])
        
        # Стиль для блоков скинов
        style.configure('Skin.TFrame',
                       background=self.colors['dark_bg'])
        
        # Стиль для меток в блоке скинов
        style.configure('Skin.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
        
        # Стиль для радиокнопок в блоке скинов
        style.configure('Skin.TRadiobutton',
                       foreground=self.colors['text'],
                       background=self.colors['dark_bg'],
                       font=self.fonts['default'])
                       
        # Стиль для информационного фрейма и его компонентов
        style.configure('Info.TFrame', background=self.colors['dark_bg'])
        style.configure('Title.TFrame', background=self.colors['dark_bg'])
        style.configure('Title.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['title'])
        style.configure('Info.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
        
        # Настройка цветов корневого окна
        self.root.configure(bg=self.colors['bg'])
        
        # Создаем стиль для информационного блока
        style.configure('Info.TFrame', background=self.colors['bg'], borderwidth=1, relief='solid')
        style.configure('Info.TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        
        # Конфигурация стилей вкладок
        style.configure('TNotebook.Tab',
                       padding=[10, 2],
                       background="#f0dfbf",
                       foreground="black")
        
        style.map('TNotebook.Tab',
                 background=[('selected', '#d9c9ac'), ('active', '#e5d4b4')],
                 foreground=[('selected', 'black'), ('active', 'black')])
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загружаем сохраненный путь после создания виджетов
        self.load_saved_path()
        
        # Создаем установщик
        self.installer = Installer(self.install_path.get(), self.t)

    def get_fonts(self):
        """Возвращает шрифты"""
        return self.fonts

    def change_language(self, new_lang):
        """Меняет язык интерфейса"""
        # Запоминаем текущую вкладку
        current_tab = self.notebook.select()
        current_tab_id = self.notebook.index(current_tab)
        
        self.lang = new_lang
        self.t = get_translation(self.lang)
        
        # Обновляем заголовок окна
        self.root.title(self.t['window_title'])
        
        # Обновляем основные элементы интерфейса
        self.path_label.config(text=self.t['select_path'])
        self.install_button.config(text=self.t['install'])
        self.update_gameinfo_button.config(text=self.t['update_gameinfo'])
        self.english_names_button.config(text=self.t['english_names'])
        self.restore_names_button.config(text=self.t['restore_names'])
        self.remove_all_mods_button.config(text=self.t['remove_all_mods'])
        
        # Обновляем информационную панель
        self.title_label.config(text=self.t['mod_info'])
        self.description_label.config(text=self.t.get('select_mod', 'Выберите мод для просмотра информации'))
        
        # Очищаем информацию о моде
        self.hide_mod_info()
        
        # Обновляем заголовки вкладок
        for index, category in enumerate(['About'] + [cat for cat in self.t['categories'] if cat != 'About']):
            self.notebook.tab(index, text=self.t['categories'][category])
        
        # Обновляем вкладку About
        if hasattr(self, 'about_label'):
            self.about_label.config(text=self.t['about']['main_text'])
            
        if hasattr(self, 'warning_label'):
            self.warning_label.config(text=self.t['about']['warning'])
        
        # Обновляем установщик с новыми переводами
        self.installer = Installer(self.install_path.get(), self.t)
        
        # Сохраняем выбранный язык
        try:
            config_path = get_resource_path("config.json")
            config = {}
            if os.path.exists(config_path):
                with codecs.open(config_path, 'r', 'utf-8') as f:
                    config = json.load(f)
            config['language'] = new_lang
            with codecs.open(config_path, 'w', 'utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Не удалось сохранить язык: {e}")
        
        # Возвращаемся к предыдущей вкладке
        self.notebook.select(current_tab_id)

    def reload_mods(self):
        """Перезагружает моды с новыми переводами"""
        # Сохраняем текущие выборы
        current_selections = {}
        for category, mods in self.selected_mods.items():
            current_selections[category] = {
                mod: var.get() for mod, var in mods.items()
            }
            
        # Очищаем текущие вкладки
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
            
        # Пересоздаем вкладки
        self.selected_mods = {category: {} for category in self.t['categories']}
        
        # Воссоздаем вкладки с новыми переводами
        for category in self.selected_mods.keys():
            if category == 'About':
                tab = self.create_about_tab(self.notebook)
            elif category == 'Skins':
                tab = self.create_skins_tab(self.notebook)
            else:
                tab = self.create_mod_list(self.notebook, category)
            self.notebook.add(tab, text=self.t['categories'][category])
            
        # Восстанавливаем выборы
        for category, mods in current_selections.items():
            if category in self.selected_mods:
                for mod, value in mods.items():
                    if mod in self.selected_mods[category]:
                        self.selected_mods[category][mod].set(value)
        
    def create_widgets(self):
        """Создает все виджеты приложения"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill="both", expand=True)
        
        # Верхняя панель с кнопками
        top_frame = self.create_top_frame(main_frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Основной контент
        content_frame = ttk.Frame(main_frame, style='TFrame')
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Инициализируем словарь для хранения выбранных модов
        self.selected_mods = {category: {} for category in self.t['categories']}
        
        # Создаем вкладки
        tab_order = ['About'] + [cat for cat in self.t['categories'] if cat != 'About']
        for category in tab_order:
            if category == 'About':
                tab = self.create_about_tab(self.notebook)
            elif category == 'Skins':
                tab = self.create_skins_tab(self.notebook)
            else:
                tab = self.create_mod_list(self.notebook, category)
            self.notebook.add(tab, text=self.t['categories'][category])
        
        # Правая информационная панель
        self.info_frame = self.create_mod_info_frame(content_frame)
        self.info_frame.pack(side=tk.RIGHT, fill="y", padx=(10, 0))
        
        # Прогресс бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=5)
        
        # Метка статуса
        self.status_label = ttk.Label(main_frame, text="", style='TLabel')
        self.status_label.pack()
        
    def setup_styles(self):
        """Настраивает стили для виджетов"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Определяем основные цвета
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        button_bg = '#3c3f41'
        button_fg = '#ffffff'
        
        # Настраиваем стили для фреймов
        style.configure('Main.TFrame', background=bg_color)
        style.configure('Info.TFrame', background=bg_color)
        
        # Настраиваем стили для меток
        style.configure('Info.TLabel',
            background=bg_color,
            foreground=fg_color,
            font=self.fonts['default']
        )
        
        # Настраиваем стили для кнопок
        style.configure('TButton',
            background=button_bg,
            foreground=button_fg,
            font=self.fonts['default']
        )
        
        # Настраиваем стили для вкладок
        style.configure('TNotebook',
            background=bg_color,
            foreground=fg_color
        )
        style.configure('TNotebook.Tab',
            background=button_bg,
            foreground=button_fg,
            font=self.fonts['default']
        )
        
        # Настраиваем стили для радиокнопок и чекбоксов
        style.configure('TRadiobutton',
            background=bg_color,
            foreground=fg_color,
            font=self.fonts['default']
        )
        style.configure('TCheckbutton',
            background=bg_color,
            foreground=fg_color,
            font=self.fonts['default']
        )
        
        # Основные стили
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('Skins.TFrame', background=self.colors['dark_bg'])
        style.configure('Character.TFrame', background=self.colors['darker_bg'])
        
        # Стиль для вкладок
        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', 
            background=self.colors['bg'],
            foreground=self.colors['text'],
            padding=[10, 5]
        )
        
        # Стиль для активной вкладки
        style.map('TNotebook.Tab',
            background=[('selected', self.colors['dark_bg'])],
            foreground=[('selected', self.colors['text'])]
        )
        
        # Стиль для радиокнопок в категории скинов
        style.configure('Skins.TRadiobutton', 
            background=self.colors['darker_bg'],
            foreground=self.colors['text']
        )
        style.map('Skins.TRadiobutton',
            background=[('active', self.colors['darker_bg']),
                       ('selected', self.colors['darker_bg'])]
        )
        
        # Стиль для меток
        style.configure('TLabel',
            background=self.colors['bg'],
            foreground=self.colors['text']
        )
        
        # Стиль для кнопок
        style.configure('TButton',
            background=self.colors['button'],
            foreground="black"
        )
        
        # Стиль для кнопки установки
        style.configure('Accent.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для кнопки удаления
        style.configure('Warning.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для кнопок языка
        style.configure('Lang.TButton',
                       background=self.colors['button'],
                       foreground="black",
                       padding=3,
                       width=3,
                       font=self.fonts['default'])
                       
        # Стиль для чекбоксов
        style.configure('TCheckbutton',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
                       
        # Стиль для полей ввода
        style.configure('TEntry',
                       background="white",
                       foreground="black",
                       font=self.fonts['default'])
                       
        # Стиль для комбобоксов
        style.configure('TCombobox',
                       background=self.colors['button'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['button'],
                       font=self.fonts['default'])
                       
        # Настройка вкладок
        style.configure('TNotebook.Tab',
                       background=self.colors['button'],
                       foreground=self.colors['text'],
                       padding=[10, 2],
                       font=self.fonts['default'])
                       
        # Настройка выбранной вкладки
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['button'])],
                 foreground=[('selected', self.colors['text'])])
        
        # Стиль для заголовков
        style.configure('Header.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['header'])
        
        # Стиль для предупреждений
        style.configure('Warning.TLabel',
                       background=self.colors['bg'],
                       foreground='red',
                       font=self.fonts['warning'])
        
        # Стиль для блоков скинов
        style.configure('Skin.TFrame',
                       background=self.colors['dark_bg'])
        
        # Стиль для меток в блоке скинов
        style.configure('Skin.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
        
        # Стиль для радиокнопок в блоке скинов
        style.configure('Skin.TRadiobutton',
                       foreground=self.colors['text'],
                       background=self.colors['dark_bg'],
                       font=self.fonts['default'])
                       
        # Стиль для информационного фрейма и его компонентов
        style.configure('Info.TFrame', background=self.colors['dark_bg'])
        style.configure('Title.TFrame', background=self.colors['dark_bg'])
        style.configure('Title.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['title'])
        style.configure('Info.TLabel',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.fonts['default'])
        
        # Настройка цветов корневого окна
        self.root.configure(bg=self.colors['bg'])
        
        # Создаем стиль для информационного блока
        style.configure('Info.TFrame', background=self.colors['bg'], borderwidth=1, relief='solid')
        style.configure('Info.TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        
    def load_saved_path(self):
        """Загружает сохраненный путь к игре из файла конфигурации"""
        try:
            config_path = get_resource_path("config.json")
            if os.path.exists(config_path):
                with codecs.open(config_path, 'r', 'utf-8') as f:
                    config = json.load(f)
                    if 'game_path' in config:
                        self.install_path.set(config['game_path'])
                    if 'language' in config:
                        self.change_language(config['language'])
        except Exception as e:
            print(f"Не удалось загрузить конфигурацию: {e}")

    def save_path(self):
        """Сохраняет путь к игре в файл конфигурации"""
        try:
            config_path = get_resource_path("config.json")
            config = {}
            if os.path.exists(config_path):
                with codecs.open(config_path, 'r', 'utf-8') as f:
                    config = json.load(f)
            config['game_path'] = self.install_path.get()
            with codecs.open(config_path, 'w', 'utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Не удалось сохранить путь: {e}")

    def browse_path(self):
        """Открывает диалог выбора пути и сохраняет выбранный путь"""
        directory = filedialog.askdirectory(title=self.t['select_path'])
        if directory:
            self.install_path.set(directory)
            self.save_path()
            self.installer.game_path = directory

    def create_mod_list(self, parent, category):
        """Создает список модов для указанной категории"""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        
        if category == 'Skins':
            return frame
            
        # Создаем канвас и скроллбар
        canvas = tk.Canvas(frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Получаем моды для категории
        mods = MODS.get(category, {})
        if isinstance(mods, list):  # Если моды в виде списка
            mods = {mod: None for mod in mods}  # Преобразуем в словарь
            
        # Создаем чекбоксы для каждого мода
        for mod_name in mods:
            var = tk.BooleanVar(value=False)
            self.selected_mods[category][mod_name] = var
            
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=mod_name,
                variable=var,
                style='TCheckbutton'
            )
            cb.pack(anchor="w", padx=5, pady=2)
            
            # Добавляем обработчики событий мыши
            cb.bind('<Enter>', lambda e, m=mod_name: self.show_mod_info(m))
            cb.bind('<Leave>', lambda e: self.hide_mod_info())
        
        # Размещаем канвас и скроллбар
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return frame
        
    def show_mod_info(self, mod_name):
        """Показывает информацию о моде"""
        # Очищаем предыдущую информацию
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Получаем описание мода на текущем языке
        mod_info = get_mod_description(mod_name, self.lang)
        
        # Создаем метку с названием мода
        mod_title = ttk.Label(
            self.info_frame,
            text=mod_name,
            style='Info.TLabel',
            font=self.fonts['header']
        )
        mod_title.pack(pady=(10, 5), padx=10, anchor='w')
        
        # Добавляем информацию о размере файла
        mod_file = f"{mod_name}.vpk"
        mod_path = os.path.join(self.local_mods_dir, mod_file)
        if os.path.exists(mod_path):
            size = os.path.getsize(mod_path)
            size_mb = size / (1024 * 1024)
            size_label = ttk.Label(
                self.info_frame,
                text=f"{size_mb:.1f} MB",
                style='Info.TLabel'
            )
            size_label.pack(pady=2, padx=10, anchor='w')
        
        # Добавляем автора мода
        if 'author' in mod_info:
            author_label = ttk.Label(
                self.info_frame,
                text=f"{self.t['author']}: {mod_info['author']}",
                style='Info.TLabel'
            )
            author_label.pack(pady=2, padx=10, anchor='w')
        
        # Добавляем описание мода
        if 'description' in mod_info:
            description_label = ttk.Label(
                self.info_frame,
                text=mod_info['description'],
                style='Info.TLabel',
                wraplength=680,
                justify='left'
            )
            description_label.pack(pady=(10, 5), padx=10, anchor='w')
        
        # Добавляем изображение, если оно есть
        if 'media' in mod_info and 'preview' in mod_info['media'] and mod_info['media']['preview']:
            image_path = get_resource_path(os.path.join('media', mod_info['media']['preview']))
            print(f"Trying to load image from: {image_path}")
            print(f"File exists: {os.path.exists(image_path)}")
            if os.path.exists(image_path):
                try:
                    print(f"Opening image file...")
                    image = Image.open(image_path)
                    print(f"Image opened successfully. Size: {image.size}")
                    # Масштабируем изображение, сохраняя пропорции
                    max_width = 680
                    max_height = 300
                    ratio = min(max_width/image.width, max_height/image.height)
                    new_width = int(image.width * ratio)
                    new_height = int(image.height * ratio)
                    
                    print(f"Resizing image to: {new_width}x{new_height}")
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Creating PhotoImage...")
                    photo = ImageTk.PhotoImage(image)
                    print(f"PhotoImage created successfully")
                    
                    image_label = ttk.Label(self.info_frame, image=photo, style='Info.TLabel')
                    image_label.image = photo
                    image_label.pack(pady=10)
                    print(f"Image displayed successfully")
                except Exception as e:
                    print(f"Error loading image: {e}")
                    print(f"Error type: {type(e)}")
                    import traceback
                    traceback.print_exc()
            
    def hide_mod_info(self):
        """Скрывает информацию о моде"""
        self.title_label.config(text="")
        self.info_label.config(text="")
        self.description_label.config(text=self.t.get('select_mod', 'Выберите мод для просмотра информации'))
        
        # Очищаем фрейм с изображением
        for widget in self.media_frame.winfo_children():
            widget.destroy()
            
    def update_progress(self, value, status_text=""):
        """Обновляет прогресс бар и текст статуса"""
        self.progress_var.set(value)
        self.status_label.config(text=status_text)
        self.root.update_idletasks()

    def install_mods(self):
        """Запускает установку модов"""
        print("Selected mods structure:")
        for category, mods in self.selected_mods.items():
            print(f"\n{category}:")
            for mod_name, var in mods.items():
                if isinstance(var, tk.StringVar):
                    print(f"  {mod_name}: {var.get()}")
                else:
                    print(f"  {mod_name}: {var.get()}")
                    
        self.installer.game_path = self.install_path.get()
        self.installer.install_mods(
            self.selected_mods,
            progress_callback=self.update_progress
        )

    def update_gameinfo(self):
        """Обновляет gameinfo.gi"""
        if not self.install_path.get():
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return
            
        self.installer.game_path = self.install_path.get()
        self.installer.update_gameinfo()
        messagebox.showinfo(self.t['success'], self.t['gameinfo_updated'])

    def apply_english_names(self):
        """Применяет английские имена"""
        if not self.install_path.get():
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return
            
        try:
            # Получаем список файлов локализации
            loc_files = [f for f in os.listdir(self.new_loc_path) if f.endswith('.txt')]
            
            # Устанавливаем файлы локализации
            if self.installer.install_localization(loc_files):
                messagebox.showinfo(self.t['success'], self.t['english_names_success'])
            
        except Exception as e:
            messagebox.showerror(self.t['error'], str(e))
            
    def restore_original_names(self):
        """Восстанавливает оригинальные имена"""
        if not self.install_path.get():
            messagebox.showerror(self.t['path_error'], self.t['path_error_msg'])
            return
            
        try:
            # Сначала удаляем текущие файлы локализации
            self.installer.remove_localization()
            
            # Затем восстанавливаем оригинальные
            if self.installer.restore_original_localization():
                messagebox.showinfo(self.t['success'], self.t['restore_names_success'])
            
        except Exception as e:
            messagebox.showerror(self.t['error'], str(e))

    def remove_all_mods(self):
        """Удаляет все установленные моды"""
        if messagebox.askyesno(
            self.t['confirm'],
            self.t['remove_all_mods_confirm'],
            icon='warning'
        ):
            self.installer.remove_all_mods()

    def create_skins_tab(self, notebook):
        """Создает вкладку для выбора скинов"""
        tab = ttk.Frame(notebook, style='Skins.TFrame')
        
        # Настраиваем веса для tab
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        # Создаем канвас и скроллбар для прокрутки
        canvas = tk.Canvas(tab, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Skins.TFrame')
        
        # Настраиваем веса для scrollable_frame
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_rowconfigure(0, weight=1)
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(frame_id, width=canvas.winfo_width())
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        
        frame_id = canvas.create_window(0, 0, window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig(frame_id, width=canvas.winfo_width())
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Получаем словарь персонажей и их скинов
        characters = MODS.get('Skins', {})
        
        # Создаем главный контейнер для сетки
        grid_frame = ttk.Frame(scrollable_frame, style='Skins.TFrame')
        grid_frame.pack(expand=True, fill="both", padx=20)
        
        # Настраиваем колонки для центрирования
        grid_frame.grid_columnconfigure(0, weight=0)  # Отступ слева
        grid_frame.grid_columnconfigure(1, weight=1)  # Первая колонка с блоком
        grid_frame.grid_columnconfigure(2, weight=1)  # Вторая колонка с блоком
        grid_frame.grid_columnconfigure(3, weight=0)  # Отступ справа
        
        # Создаем секции для каждого персонажа
        row = 0
        col = 1
        for char_name, char_skins in characters.items():
            # Создаем фрейм для персонажа с более темным фоном
            char_frame = tk.Frame(grid_frame, bg=self.colors['darker_bg'])
            char_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            
            # Создаем внутренний фрейм для контента
            content_frame = tk.Frame(char_frame, bg=self.colors['darker_bg'])
            content_frame.pack(expand=True, fill="both", padx=5, pady=5)
            
            # Метка с именем персонажа
            char_label = tk.Label(
                content_frame,
                text=char_name,
                font=self.fonts['header'],
                bg=self.colors['darker_bg'],
                fg=self.colors['text']
            )
            char_label.pack(anchor="center", padx=5, pady=(5,10))
            
            # Создаем радиогруппу для скинов персонажа
            var = tk.StringVar(value="Default")
            self.selected_mods['Skins'][char_name] = var
            
            # Создаем фрейм для радиокнопок с центрированием
            radio_frame = tk.Frame(content_frame, bg=self.colors['darker_bg'])
            radio_frame.pack(expand=True, fill="both")
            
            # Создаем внутренний фрейм для центрирования радиокнопок
            radio_center_frame = tk.Frame(radio_frame, bg=self.colors['darker_bg'])
            radio_center_frame.pack(expand=True)
            
            # Радиокнопка для дефолтного скина
            rb = ttk.Radiobutton(
                radio_center_frame,
                text="Default",
                variable=var,
                value="Default",
                style='Skins.TRadiobutton'
            )
            rb.pack(anchor="center", padx=20, pady=2)
            rb.bind('<Enter>', lambda e, m=f"{char_name} Default": self.show_mod_info(m))
            rb.bind('<Leave>', lambda e: self.hide_mod_info())
            
            # Создаем радиокнопки для каждого скина
            for skin_name in char_skins:
                rb = ttk.Radiobutton(
                    radio_center_frame,
                    text=skin_name,
                    variable=var,
                    value=skin_name,
                    style='Skins.TRadiobutton'
                )
                rb.pack(anchor="center", padx=20, pady=2)
                rb.bind('<Enter>', lambda e, m=skin_name: self.show_mod_info(m))
                rb.bind('<Leave>', lambda e: self.hide_mod_info())
            
            # Переходим к следующей позиции в сетке
            col += 1
            if col > 2:  # Если достигли конца строки
                col = 1  # Возвращаемся к первой колонке
                row += 1  # Переходим на следующую строку
        
        # Настраиваем веса строк для равномерного распределения
        for i in range(row + 1):
            grid_frame.grid_rowconfigure(i, weight=1)
        
        # Размещаем канвас и скроллбар с помощью grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Настраиваем скроллинг мышью
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return tab
        
    def create_about_tab(self, notebook):
        """Создает вкладку с информацией о программе"""
        tab = ttk.Frame(notebook, style='Info.TFrame')
        
        # Создаем метку с версией
        version_label = ttk.Label(
            tab,
            text=f"DMI v{VERSION} 28.11.2024",
            style='Info.TLabel',
            font=self.fonts['header']
        )
        version_label.pack(fill="x", pady=(20, 10), padx=20)
        
        # Создаем метку с предупреждением
        self.warning_label = ttk.Label(
            tab,
            text=self.t['about']['warning'],
            style='Info.TLabel',
            wraplength=680,
            justify='left',
            foreground='red',
            font=('Arial', 14, 'bold')
        )
        self.warning_label.pack(pady=(20, 20), padx=20)
        
        # Создаем метку с описанием
        self.about_label = ttk.Label(
            tab,
            text=self.t['about']['main_text'],
            style='Info.TLabel',
            wraplength=680,
            justify='left'
        )
        self.about_label.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return tab

    def create_mod_info_frame(self, parent):
        """Создает фрейм с информацией о модах"""
        info_frame = ttk.Frame(parent, style='Info.TFrame', width=700)
        info_frame.pack(side=tk.RIGHT, fill="y", padx=(10, 0))
        info_frame.pack_propagate(False)  # Запрещаем изменение размера

        # Заголовок
        self.title_label = ttk.Label(
            info_frame,
            text=self.t['mod_info'],
            style='Info.TLabel',
            font=self.fonts['header']
        )
        self.title_label.pack(fill="x", pady=(10, 5), padx=10)

        # Информация о моде
        self.info_label = ttk.Label(
            info_frame,
            text="",
            style='Info.TLabel'
        )
        self.info_label.pack(fill="x", pady=5, padx=10)

        # Фрейм для медиа-контента с темным фоном
        self.media_frame = ttk.Frame(info_frame, style='Info.TFrame')
        self.media_frame.pack(fill="x", pady=5, padx=10)
        self.media_frame.configure(height=300)
        self.media_frame.pack_propagate(False)  # Фиксированная высота

        # Описание мода
        self.description_label = ttk.Label(
            info_frame,
            text=self.t.get('select_mod', 'Выберите мод для просмотра информации'),
            style='Info.TLabel',
            wraplength=680,
            justify='left'
        )
        self.description_label.pack(fill="x", pady=5, padx=10)

        return info_frame

    def create_top_frame(self, parent):
        """Создает верхнюю панель с кнопками"""
        top_panel = ttk.Frame(parent, style='TFrame')
        
        # Кнопки языка
        lang_frame = ttk.Frame(top_panel, style='TFrame')
        lang_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            lang_frame,
            text="EN",
            command=lambda: self.change_language('en'),
            style="Lang.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            lang_frame,
            text="RU",
            command=lambda: self.change_language('ru'),
            style="Lang.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        # Заголовок приложения
        title_frame = ttk.Frame(top_panel, style='TFrame')
        title_frame.pack(fill="x", padx=10)
        
        self.title_label = ttk.Label(
            title_frame,
            text=self.t['window_title'],
            style='TLabel'
        )
        self.title_label.pack(anchor="center")
        
        # Фрейм для пути к игре
        path_frame = ttk.Frame(top_panel, style='TFrame')
        path_frame.pack(fill="x", pady=(10, 0))
        
        # Метка для пути
        self.path_label = ttk.Label(
            path_frame,
            text=self.t['select_path'],
            style='Path.TLabel',
            foreground="white"
        )
        self.path_label.pack(side=tk.LEFT)
        
        # Поле ввода пути
        self.path_entry = ttk.Entry(
            path_frame,
            textvariable=self.install_path,
            style='TEntry',
            width=50
        )
        self.path_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        # Кнопка выбора пути
        browse_button = ttk.Button(
            path_frame,
            text="...",
            command=self.browse_path,
            width=3
        )
        browse_button.pack(side=tk.LEFT)
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(top_panel, style='TFrame')
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Кнопка установки
        self.install_button = ttk.Button(
            button_frame,
            text=self.t['install'],
            command=self.install_mods,
            style='Accent.TButton'
        )
        self.install_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка обновления gameinfo
        self.update_gameinfo_button = ttk.Button(
            button_frame,
            text=self.t['update_gameinfo'],
            command=self.update_gameinfo
        )
        self.update_gameinfo_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопка удаления всех модов
        self.remove_all_mods_button = ttk.Button(
            button_frame,
            text=self.t['remove_all_mods'],
            command=self.remove_all_mods,
            style='Warning.TButton'
        )
        self.remove_all_mods_button.pack(side=tk.LEFT, padx=5)
        
        # Кнопки локализации
        self.english_names_button = ttk.Button(
            button_frame,
            text=self.t['english_names'],
            command=self.apply_english_names
        )
        self.english_names_button.pack(side=tk.RIGHT, padx=5)
        
        self.restore_names_button = ttk.Button(
            button_frame,
            text=self.t['restore_names'],
            command=self.restore_original_names
        )
        self.restore_names_button.pack(side=tk.RIGHT, padx=5)
        
        return top_panel
