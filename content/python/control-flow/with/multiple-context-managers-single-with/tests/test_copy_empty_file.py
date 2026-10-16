def test_copy_empty_file():
    import tempfile, os
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt') as f:
        src = f.name
    dst = src + '_copy.txt'
    try:
        copy_file(src, dst)
        with open(dst, 'r') as f:
            result = f.read()
        assert result == ''
    finally:
        os.unlink(src)
        if os.path.exists(dst):
            os.unlink(dst)
