<a name=".make"></a>
## make

Makefile for python. Run one of the following subcommands:

install: Poetry install
build: Building docs, requirements.txt, setup.py, poetry build

<a name=".mutablezip"></a>
## mutablezip

mutable zip file

<a name=".mutablezip.MutableZipFile"></a>
### MutableZipFile

```python
class MutableZipFile(ZipFile):
 |  MutableZipFile(file, mode="r", compression=ZIP_STORED, allowZip64=False)
```

Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use MutableZipFile with the 'with statement',
    Upon __exit__ (if updates were applied) a new zip file will override the
	exiting one with the updates

<a name=".mutablezip.MutableZipFile.DeleteMarker"></a>
### DeleteMarker

```python
class DeleteMarker()
```

delete marker

<a name=".mutablezip.MutableZipFile.__enter__"></a>
#### \_\_enter\_\_

```python
 | __enter__()
```

Allow updates

<a name=".mutablezip.MutableZipFile.__exit__"></a>
#### \_\_exit\_\_

```python
 | __exit__(exc_type, exc_val, exc_tb)
```

Call base to close zip

<a name=".mutablezip.MutableZipFile.removeFile"></a>
#### removeFile

```python
 | removeFile(path)
```

flag a file with a delete marker

