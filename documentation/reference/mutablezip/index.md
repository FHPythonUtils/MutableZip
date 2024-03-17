# Mutablezip

[Mutablezip Index](../README.md#mutablezip-index) / Mutablezip

> Auto-generated documentation for [mutablezip](../../../mutablezip/__init__.py) module.

- [Mutablezip](#mutablezip)
  - [MutableZipFile](#mutablezipfile)
    - [MutableZipFile()._closeAllTempFiles](#mutablezipfile()_closealltempfiles)
    - [MutableZipFile().removeFile](#mutablezipfile()removefile)
    - [MutableZipFile().write](#mutablezipfile()write)
    - [MutableZipFile().writestr](#mutablezipfile()writestr)

## MutableZipFile

[Show source in __init__.py:14](../../../mutablezip/__init__.py#L14)

Add delete (via remove_file) and update (via writestr and write methods)
To enable update features use MutableZipFile with the 'with statement',
Upon __exit__ (if updates were applied) a new zip file will override the
exiting one with the updates.

#### Signature

```python
class MutableZipFile(ZipFile):
    def __init__(
        self,
        file: str | IO[bytes],
        mode: Literal["r", "w", "x", "a"] = "r",
        compression: int = ZIP_STORED,
        allowZip64: bool = False,
    ) -> None: ...
```

### MutableZipFile()._closeAllTempFiles

[Show source in __init__.py:118](../../../mutablezip/__init__.py#L118)

Close all temporary files.

#### Signature

```python
def _closeAllTempFiles(self) -> None: ...
```

### MutableZipFile().removeFile

[Show source in __init__.py:124](../../../mutablezip/__init__.py#L124)

Flag a file with a delete marker.

#### Signature

```python
def removeFile(self, path: str | PathLike[str]) -> None: ...
```

### MutableZipFile().write

[Show source in __init__.py:73](../../../mutablezip/__init__.py#L73)

#### Signature

```python
def write(
    self,
    filename: str | PathLike[str],
    arcname: str | PathLike[str] | None = None,
    compress_type: int | None = None,
    compresslevel: int | None = None,
) -> None: ...
```

### MutableZipFile().writestr

[Show source in __init__.py:44](../../../mutablezip/__init__.py#L44)

#### Signature

```python
def writestr(
    self,
    zinfo_or_arcname: str | ZipInfo,
    data: bytes | str,
    compress_type: int | None = None,
    compresslevel: int | None = None,
) -> None: ...
```