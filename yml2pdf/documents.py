import io

# noinspection PyPackageRequirements
import yaml
from reportlab.platypus import SimpleDocTemplate


class Document:
    width = 595
    height = 842
    right_margin = 0
    left_margin = 0
    top_margin = 0
    bottom_margin = 0

    def __init__(self, yml, out_file=None):
        self.data = yaml.load(yml)
        self.outfile = out_file or io.BytesIO()
        self.doc = SimpleDocTemplate(
            self.outfile,
            pagesize=[self.document_property['width'], self.document_property['height']],
            rightMargin=self.document_property['right_margin'],
            leftMargin=self.document_property['left_margin'],
            topMargin=self.document_property['top_margin'],
            bottomMargin=self.document_property['bottom_margin']
        )
        self.story = []

        for element in self.body:
            self.story.append(element.to_flowable())

    @property
    def body(self):
        return self.data.get('body')

    @property
    def document_property(self):
        document_style = self.data['document']

        return dict(
            width=document_style['width'] if 'width' in document_style else self.width,
            height=document_style['height'] if 'height' in document_style else self.height,
            right_margin=document_style['right_margin'] if 'right_margin' in document_style else self.right_margin,
            left_margin=document_style['left_margin'] if 'left_margin' in document_style else self.left_margin,
            bottom_margin=document_style['bottom_margin'] if 'bottom_margin' in document_style else self.bottom_margin,
            top_margin=document_style['top_margin'] if 'top_margin' in document_style else self.top_margin
        )

    def build(self):
        self.doc.build(self.story)
