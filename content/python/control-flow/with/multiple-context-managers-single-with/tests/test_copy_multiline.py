def test_copy_multiline():
    import tempfile, os
    lines = 'line1\nline2\nline3\n'
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt') as f:
        f.write(lines)
        src = f.name
    dst = src + '_copy.txt'
    try:
        copy_file(src, dst)
        with open(dst, 'r') as f:
            result = f.read()
        assert result == lines
    finally:
        os.unlink(src)
        if os.path.exists(dst):
            os.unlink(dst)
