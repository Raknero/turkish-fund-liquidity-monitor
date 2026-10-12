"""Import and route smoke tests, a safety net for moving files around."""
import importlib
import unittest

MODULES = [
    "terminal.data_scraper",
    "terminal.main",
    "terminal.signals",
    "kap_pipeline.kap_downloader",
    "kap_pipeline.kap_pdf_parser",
    "kap_pipeline.report_dating",
    "kap_pipeline.kap_delta_engine",
    "case_study.build_case_study",
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
        from terminal.main import app

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
