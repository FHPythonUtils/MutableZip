#!/usr/bin/env python3.9

"""tests"""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

THISDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THISDIR.parent))

from mutablezip import MutableZipFile


def test_MutableZipFile() -> None:
	with MutableZipFile(f"{THISDIR}/data/mutable.zip", "a", compression=ZIP_DEFLATED) as zipFile:
		with zipFile.open("foo.txt", "r") as file:
			lines = [line.strip() for line in file.readlines()]
		lines.append(b"new line")
		zipFile.writestr("foo.txt", b"\n".join(lines))
	with ZipFile(f"{THISDIR}/data/mutable.zip", "r") as zipFile:
		assert len(zipFile.namelist()) == 1


def test_ZipFile() -> None:
	with ZipFile(f"{THISDIR}/data/immutable.zip", "a", compression=ZIP_DEFLATED) as zipFile:
		with zipFile.open("foo.txt", "r") as file:
			lines = [line.strip() for line in file.readlines()]
		lines.append(b"new line")
		zipFile.writestr("foo.txt", b"\n".join(lines))
	with ZipFile(f"{THISDIR}/data/immutable.zip", "r") as zipFile:
		assert len(zipFile.namelist()) > 1
