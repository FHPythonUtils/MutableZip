# Mutablezip

> Auto-generated documentation for [mutablezip](../../../mutablezip/__init__.py) module.

mutable zip file

- [Mutablezip](../README.md#mutablezip-index) / [Modules](../MODULES.md#mutablezip-modules) / Mutablezip
    - [MutableZipFile](#mutablezipfile)
        - [MutableZipFile().removeFile](#mutablezipfileremovefile)
        - [MutableZipFile().write](#mutablezipfilewrite)
        - [MutableZipFile().writestr](#mutablezipfilewritestr)

## MutableZipFile

[[find in source code]](../../../mutablezip/__init__.py#L13)

```python
class MutableZipFile(ZipFile):
    def __init__(
        file: str | IO[bytes],
        mode: Literal['r', 'w', 'x', 'a'] = 'r',
        compression: int = ZIP_STORED,
        allowZip64: bool = False,
    ):
```

Add delete (via remove_file) and update (via writestr and write methods)
To enable update features use MutableZipFile with the 'with statement',
Upon __exit__ (if updates were applied) a new zip file will override the
exiting one with the updates

### MutableZipFile().removeFile

[[find in source code]](../../../mutablezip/__init__.py#L117)

```python
def removeFile(path: str | PathLike[str]):
```

flag a file with a delete marker

### MutableZipFile().write

[[find in source code]](../../../mutablezip/__init__.py#L69)

```python
def write(
    filename: str | PathLike[str],
    arcname: str | PathLike[str] | None = None,
    compress_type: int | None = None,
    compresslevel: int | None = None,
):
```

### MutableZipFile().writestr

[[find in source code]](../../../mutablezip/__init__.py#L43)

```python
def writestr(
    zinfo_or_arcname: str | ZipInfo,
    data: bytes | str,
    compress_type: int | None = None,
    compresslevel: int | None = None,
):
```
