from drill._runner import run_tests


def _ns(src):
    ns = {}
    exec(src, ns)
    return ns


def test_passing_test_counts_as_passed():
    ns = _ns("def make(f):\n    return lambda x: x * f")
    tests = [{"name": "t1", "source": "def test_a():\n    assert make(3)(5) == 15"}]
    out = run_tests(ns, "make", tests)
    assert out == {"passed": 1, "failed": 0, "detail": []}


def test_failing_assert_reports_reason():
    ns = _ns("def make(f):\n    return lambda x: x * f")
    tests = [{"name": "t1", "source": "def test_a():\n    assert make(3)(5) == 999"}]
    out = run_tests(ns, "make", tests)
    assert out["passed"] == 0 and out["failed"] == 1
    assert out["detail"][0]["name"] == "test_a"
    assert "AssertionError" in out["detail"][0]["reason"]


def test_fn_alias_and_equal_helper_available():
    ns = _ns("def make(f):\n    return lambda x: x * f")
    tests = [
        {
            "name": "t1",
            "source": "def test_a():\n    assert fn(2)(10) == 20 and equal((1, 2), [1, 2])",
        }
    ]
    out = run_tests(ns, "make", tests)
    assert out["failed"] == 0


def test_exception_in_test_is_a_failure_with_reason():
    ns = _ns("def make(f):\n    return lambda x: x * f")
    tests = [{"name": "t1", "source": "def test_a():\n    make(3).nope"}]
    out = run_tests(ns, "make", tests)
    assert out["failed"] == 1 and "AttributeError" in out["detail"][0]["reason"]


def test_exception_in_user_code_includes_line_number():
    # Error on line 2 of the submission ("return x.nope"); test just calls fn.
    ns = _ns("def fn(x):\n    return x.nope")
    tests = [{"name": "t1", "source": "def test_a():\n    fn(1)"}]
    out = run_tests(ns, "fn", tests)
    assert out["failed"] == 1
    reason = out["detail"][0]["reason"]
    assert "AttributeError" in reason
    assert "line 2" in reason


def test_source_with_no_test_function_is_a_failure():
    ns = _ns("def make(f):\n    return f")
    tests = [{"name": "bad", "source": "x = 1"}]
    out = run_tests(ns, "make", tests)
    assert out["failed"] == 1 and "no test function" in out["detail"][0]["reason"]


def test_multiple_test_functions_in_one_source_all_run():
    ns = _ns("def make(f):\n    return lambda x: x * f")
    tests = [
        {
            "name": "t",
            "source": "def test_a():\n    assert make(1)(1) == 1\n"
            "def test_b():\n    assert make(2)(2) == 4",
        }
    ]
    out = run_tests(ns, "make", tests)
    assert out == {"passed": 2, "failed": 0, "detail": []}
