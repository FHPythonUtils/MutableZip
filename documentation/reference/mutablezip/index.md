# Mutablezip

[Mutablezip Index](../README.md#mutablezip-index) /
Mutablezip

> Auto-generated documentation for [mutablezip](../../../mutablezip/__init__.py) module.

- [Mutablezip](#mutablezip)
  - [MutableZipFile](#mutablezipfile)
    - [MutableZipFile().removeFile](#mutablezipfile()removefile)
    - [MutableZipFile().write](#mutablezipfile()write)
    - [MutableZipFile().writestr](#mutablezipfile()writestr)

## MutableZipFile

[Show source in __init__.py:13](../../../mutablezip/__init__.py#L13)

Add delete (via remove_file) and update (via writestr and write methods)
To enable update features use MutableZipFile with the 'with statement',
Upon __exit__ (if updates were applied) a new zip file will override the
exiting one with the updates

#### Signature

```python
class MutableZipFile(ZipFile):
    def __init__(
        self,
        file: str | IO[bytes],
        mode: Literal["r", "w", "x", "a"] = "r",
        compression: int = ZIP_STORED,
        allowZip64: bool = False,
    ): ...
```

### MutableZipFile().removeFile

[Show source in __init__.py:117](../../../mutablezip/__init__.py#L117)

flag a file with a delete marker

#### Signature

```python
def removeFile(self, path: str | PathLike[str]): ...
```

### MutableZipFile().write

[Show source in __init__.py:69](../../../mutablezip/__init__.py#L69)

#### Signature

```python
def write(
    self,
    filename: str | PathLike[str],
    arcname: str | PathLike[str] | None = None,
    compress_type: int | None = None,
    compresslevel: int | None = None,
): ...
```

### MutableZipFile().writestr

[Show source in __init__.py:43](../../../mutablezip/__init__.py#L43)

#### Signature

```python
def writestr(
    self,
    zinfo_or_arcname: str | ZipInfo,
    data: bytes | str,
    compress_type: int | None = None,
    compresslevel: int | None = None,
): ...
```