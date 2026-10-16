def test_reads_empty_file():
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp_path = tmp.name
    try:
        assert read_file(tmp_path) == ''
    finally:
        os.unlink(tmp_path)
