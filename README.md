# FCS3toCSV
Extract data records from FCS3.0 format file and save as CSV format file.

I have confirmed the work of this program by using the following:

* Test data of [FCSExtract Utility](http://research.stowers-institute.org/mcm/efg/ScientificSoftware/Utility/FCSExtract/index.htm)
* Exported data from [Sony ec800](http://www.sonybiotechnology.com/ec800_overview.php)

## Requirements

* Python 3.4.x

## How to use

```
python main.py /path/to/file_or_dir
```

## .EXE for Windows
* .exe package is available at `./dist/FSC3toCSV.exe`
* Drag and drop a FCS3.0 file (`.fcs`) or directory into main.exe
* This package is complied on Windows 7 with python 3.4.3 and py2exe

### How to compile yourself
* Install latest python 3.4 from official site and py2exe from pip
* Run `setup.py` as below:

```
python setup.py
```

* `FCS3toCSV.exe` will be built into `./dist/`
