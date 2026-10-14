"""The 16.09 estimate reads its inputs from TLY's 16.09 row, nothing else."""
import unittest

from case_study.build_case_study import read_tly_row_1609


def database(*records):
    return {"TLY": {"records": list(records)}}


ROW_1509 = {"Tarih": "15.09.2026", "Fiyat": 1.0, "ToplamDeger": 10.0, "Varliklar": {"Hisse Senedi": 88.39}}
ROW_1609 = {"Tarih": "16.09.2026", "Fiyat": 2.0, "ToplamDeger": 20.0, "Varliklar": {"Hisse Senedi": 87.43}}


class ReadTlyRow1609(unittest.TestCase):
    def test_reads_the_1609_row_not_the_1509_row(self):
        self.assertEqual(read_tly_row_1609(database(ROW_1509, ROW_1609)), (2.0, 20.0, 87.43))

    def test_missing_1609_row_raises(self):
        with self.assertRaises(ValueError):
            read_tly_row_1609(database(ROW_1509))

    def test_missing_equity_share_raises(self):
        row = dict(ROW_1609, Varliklar={"Ters-Repo": 2.7})
        with self.assertRaises(ValueError):
            read_tly_row_1609(database(ROW_1509, row))


if __name__ == "__main__":
    unittest.main()
