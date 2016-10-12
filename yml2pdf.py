import io

# noinspection PyPackageRequirements
import yaml

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


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
        canvas.Canvas.__init__(self, self.outfile, pagesize=(self.width, self.height))

    def measure_width(self, text):
        return stringWidth(text, self._fontname, self._fontsize)

    @property
    def width(self):
        return self.data['width']

    @property
    def height(self):
        return self.data['height']

    def draw(self):
        for element in self.data['body']:
            element.draw(self)
        self.save()

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


class Element(yaml.YAMLObject):
    def draw(self, canvas: Template):
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

    yaml_tag = '!label'
    mode = TextRenderModes.fill_text
    text = None
    pos = (0, 0)

    # __slots__ = ('text', 'pos')

    def draw(self, tableau: Template):
        tableau.drawString(self.pos[0], self.pos[1], self.text, mode=self.mode)
