# Corrupt finder

## Usage

`python main.py path.pdf`

or

```python

vals = scan_pdf("some path",no_print=True) # returns and doesn't print
```

## Compile

` pyinstaller main.py      `
or

`pyinstaller main.py   --onefile   `

### Requirements
* poppler (https://poppler.freedesktop.org/)
* `pip install requirements.txt`