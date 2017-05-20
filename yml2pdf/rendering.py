import io

# noinspection PyPackageRequirements
import yaml
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts


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