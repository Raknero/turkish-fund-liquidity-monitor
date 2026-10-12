"""Import and route smoke tests, a safety net for moving files around."""
import importlib
import unittest
from pathlib import Path

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


class StaticFilesOnly(unittest.TestCase):
    # Only terminal/static/ is served; nothing else in the repo is reachable.
    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient

        from terminal.main import app

        cls.client = TestClient(app)

    def test_dashboard_served(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_repo_files_not_served(self):
        for path in [
            "/INTERNAL_ARCHITECTURE.md",
            "/case_study/private/trades.json",
            "/main.py",
        ]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)


class DataPaths(unittest.TestCase):
    def test_database_under_data_dir(self):
        from terminal import data_scraper

        repo_root = Path(__file__).resolve().parents[1]
        self.assertEqual(Path(data_scraper.DATABASE_FILE).parent, repo_root / "data")


if __name__ == "__main__":
    unittest.main()
