import argparse
from fontTools.ttLib import TTFont
import os
import fontforge
import svgutils.transform as sg
import traceback
import json
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d - %(funcName)s()',
                    encoding='utf-8')
logger = logging.getLogger(__name__)


def make_font(svg_dir, ttf_file, fontname, familyname, fullname, version, design_size, em, ascent, descent,
              start_unicode_value, glyph_width):
    # Создаем новый шрифт в FontForge
    logger.debug("Creating new font in FontForge")
    font = fontforge.font()

    # Устанавливаем некоторые свойства шрифта
    font.fontname = fontname
    font.familyname = familyname
    font.fullname = fullname
    font.version = version

    # Устанавливаем размеры шрифта
    font.design_size = design_size
    font.em = em
    font.ascent = ascent
    font.descent = descent

    # Начинаем с заданного кода Unicode
    unicode_value = start_unicode_value
    logger.debug("Start unicode value: %s", unicode_value)
    # Добавляем все SVG-файлы в шрифт
    for filename in os.listdir(svg_dir):
        logger.debug("File name: %s", filename)
        if filename.endswith(".svg"):
            # Создаем новый глиф с именем файла (без расширения)
            glyph = font.createChar(unicode_value, os.path.splitext(filename)[0])
            logger.debug("Glyph name: %s", glyph.glyphname)
            # Импортируем SVG файл в глиф
            glyph.importOutlines(os.path.join(svg_dir, filename))
            logger.debug("Glyph importOutlines: %s", glyph.glyphname)
            # Увеличиваем код Unicode для следующего глифа
            unicode_value += 1

            # Устанавливаем ширину глифа
            glyph.width = glyph_width

    # Генерируем TTF-шрифт
    logger.debug("Generating TTF font")
    font.generate(ttf_file)
    logger.debug("TTF font generated")


def generate_class_dart(font_file, output_file, class_name):
    logger.debug("Generating icon data")
    logger.debug("Font file: %s", font_file)
    font = TTFont(font_file)

    icons = {}
    logger.debug("Font cmap tables: %s", font["cmap"].tables)
    for table in font["cmap"].tables:
        for code, name in table.cmap.items():
            logger.debug("Code: %s, name: %s", code, name)
            if not name.startswith("uni") and code >= 0x100 and name not in icons:
                logger.debug("Adding icon: %s", name)
                icons[
                    name] = f"  static const IconData {name.replace('-', '_').title()} = IconData(0x{code:X}, fontFamily: '{class_name}');\n"

    with open(output_file, "w") as f:
        logger.debug("Writing icon data to file: %s", output_file)
        f.write(f"class {class_name} {{\n")
        logger.debug("Icons: %s", icons)
        for icon in icons.values():
            f.write(icon)
        f.write("}\n")
    logger.debug("Icon data generated")


def generate_one_svg_file(file_name_one, svg_dir):
    # Указываем директорию, в которой находятся SVG-файлы
    svg_dir = svg_dir
    logger.debug("SVG dir: %s", svg_dir)
    # Указываем имя результирующего SVG файла
    output_svg = file_name_one
    logger.debug("Output SVG: %s", output_svg)

    # Создаем пустой SVG файл
    combined_svg = sg.SVGFigure()

    # Добавляем все SVG-файлы в общий SVG файл
    for filename in os.listdir(svg_dir):
        logger.debug("File name: %s", filename)
        if filename.endswith(".svg"):
            logger.debug("Adding SVG file: %s", filename)
            # Загружаем SVG файл
            svg_file = sg.fromfile(os.path.join(svg_dir, filename))
            logger.debug("SVG file loaded: %s", os.path.join(svg_dir, filename))
            # Добавляем SVG файл в общий SVG файл

            combined_svg.append(svg_file.getroot())

    # Сохраняем общий SVG файл
    logger.debug("Saving combined SVG file: %s", output_svg)
    combined_svg.save(output_svg)


def load_default_args_from_json(json_file_path: str = './default_config.json'):
    with open(json_file_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    default_args = load_default_args_from_json()

    parser = argparse.ArgumentParser(
        description='Generate a TTF font from SVG files. Make Dart file with IconData. And make one SVG file from all SVG files.')

    parser.add_argument('--svg_dir', default=default_args.get('svg_dir', './iconlib/'),
                        help='Directory with SVG files.')
    parser.add_argument('--ttf_file', default=default_args.get('ttf_file', 'CustomFont.ttf'),
                        help='Output TTF file name.')
    parser.add_argument('--fontname', default=default_args.get('fontname', 'CustomFont'), help='Internal font name.')
    parser.add_argument('--familyname', default=default_args.get('familyname', 'customfont'), help='Font family name.')
    parser.add_argument('--fullname', default=default_args.get('fullname', 'Regular'), help='Full font name.')
    parser.add_argument('--version', default=default_args.get('version', '001.000'), help='Font version.')
    parser.add_argument('--design_size', default=default_args.get('design_size', 16), type=int,
                        help='Font design size.')
    parser.add_argument('--em', default=default_args.get('em', 512), type=int, help='Font em size.')
    parser.add_argument('--ascent', default=default_args.get('ascent', 448), type=int, help='Font ascent.')
    parser.add_argument('--descent', default=default_args.get('descent', 64), type=int, help='Font descent.')
    parser.add_argument('--start_unicode_value', default=default_args.get('start_unicode_value', 0xE000), type=int,
                        help='Start unicode value for glyphs.')
    parser.add_argument('--glyph_width', default=default_args.get('glyph_width', 500), type=int, help='Glyph width.')
    parser.add_argument('--dart_file', default=default_args.get('dart_file', 'atomfont_icons.dart'),
                        help='Output Dart file name.')
    parser.add_argument('--class_name', default=default_args.get('class_name', 'CustomFontIcons'),
                        help='Class name for Dart file.')
    parser.add_argument('--one_svg_file', default=default_args.get('one_svg_file', 'customfont_one.svg'),
                        help='Output SVG file name.')
    parser.add_argument('--debug', action='store_true', default=default_args.get('debug', False),
                        help='Enable debug mode.')
    parser.add_argument('--output_dir', default=default_args.get('output_dir', './output'), help='Output directory.')

    args = parser.parse_args()
    logger.debug("Args: %s", args)
    try:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
            ttf_file = os.path.abspath(os.path.join(args.output_dir, args.ttf_file))
            dart_file = os.path.abspath(os.path.join(args.output_dir, args.dart_file))
            one_svg_file = os.path.abspath(os.path.join(args.output_dir, args.one_svg_file))
        else:
            for file in os.listdir(args.output_dir):
                os.remove(os.path.join(args.output_dir, file))
            ttf_file = os.path.abspath(os.path.join(args.output_dir, args.ttf_file))
            dart_file = os.path.abspath(os.path.join(args.output_dir, args.dart_file))
            one_svg_file = os.path.abspath(os.path.join(args.output_dir, args.one_svg_file))

        if args.debug:
            logger.setLevel(logging.DEBUG)

        make_font(args.svg_dir, ttf_file, args.fontname, args.familyname, args.fullname, args.version, args.design_size,
                  args.em, args.ascent, args.descent, args.start_unicode_value, args.glyph_width)
        generate_class_dart(ttf_file, dart_file, args.class_name)
        generate_one_svg_file(one_svg_file, args.svg_dir)
    except Exception as e:
        logger.error("Error: %s", e)
        logger.exception("Exception: %s", e)
        logger.exception("Trace %s", traceback.format_exc())
        raise e
