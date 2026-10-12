"""Import and route smoke tests, a safety net for moving files around."""
import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "kap_pdf_downloader"))
sys.path.insert(0, str(ROOT / "case_study"))

MODULES = [
    "data_scraper",
    "main",
    "signals",
    "kap_downloader",
    "kap_pdf_parser",
    "report_dating",
    "kap_delta_engine",
    "build_case_study",
]


class ModulesImport(unittest.TestCase):
    def test_every_module_imports(self):
        for name in MODULES:
            with self.subTest(module=name):
                importlib.import_module(name)


class AppRoutes(unittest.TestCase):
    # Routes are read from app.routes; TestClient is never opened as a
    # context manager, so lifespan (and its TEFAS refresh) never runs.
    def test_api_routes_exist(self):
        from main import app

        routes = {
            (route.path, method)
            for route in app.routes
            for method in getattr(route, "methods", None) or ()
        }
        for expected in [
            ("/api/add-fund", "POST"),
            ("/api/remove-fund", "POST"),
            ("/api/hard-delete-fund", "DELETE"),
            ("/fund_database.json", "GET"),
        ]:
            with self.subTest(route=expected):
                self.assertIn(expected, routes)


if __name__ == "__main__":
    unittest.main()
