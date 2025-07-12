import os
import shutil
import tempfile
from pathlib import Path
import glob
import pandas as pd
import pytest
from difflib import get_close_matches

import hamsoorat  # assume module is named hamsoorat.py

# Helpers to create dummy files

def create_image_files(tmp_path, names, ext_list):
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    files = []
    for name in names:
        for ext in ext_list:
            f = img_dir / f"{name}.{ext}"
            f.write_text("dummy")
            files.append(str(f))
    return str(img_dir), files

# Fixture to setup environment and module reload
@pytest.fixture(autouse=True)
def env_setup(monkeypatch, tmp_path):
    # Create temp XLSX
    input_file = tmp_path / "input.csv"
    df = pd.DataFrame({
        'نام': ['Ali', 'Bob'],
        'نام خانوادگی': ['Rezaei', 'Smith']
    })
    df.to_csv(input_file, index=False)

    output_file = tmp_path / "output.csv"
    img_dir, files = create_image_files(tmp_path, ['Ali-Rezaei'], ['jpg', 'png'])

    monkeypatch.setenv('XLSX_INPUT', str(input_file))
    monkeypatch.setenv('XLSX_OUTPUT', str(output_file))
    monkeypatch.setenv('IMAGE_DIR', img_dir)
    monkeypatch.setenv('IMAGE_EXTENSIONS', 'jpg,png')
    monkeypatch.setenv('FUZZY_MATCH_THRESHOLD', '0.8')

    yield {
        'input': str(input_file),
        'output': str(output_file),
        'img_dir': img_dir,
        'files': files
    }

def test_exact_match_found(env_setup):
    key = 'Ali-Rezaei'
    path = hamsoorat.exact_match(key)
    assert path is not None
    assert Path(path).stem == key

def test_exact_match_missing(env_setup, monkeypatch):
    # No such file
    assert hamsoorat.exact_match('Nonexistent') is None

def test_fuzzy_match(env_setup):
    files = env_setup['files']
    # use a key slightly off
    res = hamsoorat.fuzzy_match('Ali-Rezaey', files)
    assert res is not None
    assert Path(res).stem == 'Ali-Rezaei'

def test_collect_images(env_setup):
    all_files = hamsoorat.collect_images()
    # Should find at least one jpg and one png
    exts = {Path(f).suffix for f in all_files}
    assert '.jpg' in exts and '.png' in exts

@pytest.mark.parametrize("ext", ['.csv', '.xlsx', '.xls'])
def test_read_write_roundtrip(env_setup, ext, tmp_path):
    # Create sample
    data = pd.DataFrame({'A': [1, 2]})
    in_file = tmp_path / f"test{ext}"
    if ext == '.csv':
        data.to_csv(in_file, index=False)
    else:
        data.to_excel(in_file, index=False)

    df = hamsoorat.read_input_file(str(in_file))
    assert 'A' in df.columns

    out_file = tmp_path / f"out{ext}"
    hamsoorat.write_output_file(df, str(out_file))
    assert out_file.exists()

def test_main_executes(env_setup, caplog):
    caplog.set_level('INFO', logger='hamsoorat')
    # Run main
    hamsoorat.main()
    # Output file should exist and have pic_path column
    df = pd.read_csv(env_setup['output'])
    assert 'pic_path' in df.columns
    # Check log messages
    assert 'Hamsoorat - Name-to-Image Matching Tool Started' in caplog.text
    assert 'Matched: Ali-Rezaei' in caplog.text

