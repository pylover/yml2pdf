
# noinspection PyPackageRequirements
import yaml
from rtl import rtl

from yml2pdf.rendering import Document


class Element(yaml.YAMLObject):

    def draw(self, canvas: Document, context: dict):
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
