"""Sort the files in a folder into subfolders by file type.

Only files directly inside the folder are moved. Subfolders and hidden files
(names starting with '.') are left alone. Every run writes an undo log, so
the last run can be reversed.
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "PDF_Files": [".pdf"],
    "Word_Documents": [".doc", ".docx"],
    "Text_Files": [".txt", ".md"],
    "Presentations": [".ppt", ".pptx"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Images_JPEG": [".jpg", ".jpeg"],
    "Images_PNG": [".png"],
    "Images_SVG": [".svg"],
    "Images_GIF": [".gif"],
    "Images_WEBP": [".webp"],
    "Images_RAW": [".raw", ".nef", ".cr2"],
    "Code_Python": [".py"],
    "Code_JavaScript": [".js"],
    "Code_HTML": [".html"],
    "Code_CSS": [".css"],
    "Code_C_CPP": [".c", ".cpp", ".h"],
    "Code_Java": [".java"],
    "Code_Go": [".go"],
    "Code_Rust": [".rs"],
    "Code_SQL": [".sql"],
    "Code_Shell": [".sh"],
    "Data_JSON": [".json"],
    "Data_YAML": [".yml", ".yaml"],
    "Data_XML": [".xml"],
    "Config_Files": [".ini", ".cfg", ".conf"],
    "Log_Files": [".log"],
    "Video_MP4": [".mp4"],
    "Video_MKV": [".mkv"],
    "Video_MOV": [".mov"],
    "Audio_MP3": [".mp3"],
    "Audio_WAV": [".wav"],
    "Audio_FLAC": [".flac"],
    "Archives_ZIP": [".zip"],
    "Archives_RAR": [".rar"],
    "Archives_7Z": [".7z"],
    "Archives_TAR": [".tar"],
    "Archives_GZ": [".gz"],
    "Executables_EXE": [".exe"],
    "Installers_DMG": [".dmg"],
    "Installers_PKG": [".pkg"],
    "Installers_MSI": [".msi"],
    "Fonts_TTF": [".ttf"],
    "Fonts_OTF": [".otf"],
    "No_Extension": [""],
}
OTHER = "Other"
UNDO_LOG = ".organizer_undo.json"

FOLDER_FOR_EXTENSION = {ext: folder for folder, exts in CATEGORIES.items() for ext in exts}


def category_for(path):
    return FOLDER_FOR_EXTENSION.get(Path(path).suffix.lower(), OTHER)


def unique_path(path, taken=()):
    """`path`, or `name_1.ext`, `name_2.ext`, ... if that name is already used."""
    candidate, n = path, 1
    while candidate.exists() or candidate in taken:
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
        n += 1
    return candidate


def plan(folder):
    """Work out every move as (source, destination) pairs without touching anything."""
    folder = Path(folder)
    moves, taken = [], set()
    for f in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not f.is_file() or f.name.startswith("."):
            continue
        destination = unique_path(folder / category_for(f) / f.name, taken)
        taken.add(destination)
        moves.append((f, destination))
    return moves


def apply(folder, moves):
    """Carry out the moves and record them in the undo log."""
    folder = Path(folder)
    done = []
    for source, destination in moves:
        destination.parent.mkdir(exist_ok=True)
        shutil.move(str(source), str(destination))
        done.append({"from": source.name, "to": str(destination.relative_to(folder))})
    log = {"time": datetime.now().isoformat(timespec="seconds"), "moves": done}
    (folder / UNDO_LOG).write_text(json.dumps(log, indent=2))
    return len(done)


def undo(folder):
    """Move everything from the last run back. Returns how many files were restored."""
    folder = Path(folder)
    log_path = folder / UNDO_LOG
    if not log_path.exists():
        raise FileNotFoundError(f"nothing to undo in {folder}")
    moves = json.loads(log_path.read_text())["moves"]

    restored = 0
    for m in reversed(moves):
        current, original = folder / m["to"], folder / m["from"]
        if current.exists() and not original.exists():
            shutil.move(str(current), str(original))
            restored += 1
    # remove category folders that are now empty
    for parent in {(folder / m["to"]).parent for m in moves}:
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()
    log_path.unlink()
    return restored
