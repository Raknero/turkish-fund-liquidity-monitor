"""Relative links in tracked Markdown files point at files that exist."""
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def tracked_markdown():
    out = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [REPO_ROOT / line for line in out.splitlines() if line]


def relative_links(md_file):
    in_fence = False
    for number, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for target in LINK.findall(line):
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            yield number, target


class RelativeLinksResolve(unittest.TestCase):
    def test_targets_exist(self):
        files = tracked_markdown()
        self.assertTrue(files)
        for md_file in files:
            for number, target in relative_links(md_file):
                path = target.split("#", 1)[0]
                with self.subTest(file=md_file.relative_to(REPO_ROOT).as_posix(), line=number, link=target):
                    self.assertTrue((md_file.parent / path).exists())


if __name__ == "__main__":
    unittest.main()
