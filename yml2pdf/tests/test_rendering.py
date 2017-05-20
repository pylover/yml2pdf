
from os.path import dirname, abspath, join, exists
from os import mkdir
import io
import unittest

from yml2pdf.rendering import Template
from yml2pdf.elements import Label


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = abspath(join(dirname(__file__), 'temp'))
        self.stuff_dir = abspath(join(dirname(__file__), 'test_stuff'))
        if not exists(self.temp_dir):
            mkdir(self.temp_dir)

    def test_draw(self):
        out_filename = join(self.temp_dir, 'test_draw.pdf')

        yml = """

        version: 1
        width: 800
        height: 600

        fonts:
          default: tahoma
          tahoma: '%(stuff)s/tahoma.ttf'
          tahoma-bold: '%(stuff)s/tahoma-bold.ttf'

        body:
          - !Label
            text: 'Page: %(page)s'
            pos: [20, 20]


          - !Label
            text: 'Lorem Ipsum'
            pos: [20, 100]

          - !Label
            text: 'لورم ایپسام'
            pos: [20, 200]
            rtl: true


        """

        out = io.BytesIO()
        t = Template(yml, out)

        ctx = dict(
            stuff=self.stuff_dir,
            temp=self.temp_dir,
        )

        t.register_fonts(ctx)

        self.assertEqual(t.data['width'], 800)
        self.assertEqual(t.data['height'], 600)
        self.assertIsInstance(t.data['body'][0], Label)
        self.assertEqual(t.data['body'][1].text, 'Lorem Ipsum')

        for i in range(5):
            ctx['page'] = i + 1
            t.draw_new_page(ctx)
        t.save()
        out.seek(0)

        with open(out_filename, 'wb') as f:
            f.write(out.read())

        file_length = len(out.getbuffer())
        self.assertTrue(file_length // 100 >= 290)


if __name__ == '__main__':
    unittest.main()
