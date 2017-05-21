
from os.path import dirname, abspath, join, exists
from os import mkdir
import unittest

from yml2pdf.rendering import Document


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = abspath(join(dirname(__file__), 'temp'))
        self.stuff_dir = abspath(join(dirname(__file__), 'test_stuff'))
        if not exists(self.temp_dir):
            mkdir(self.temp_dir)

    def test_draw(self):
        out_filename = join(self.temp_dir, 'test_draw.pdf')

        yml = """
        width: 595
        height: 842

        fonts:
          default: tahoma
          tahoma: '%(stuff)s/tahoma.ttf'
          tahoma-bold: '%(stuff)s/tahoma-bold.ttf'

        body:
          - !Spacer
            height: 100

          - !Paragraph
            text: 'Hello word'
            styles:
              text_color: '#FF0000'
              font_size: 12

          - !Spacer
            height: 100
            
          - !Paragraph
            text: 'Hello word again'
            styles:
              font_size: 18
              
          - !Spacer
            height: 10
                        
          - !Paragraph
            text: 'Goodbye world'
            styles:
              font_size: 8
              text_color: '#00FF00'

        """

        doc = Document(yml, out_filename)

        ctx = dict(
            stuff=self.stuff_dir,
            temp=self.temp_dir
        )

        doc.register_fonts(ctx)

        doc.build()


if __name__ == '__main__':
    unittest.main()
