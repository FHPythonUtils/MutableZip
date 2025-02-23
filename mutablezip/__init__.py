"""mutable zip file."""

from __future__ import annotations

import os
from os import PathLike
from pathlib import Path
from shutil import copyfileobj, move, rmtree
from tempfile import TemporaryFile, mkdtemp
from types import TracebackType
from typing import IO, Literal
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from typing_extensions import Self


class MutableZipFile(ZipFile):
	"""
	Add delete (via remove_file) and update (via writestr and write methods)
	To enable update features use MutableZipFile with the 'with statement',
	Upon __exit__ (if updates were applied) a new zip file will override the
	exiting one with the updates.
	"""

	class DeleteMarker:
		"""delete marker."""

	def __init__(
		self,
		file: str | IO[bytes] | os.PathLike,
		mode: Literal["r", "w", "x", "a"] = "r",
		compression: int = ZIP_STORED,
		allowZip64: bool = True,  # noqa: FBT001, FBT002 # Normally, I'd address the boolean
		# typed issue but here we need to maintain compat with ZipFile
		compresslevel: int | None = None,
		*,
		strict_timestamps: bool = True,
	) -> None:
		"""Open a ZIP file, where file can be a path to a file (a string), a
		file-like object or a path-like object.

		:param str | IO[bytes] | os.PathLike file: can be a path to a file (a string), a
		file-like object or a path-like object.
		:param Literal["r", "w", "x", "a"] mode: parameter should be 'r' to read an
		existing file, 'w' to truncate and write a new file, 'a' to append to an existing
		file, or 'x' to exclusively create and write a new file
		:param int compression: the ZIP compression method to use when writing the
		archive, and should be ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2 or ZIP_LZMA
		:param bool allowZip64: s True (the default) zipfile will create ZIP files
		that use the ZIP64 extensions when the zipfile is larger than 4 GiB.
		:param int | None compresslevel: controls the compression level to use when
		writing files to the archive. When using ZIP_STORED or ZIP_LZMA it has no effect.
		When using ZIP_DEFLATED integers 0 through 9 are accepted
		:param bool strict_timestamps: when set to False, allows to zip files older than
		1980-01-01 and newer than 2107-12-31, defaults to True

		https://docs.python.org/3/library/zipfile.html
		"""
		super().__init__(
			file,
			mode=mode,
			compression=compression,
			allowZip64=allowZip64,
			compresslevel=compresslevel,
			strict_timestamps=strict_timestamps,
		)
		# track file to override in zip
		self._replace = {}
		# Whether the with statement was called
		self._allowUpdates = False
		# Let's set some properties here - though there 'shouldn't' be a need
		# for this
		self.file = file
		self.mode = mode
		self.compression = compression
		self.allowZip64 = allowZip64

	def writestr(
		self,
		zinfo_or_arcname: str | ZipInfo,
		data: bytes | str,
		compress_type: int | None = None,
		compresslevel: int | None = None,
	) -> None:
		"""Write a file into the archive. The contents is data, which may be either a
		str or a bytes instance; if it is a str, it is encoded as UTF-8 first.

		zinfo_or_arcname is either the file name it will be given in the archive, or a
		ZipInfo instance. If it's an instance, at least the filename, date, and time
		must be given. If it's a name, the date and time is set to the current date and
		time. The archive must be opened with mode 'w', 'x' or 'a'.
		"""
		if isinstance(zinfo_or_arcname, ZipInfo):
			name = zinfo_or_arcname.filename
		else:
			name = zinfo_or_arcname
		# If the file exits, and needs to be overridden,
		# mark the entry, and create a temp-file for it
		# we allow this only if the with statement is used
		if self._allowUpdates and name in self.namelist():
			tempFile = self._replace.setdefault(name, TemporaryFile())
			if isinstance(data, str):
				tempFile.write(data.encode("utf-8"))  # strings are unicode
			else:
				tempFile.write(data)
		# Otherwise just act normally
		else:
			super().writestr(
				zinfo_or_arcname,
				data,
				compress_type=compress_type,
				compresslevel=compresslevel,
			)

	def write(
		self,
		filename: str | PathLike[str],
		arcname: str | PathLike[str] | None = None,
		compress_type: int | None = None,
		compresslevel: int | None = None,
	) -> None:
		"""Write the file named filename to the archive, giving it the archive name
		arcname (by default, this will be the same as filename, but without a drive
		letter and with leading path separators removed). If given, compress_type
		overrides the value given for the compression parameter to the constructor
		for the new entry. Similarly, compresslevel will override the constructor if
		given. The archive must be open with mode 'w', 'x' or 'a'.

		"""
		arcname = arcname or filename
		# If the file exits, and needs to be overridden,
		# mark the entry, and create a temp-file for it
		# we allow this only if the with statement is used
		if self._allowUpdates and arcname in self.namelist():
			with TemporaryFile() as tempFile, Path(filename).open("rb") as source:
				copyfileobj(source, tempFile)

		# Behave normally
		else:
			super().write(
				filename,
				arcname=arcname,
				compress_type=compress_type,
				compresslevel=compresslevel,
			)

	def __enter__(self) -> Self:
		# Allow updates
		self._allowUpdates = True
		return self

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_val: BaseException | None,
		exc_tb: TracebackType | None,
	) -> None:
		# Call base to close zip
		try:
			super().__exit__(exc_type, exc_val, exc_tb)
			if len(self._replace) > 0:
				self._rebuildZip()
		finally:
			# Release all the temp files regardless of success
			self._closeAllTempFiles()
			self._allowUpdates = False

	def _closeAllTempFiles(self) -> None:
		"""Close all temporary files."""
		for tempFile in self._replace.values():
			if hasattr(tempFile, "close"):
				tempFile.close()

	def removeFile(self, path: str | PathLike[str]) -> None:
		"""Flag a file with a delete marker."""
		self._replace[path] = self.DeleteMarker()

	def _rebuildZip(self) -> None:
		tempdir = mkdtemp()
		try:
			tempZipPath = Path(tempdir) / "new.zip"
			with ZipFile(self.file, "r") as zipRead, ZipFile(
				tempZipPath,
				"w",
				compression=self.compression,
				allowZip64=self.allowZip64,
			) as zipWrite:
				for item in zipRead.infolist():
					# Check if the file should be replaced / or deleted
					replacement = self._replace.get(item.filename, None)
					# If marked for deletion, do not copy file to new zipfile
					if isinstance(replacement, self.DeleteMarker):
						del self._replace[item.filename]
						continue
					# If marked for replacement, copy temp_file, instead of old file
					if replacement is not None:
						del self._replace[item.filename]
						# Write replacement to archive,
						# and then close it ,deleting the temp file
						replacement.seek(0)
						data = replacement.read()
						replacement.close()
					else:
						data = zipRead.read(item.filename)
					zipWrite.writestr(item, data)
			# Override the archive with the updated one
			if isinstance(self.file, str):
				move(tempZipPath.as_posix(), self.file)
			elif hasattr(self.file, "name"):
				move(tempZipPath.as_posix(), self.file.name)
			elif hasattr(self.file, "write"):
				self.file.write(tempZipPath.read_bytes())
			else:
				msg = f"Sorry but {type(self.file).__name__} is not supported at this time!"
				raise RuntimeError(msg)
		finally:
			rmtree(tempdir)
