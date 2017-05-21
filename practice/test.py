
from os.path import dirname, abspath, join, exists
from os import mkdir
import unittest

from yml2pdf.rendering import Document


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.stuff_dir = abspath(join(dirname(__file__), 'test_stuff'))

    def test_draw(self):
        out_filename = join(dirname(__file__), 'test_draw.pdf')

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
              textColor: '#FF0000'
              fontSize: 12

          - !Spacer
            height: 100
            
          - !Paragraph
            text: 'Hello word again'
            styles:
              fontSize: 18
              
          - !Spacer
            height: 10
                        
          - !Paragraph
            text: 'Goodbye world'
            styles:
              fontSize: 8
              textColor: '#FF592F'

        """

        doc = Document(yml, out_filename)

        ctx = dict(
            stuff=self.stuff_dir,
        )

        doc.register_fonts(ctx)

        doc.build()


if __name__ == '__main__':
    unittest.main()
