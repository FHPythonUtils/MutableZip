""" mutable zip file """
from __future__ import annotations
from types import TracebackType
from typing import Optional, Union, IO, Type
from zipfile import ZipFile, ZIP_STORED, ZipInfo
from shutil import move, rmtree, copyfileobj
from tempfile import mkdtemp, TemporaryFile
from os import PathLike
from os.path import join


class MutableZipFile(ZipFile):
	"""
    Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use MutableZipFile with the 'with statement',
    Upon __exit__ (if updates were applied) a new zip file will override the
	exiting one with the updates
    """
	class DeleteMarker:
		""" delete marker """

	def __init__(self, file: Union[str, IO[bytes]], mode: str="r",
	compression: int=ZIP_STORED, allowZip64: bool=False):
		super().__init__(file, mode=mode,
		compression=compression, allowZip64=allowZip64)
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

	def writestr(self, zinfo_or_arcname: Union[str, ZipInfo], data: Union[bytes, str],
	compress_type: Optional[int]=None, compresslevel: Optional[int]=None):
		if isinstance(zinfo_or_arcname, ZipInfo):
			name = zinfo_or_arcname.filename
		else:
			name = zinfo_or_arcname
		# If the file exits, and needs to be overridden,
		# mark the entry, and create a temp-file for it
		# we allow this only if the with statement is used
		if self._allowUpdates and name in self.namelist():
			tempFile = self._replace[name] = self._replace.get(name, TemporaryFile())
			if isinstance(data, str):
				tempFile.write(data.encode("utf-8")) # strings are unicode
			else:
				tempFile.write(data)
		# Otherwise just act normally
		else:
			super().writestr(zinfo_or_arcname, data,
			compress_type=compress_type, compresslevel=compresslevel)

	def write(self, filename: Union[str, PathLike[str]],
	arcname: Optional[Union[str, PathLike[str]]]=None, compress_type: Optional[int]=None,
	compresslevel: Optional[int]=None):
		arcname = arcname or filename
		# If the file exits, and needs to be overridden,
		# mark the entry, and create a temp-file for it
		# we allow this only if the with statement is used
		if self._allowUpdates and arcname in self.namelist():
			tempFile = self._replace[
			arcname] = self._replace.get(arcname, TemporaryFile())
			with open(filename, "rb") as source:
				copyfileobj(source, tempFile)
		# Behave normally
		else:
			super().write(filename, arcname=arcname,
			compress_type=compress_type, compresslevel=compresslevel)

	def __enter__(self):
		# Allow updates
		self._allowUpdates = True
		return self

	def __exit__(self, exc_type: Optional[Type[BaseException]],
	exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]):
		# Call base to close zip
		try:
			super().__exit__(exc_type, exc_val, exc_tb)
			if len(self._replace) > 0:
				self._rebuildZip()
		finally:
			# Release all the temp files regardless of success
			self._closeAllTempFiles()
			self._allowUpdates = False

	def _closeAllTempFiles(self):
		""" close all temporary files """
		for tempFile in self._replace.values():
			if hasattr(tempFile, 'close'):
				tempFile.close()

	def removeFile(self, path: Union[str, PathLike[str]]):
		""" flag a file with a delete marker """
		self._replace[path] = self.DeleteMarker()

	def _rebuildZip(self):
		tempdir = mkdtemp()
		try:
			tempZipPath = join(tempdir, 'new.zip')
			with ZipFile(self.file, 'r') as zipRead:
				# Create new zip with assigned properties
				with ZipFile(tempZipPath, 'w', compression=self.compression,
				allowZip64=self.allowZip64) as zipWrite:
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
							# and then close it (deleting the temp file)
							replacement.seek(0)
							data = replacement.read()
							replacement.close()
						else:
							data = zipRead.read(item.filename)
						zipWrite.writestr(item, data)
			# Override the archive with the updated one
			if isinstance(self.file, str):
				move(tempZipPath, self.file)
			else:
				move(tempZipPath, self.file.name)
		finally:
			rmtree(tempdir)
