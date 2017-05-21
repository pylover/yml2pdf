# noinspection PyPackageRequirements
import yaml

from reportlab.lib.colors import HexColor
from reportlab.platypus import Spacer
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from yml2pdf.helpers import to_camel_case

class Element(yaml.YAMLObject):

    @property
    def flowable(self):
        raise NotImplementedError()

    def style_sheet(self, styles=None):
        style_sheet = getSampleStyleSheet()['Normal']

        for key, value in styles.items():
            key = to_camel_case(key)
            if hasattr(style_sheet, key):
                if key == 'textColor':
                    setattr(style_sheet, key, HexColor(value))
                else:
                    setattr(style_sheet, key, value)

        return style_sheet


class ParagraphElement(Element):
    yaml_tag = '!Paragraph'

    text = None
    styles = None

    @property
    def flowable(self):
        return Paragraph(self.text, self.style_sheet(self.styles))


class SpacerElement(Element):
    yaml_tag = "!Spacer"

    width = 0
    height = 0

    @property
    def flowable(self):
        return Spacer(self.width, self.height)
