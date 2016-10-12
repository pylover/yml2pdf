
from os.path import dirname, abspath, join, exists
from os import mkdir
import io
import unittest

from yml2pdf import Template, Label


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = abspath(join(dirname(__file__), 'temp'))
        if not exists(self.temp_dir):
            mkdir(self.temp_dir)

    def test_draw(self):
        out_filename = join(self.temp_dir, 'test_draw.pdf')

        yml = """

        width: 800
        height: 600

        body:
          - !label
            text: 'Page: %(page)s'
            pos: [20, 20]


          - !label
            text: 'Lorem Ipsum'
            pos: [20, 100]

          - !label
            text: 'لورم ایپسام'
            pos: [20, 200]


        """

        out = io.BytesIO()
        t = Template(yml, out)

        self.assertEqual(t.data['width'], 800)
        self.assertEqual(t.data['height'], 600)
        self.assertIsInstance(t.data['body'][0], Label)
        self.assertEqual(t.data['body'][1].text, 'Lorem Ipsum')

        for i in range(5):
            t.draw_new_page(dict(page=i+1))
        t.save()
        out.seek(0)

        with open(out_filename, 'wb') as f:
            f.write(out.read())
        self.assertEqual(len(out.getbuffer()) // 100, 37)

