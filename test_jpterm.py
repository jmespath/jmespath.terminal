"""Regression tests for jpterm input-file handling."""
import sys

import jpterm


def test_load_input_json_missing_file_raises_oserror(tmp_path):
    missing = tmp_path / 'does-not-exist.json'
    try:
        jpterm._load_input_json(str(missing))
    except OSError:
        pass
    else:
        raise AssertionError('expected OSError for a missing input file')


def test_main_missing_file_reports_clean_error(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['jpterm', 'does-not-exist.json'])
    rc = jpterm.main()
    assert rc == 1
    captured = capsys.readouterr()
    assert 'Unable to load the input JSON' in captured.err
    assert 'Traceback' not in captured.err
