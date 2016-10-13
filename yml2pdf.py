import io

# noinspection PyPackageRequirements
import yaml
from rtl import rtl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts

__version__ = '0.1.0-dev0'


# noinspection PyClassicStyleClass, PyAbstractClass
class Template(canvas.Canvas):
    """

    Draw a YAML structure into ReportLab's canvas.

    :param yml: ``str`` or ``file-like`` object.
    :param out_file: ``str`` or ``file-like`` object.
    """

    def __init__(self, yml, out_file=None):
        # yaml.add_constructor('!label', Label)
        self.data = yaml.load(yml)
        self.outfile = out_file or io.BytesIO()
        self.current_page = 0

        canvas.Canvas.__init__(self, self.outfile, pagesize=(self.width, self.height))

    def measure_width(self, text):
        return pdfmetrics.stringWidth(text, self._fontname, self._fontsize)

    @property
    def version(self):
        return self.data.get('version')

    @property
    def fonts(self):
        return self.data.get('fonts')

    @property
    def body(self):
        return self.data.get('body')

    @property
    def font_name(self):
        return self._fontname

    @property
    def default_font(self) -> str:
        if not self.fonts:
            return None

        name = self.fonts.get('default')
        if name:
            return name

        return next(self.fonts.keys())

    @property
    def width(self):
        return self.data['width']

    @property
    def height(self):
        return self.data['height']

    def register_fonts(self, context):
        if self.fonts:

            for font_name, font_filename in self.fonts.items():
                if font_name == 'default':
                    continue
                pdfmetrics.registerFont(ttfonts.TTFont(font_name % context, font_filename % context))

    def draw_new_page(self, context):
        if self.current_page > 0:
            self.showPage()
        self.current_page += 1

        for element in self.body:
            element.draw(self, context)


class Element(yaml.YAMLObject):

    def draw(self, canvas: Template, context: dict):
        raise NotImplementedError()


class TextRenderModes(object):
    fill_text = 0
    stroke_text = 1
    fill_then_stroke = 2
    invisible = 3
    fill_text_and_add_to_clipping_path = 4
    stroke_text_and_add_to_clipping_path = 5
    fill_then_stroke_and_add_to_clipping_path = 6
    add_to_clipping_path = 7


class Label(Element):
    yaml_tag = '!Label'

    mode = TextRenderModes.fill_text
    text = None
    pos = (0, 0)
    font = None
    font_size = 10
    rtl = None

    def ensure_font(self, tableau):
        font_name = self.font or tableau.default_font

        if tableau.font_name != font_name:
            tableau.setFont(font_name, self.font_size)

    def draw(self, tableau, context):
        self.ensure_font(tableau)

        text = self.text % context
        if self.rtl:
            text = rtl(text)

        tableau.drawString(self.pos[0], self.pos[1], text, mode=self.mode)


# def draw_center(self, y, text):
#     self.drawCentredString(self.width / 2.0, y, text)
#


# from reportlab.graphics.barcode import code128
# def draw_barcode(self, code, x, y, width, height):
#     barcode = code128.Code128(
#         code,
#         quiet=0,
#         barWidth=width,
#         barHeight=height)
#     barcode.drawOn(self, x, y)