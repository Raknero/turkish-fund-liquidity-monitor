"""TEFAS distribution codes mapped to asset names, without losing values."""
import contextlib
import io
import unittest
from unittest import mock

from terminal import data_scraper
from terminal.data_scraper import build_distribution_map

# TP2's raw dagilimSiraliGetirT row for 31.08.2026, trimmed.
TP2_0831 = {"fonKodu": "TP2", "tarih": "2026-08-31", "bpp": 14.65, "tpp": 0.02, "tr": 63.76}


class MoneyMarketCodes(unittest.TestCase):
    def test_bpp_and_tpp_stay_separate(self):
        varliklar = build_distribution_map([TP2_0831])["31.08.2026"]
        self.assertEqual(varliklar["Borsa İstanbul Para Piyasası"], 14.65)
        self.assertEqual(varliklar["Takasbank Para Piyasası"], 0.02)
        self.assertAlmostEqual(sum(varliklar.values()), 14.65 + 0.02 + 63.76)


class SameNameCollision(unittest.TestCase):
    def test_values_are_summed(self):
        record = {"tarih": "2026-08-31", "hs": 10.0, "xx": 2.5}
        with mock.patch.dict(data_scraper.TEFAS_DISTRIBUTION_MAP, {"xx": "Hisse Senedi"}):
            with contextlib.redirect_stdout(io.StringIO()) as log:
                varliklar = build_distribution_map([record])["31.08.2026"]
        self.assertEqual(varliklar, {"Hisse Senedi": 12.5})
        self.assertIn("[UYARI]", log.getvalue())


if __name__ == "__main__":
    unittest.main()
