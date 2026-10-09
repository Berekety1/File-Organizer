# File Organizer

A command-line tool that tidies up a messy folder (Downloads, Desktop, …) by sorting its files into subfolders by type. It shows you the plan first, never overwrites anything, and can undo the last run.

```
$ python main.py ~/Downloads
Found 11 files to organise in /Users/me/Downloads

Audio_MP3/ (1)
  song.mp3
Images_JPEG/ (1)
  photo.JPG
PDF_Files/ (2)
  Lecture 3.pdf
  report.pdf  ->  report_1.pdf (renamed, name already taken)
Spreadsheets/ (1)
  data.csv
...

Move 11 files? (y/n): y
Moved 11 files. Run again with --undo to put them back.
```

## Usage

```bash
python main.py ~/Downloads             # show the plan, then ask before moving
python main.py ~/Downloads --dry-run   # only show the plan
python main.py ~/Downloads --yes       # move without asking
python main.py ~/Downloads --undo      # put everything from the last run back
python main.py                         # asks which folder to organise
```

It needs only the Python standard library (Python 3.9+).

## How it works

- **Sorting by extension.** More than 40 file types are sorted into folders such as `PDF_Files`, `Images_PNG`, `Code_Python`, `Video_MP4` and `Archives_ZIP` (the full list is at the top of [`organizer.py`](organizer.py)). Extensions are matched case-insensitively, files without an extension go to `No_Extension`, and unknown types go to `Other`.
- **Nothing is overwritten.** If the destination already has a file with the same name, the new one is saved as `name_1.ext`, `name_2.ext`, and so on.
- **Safe defaults.** Only files directly inside the folder are moved. Subfolders and hidden files (such as `.DS_Store`) are left alone.
- **Undo.** Each run saves its moves to `.organizer_undo.json` inside the folder. `--undo` moves every file back and removes any folders it left empty.

## Tests

```bash
pip install pytest
python -m pytest
```

## Project structure

```
organizer.py              planning, moving and undo logic
main.py                   command-line interface
tests/test_organizer.py   tests (run in temporary folders)
```
