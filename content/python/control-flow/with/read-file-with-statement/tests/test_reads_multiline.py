def test_reads_multiline():
    import tempfile, os
    content = 'line1\nline2\nline3'
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        assert read_file(tmp_path) == content
    finally:
        os.unlink(tmp_path)
