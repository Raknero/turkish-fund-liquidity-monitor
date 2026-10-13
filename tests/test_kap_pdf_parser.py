"""Equities-section markers in the KAP PDF parser, tested on table rows."""
import unittest

from kap_pipeline.kap_pdf_parser import KAPPdfParser


class SectionMarkers(unittest.TestCase):
    def test_group_total_split_across_cells_ends_section(self):
        self.assertTrue(KAPPdfParser._is_section_end(["GRUP", "TOPLAMI", "1,00"]))

    def test_group_total_in_one_cell_ends_section(self):
        self.assertTrue(KAPPdfParser._is_section_end(["GRUP TOPLAMI", "1,00"]))

    def test_split_equities_heading_starts_section(self):
        self.assertTrue(KAPPdfParser._is_section_start(["HİSSE SENETL", "ERİ"]))

    def test_holding_row_is_neither(self):
        row = ["DSTKF", "TL", "", "", "", "27.025.777,00"]
        self.assertFalse(KAPPdfParser._is_section_start(row))
        self.assertFalse(KAPPdfParser._is_section_end(row))


if __name__ == "__main__":
    unittest.main()
