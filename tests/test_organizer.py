from pathlib import Path

import pytest

import organizer


def make(folder, *names):
    for name in names:
        (folder / name).write_text(name)


def tree(folder):
    """Every file under `folder`, as sorted relative paths."""
    return sorted(str(p.relative_to(folder)).replace("\\", "/") for p in folder.rglob("*") if p.is_file())


def test_categories():
    assert organizer.category_for("report.pdf") == "PDF_Files"
    assert organizer.category_for("PHOTO.JPG") == "Images_JPEG"  # extensions are case-insensitive
    assert organizer.category_for("Makefile") == "No_Extension"
    assert organizer.category_for("weird.xyz") == "Other"


def test_plan_does_not_touch_anything(tmp_path):
    make(tmp_path, "a.pdf", "b.png")
    moves = organizer.plan(tmp_path)
    assert [(s.name, d.parent.name) for s, d in moves] == [("a.pdf", "PDF_Files"), ("b.png", "Images_PNG")]
    assert tree(tmp_path) == ["a.pdf", "b.png"]


def test_apply_sorts_files(tmp_path):
    make(tmp_path, "a.pdf", "b.png", "notes.txt", "c.xyz")
    organizer.apply(tmp_path, organizer.plan(tmp_path))
    assert tree(tmp_path) == [".organizer_undo.json", "Images_PNG/b.png", "Other/c.xyz",
                              "PDF_Files/a.pdf", "Text_Files/notes.txt"]


def test_never_overwrites_existing_files(tmp_path):
    (tmp_path / "PDF_Files").mkdir()
    (tmp_path / "PDF_Files" / "a.pdf").write_text("old")
    make(tmp_path, "a.pdf")
    organizer.apply(tmp_path, organizer.plan(tmp_path))
    assert (tmp_path / "PDF_Files" / "a.pdf").read_text() == "old"
    assert (tmp_path / "PDF_Files" / "a_1.pdf").read_text() == "a.pdf"


def test_hidden_files_and_subfolders_are_left_alone(tmp_path):
    make(tmp_path, ".hidden.pdf")
    (tmp_path / "project").mkdir()
    make(tmp_path / "project", "inner.pdf")
    assert organizer.plan(tmp_path) == []


def test_undo_restores_everything(tmp_path):
    make(tmp_path, "a.pdf", "b.png", "c.xyz")
    (tmp_path / "PDF_Files").mkdir()
    make(tmp_path / "PDF_Files", "a.pdf")  # forces a rename
    before = tree(tmp_path)

    organizer.apply(tmp_path, organizer.plan(tmp_path))
    assert organizer.undo(tmp_path) == 3
    assert tree(tmp_path) == before
    assert not (tmp_path / "Images_PNG").exists()  # emptied folders are removed
    assert (tmp_path / "PDF_Files").exists()        # folders that still hold files stay


def test_undo_without_a_run(tmp_path):
    with pytest.raises(FileNotFoundError):
        organizer.undo(tmp_path)
