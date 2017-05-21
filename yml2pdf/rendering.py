import io

# noinspection PyPackageRequirements
import yaml
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import SimpleDocTemplate

from yml2pdf.elements import Spacer, Element

# noinspection PyClassicStyleClass, PyAbstractClass
class Document:
    """

    Draw a YAML structure into ReportLab's canvas.

    :param yml: ``str`` or ``file-like`` object.
    :param out_file: ``str`` or ``file-like`` object.
    """

    def __init__(self, yml, out_file=None):
        self.data = yaml.load(yml)
        self.outfile = out_file or io.BytesIO()
        self.current_page = 0
        self.doc = SimpleDocTemplate(
            self.outfile,
            pagesize=[self.width, self.height],
            rightMargin=20, leftMargin=20,
            topMargin=20, bottomMargin=20
        )
        self.story = []

        for element in self.body:
            self.story.append(element.flowable)

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

    def build(self):
        self.doc.build(self.story)
