from django.test import TestCase

from . import helper



class HelperTests(TestCase):

    def test_recid2img(self):
        self.assertEqual(
            "Htw-berlin-stoffmuster-ha02-02-001.jpg",
            helper.recid2img("HA.II.02.001")
        )

        self.assertEqual(
            "Htw-berlin-stoffmuster-ha02-02-001-002.jpg",
            helper.recid2img("HA.II.02.001-002")
        )

        with self.assertRaises(ValueError):
            helper.recid2img("HA.II.02")

        with self.assertRaises(ValueError):
            helper.recid2img("HA.II.02.02")

    def test_img2recids(self):
        vol, page, page1, page2 = helper.img2recids(
            "Htw-berlin-stoffmuster-ha02-02-001.jpg")
        self.assertEqual(vol, "HA.II.02")
        self.assertEqual(page, "HA.II.02.001")
        self.assertEqual(page1, None)
        self.assertEqual(page2, None)

        vol, page, page1, page2 = helper.img2recids(
            "Htw-berlin-stoffmuster-ha02-02-001-002.jpg")
        self.assertEqual(vol, "HA.II.02")
        self.assertEqual(page, "HA.II.02.001-002")
        self.assertEqual(page1, "HA.II.02.001")
        self.assertEqual(page2, "HA.II.02.002")

        with self.assertRaises(ValueError):
            helper.img2recids("Htw-berlin-stoffmuster-ha02-02-01.jpg")
