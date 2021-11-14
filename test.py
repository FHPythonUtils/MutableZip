#!/usr/bin/env python3.9

""" tests """
from __future__ import annotations

from zipfile import ZIP_DEFLATED, ZipFile

from mutablezip import MutableZipFile

with MutableZipFile("mutable.zip", "a", compression=ZIP_DEFLATED) as zipFile:
	with zipFile.open("foo.txt", "r") as file:
		lines = [line.strip() for line in file.readlines()]
	lines.append(b"new line")
	zipFile.writestr("foo.txt", b"\n".join(lines))

with ZipFile("immutable.zip", "a", compression=ZIP_DEFLATED) as zipFile:
	with zipFile.open("foo.txt", "r") as file:
		lines = [line.strip() for line in file.readlines()]
	lines.append(b"new line")
	zipFile.writestr("foo.txt", b"\n".join(lines))
