#!/usr/bin/env python3
"""Copy the public website into site-dist without source, notes, or credentials."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "site-dist"
PUBLIC_SUFFIXES = {".html", ".css", ".js", ".svg", ".ico", ".webmanifest"}
PUBLIC_NAMES = {".nojekyll", "_headers", "_redirects", "robots.txt", "CNAME"}
MAX_ASSET_BYTES = 25 * 1024 * 1024


def build():
    if not (ROOT / "index.html").is_file():
        raise SystemExit("Missing index.html in the project root.")
    if DEST.is_symlink():
        raise SystemExit("Refusing to replace a symlink at site-dist.")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()

    source_files = [
        path for path in ROOT.iterdir()
        if path.is_file() and (path.suffix in PUBLIC_SUFFIXES or path.name in PUBLIC_NAMES)
    ]
    if (ROOT / "assets").is_dir():
        source_files.extend(path for path in (ROOT / "assets").rglob("*") if path.is_file())

    copied = 0
    for source in sorted(source_files):
        if source.is_symlink():
            raise SystemExit(f"Public files must not be symlinks: {source.relative_to(ROOT)}")
        if source.name == ".DS_Store" or source.name.startswith(".") and source.name not in PUBLIC_NAMES:
            continue
        if source.stat().st_size > MAX_ASSET_BYTES:
            raise SystemExit(f"Cloudflare Pages' 25 MiB file limit exceeded: {source.relative_to(ROOT)}")
        target = DEST / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied += 1
    print(f"Prepared {copied} public files in {DEST.name}/")


if __name__ == "__main__":
    build()
