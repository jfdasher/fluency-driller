def test_reads_content():
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write('hello world')
        tmp_path = tmp.name
    try:
        assert read_file(tmp_path) == 'hello world'
    finally:
        os.unlink(tmp_path)
