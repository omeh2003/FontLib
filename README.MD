# Иконка SVG в TTF

Этот скрипт позволяет генерировать TTF-шрифт из SVG-файлов, создавать Dart файл с IconData и объединять все SVG-файлы в один.

## Установка

Прежде всего, убедитесь, что у вас установлены все необходимые зависимости:
- fontTools
- fontforge
- svgutils

Вы можете установить их с помощью pip:

```bash
pip install fontTools fontforge svgutils
```

Ubuntu
```bash
sudo apt-get install -y fontforge python3-fontforge fontforge-extras
```

## Использование

### Как скрипт

```bash
python my_generate.py --svg_dir=./path/to/svg/files --ttf_file=output.ttf --fontname=MyFont --familyname=myfont --fullname=Regular --version=001.000 --design_size=16 --em=512 --ascent=448 --descent=64 --start_unicode_value=0xE000 --glyph_width=500 --dart_file=myfont_icons.dart --class_name=MyFontIcons --one_svg_file=myfont_one.svg --output_dir=./output
```

### Как модуль

```python
from main import make_font, generate_class_dart, generate_one_svg_file

# Создание шрифта
make_font("./path/to/svg/files", "output.ttf", "MyFont", "myfont", "Regular", "001.000", 16, 512, 448, 64, 0xE000, 500)

# Создание Dart файла с IconData
generate_class_dart("output.ttf", "myfont_icons.dart", "MyFontIcons")

# Объединение всех SVG файлов в один
generate_one_svg_file("myfont_one.svg", "./path/to/svg/files")
```

## Аргументы

- `svg_dir` - директория с SVG файлами.
- `ttf_file` - имя выходного TTF файла.
- `fontname` - внутреннее имя шрифта.
- `familyname` - имя семейства шрифтов.
- `fullname` - полное имя шрифта.
- `version` - версия шрифта.
- `design_size` - размер дизайна шрифта.
- `em` - размер шрифта 'em'.
- `ascent` - восхождение шрифта.
- `descent` - спуск шрифта.
- `start_unicode_value` - начальное значение Unicode для глифов.
- `glyph_width` - ширина глифа.
- `dart_file` - имя выходного Dart файла.
- `class_name` - имя класса для Dart файла.
- `one_svg_file` - имя выходного SVG файла.
- `debug` - включить режим отладки.
- `output_dir` - выходная директория.

## Логирование

Логирование реализовано на уровне ERROR. Если вы хотите увидеть больше информации, вы можете включить режим отладки, добавив флаг `--debug` при запуске скрипта.

# CI/CD конфигурация

## GitLab CI/CD

Мы используем GitLab CI/CD для автоматической генерации шрифтов при изменении SVG иконок.

GitLab CI/CD конфигурация определена в файле `.gitlab-ci.yml`.

### Стадии

Конфигурация определяет две стадии:

- `generate` - генерация шрифтов
- `build` - построение проекта

### Задачи

- `generate_classes` - эта задача выполняется на стадии `generate`. Она запускает Docker контейнер, который генерирует шрифты. Задача выполняется только при изменении иконок.
- `build` - эта задача выполняется на стадии `build`. В настоящий момент она просто выводит сообщение "Building the project...".

### Переменные

- `$CI_REGISTRY_USER` - имя пользователя для Docker реестра.
- `$CI_REGISTRY_PASSWORD` - пароль для Docker реестра.
- `$CI_REGISTRY` - адрес Docker реестра.
- `$ARGUMENTS_FOR_SCRIPT_GENERATE_ICONS` - аргументы для скрипта, генерирующего иконки.

## Dockerfile

Мы также используем Dockerfile для определения Docker образа, который используется для генерации шрифтов. Образ содержит все необходимые зависимости и наш скрипт для генерации шрифтов.

## Travis CI

Мы также можем использовать Travis CI для автоматической генерации шрифтов. Конфигурация определяет две стадии - `generate` и `build`. На стадии `generate` запускается скрипт `my_generate.py` с аргументами, определенными в переменной `$ARGUMENTS_FOR_SCRIPT_GENERATE_ICONS`. Эта задача выполняется только при изменении иконок.

### Переменные

- `$ARGUMENTS_FOR_SCRIPT_GENERATE_ICONS` - аргументы для скрипта, генерирующего иконки.

## GitHub Actions

Мы также можем использовать GitHub Actions для автоматической генерации шрифтов. Конфигурация определяет две стадии - `generate` и `build`. На стадии `generate` запускается скрипт `my_generate.py` с аргументами, определенными в переменной `$ARGUMENTS_FOR_SCRIPT_GENERATE_ICONS`. Эта задача выполняется только при изменении иконок.

### Docker

Мы используем Docker для запуска скрипта `my_generate.py`. Образ определен в файле `Dockerfile`.
```bash
docker build -t fontlib .
```
```bash
docker run -v .\\iconlib:/app/iconlib -v .\\output:/app/output -v .\\default_config.json:/app/default_config.json fontlib
```