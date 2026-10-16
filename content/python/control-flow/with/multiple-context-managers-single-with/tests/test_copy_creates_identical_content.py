def test_copy_creates_identical_content():
    import tempfile, os
    content = 'hello\nworld\n'
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt') as f:
        f.write(content)
        src = f.name
    dst = src + '_copy.txt'
    try:
        copy_file(src, dst)
        with open(dst, 'r') as f:
            result = f.read()
        assert result == content
    finally:
        os.unlink(src)
        if os.path.exists(dst):
            os.unlink(dst)
