Module mutablezip
=================
mutable zip file

Classes
-------

`MutableZipFile(file: Union[str, IO[bytes]], mode: str = 'r', compression: int = 0, allowZip64: bool = False)`
:   Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use MutableZipFile with the 'with statement',
    Upon __exit__ (if updates were applied) a new zip file will override the
        exiting one with the updates
    
    Open the ZIP file with mode read 'r', write 'w', exclusive create 'x',
    or append 'a'.

    ### Ancestors (in MRO)

    * zipfile.ZipFile

    ### Class variables

    `DeleteMarker`
    :   delete marker

    ### Methods

    `removeFile(self, path: Union[str, PathLike[str]])`
    :   flag a file with a delete marker

    `write(self, filename: Union[str, PathLike[str]], arcname: Optional[Union[str, PathLike[str]]] = None, compress_type: Optional[int] = None, compresslevel: Optional[int] = None)`
    :   Put the bytes from filename into the archive under the name
        arcname.

    `writestr(self, zinfo_or_arcname: Union[str, ZipInfo], data: Union[bytes, str], compress_type: Optional[int] = None, compresslevel: Optional[int] = None)`
    :   Write a file into the archive.  The contents is 'data', which
        may be either a 'str' or a 'bytes' instance; if it is a 'str',
        it is encoded as UTF-8 first.
        'zinfo_or_arcname' is either a ZipInfo instance or
        the name of the file in the archive.