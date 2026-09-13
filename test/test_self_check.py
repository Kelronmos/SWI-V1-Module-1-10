from security.self_check import SelfCheck, require_valid


def test_all_checks_pass():
    gate = SelfCheck([lambda x: x is not None, lambda x: isinstance(x, dict)])
    result = gate.validate({})
    assert result.passed


def test_any_failed_check_halts():
    gate = SelfCheck([lambda x: True, lambda x: False, lambda x: True])
    result = gate.validate({})
    assert not result.passed


def test_check_exception_fails_closed():
    def broken(_):
        raise RuntimeError("unexpected")

    result = SelfCheck([broken]).validate({})
    assert not result.passed


def test_require_valid_allows_pass():
    require_valid(SelfCheck([lambda x: True]).validate({}))


def test_require_valid_blocks_failure():
    try:
        require_valid(SelfCheck([lambda x: False]).validate({}))
    except ValueError:
        pass
    else:
        raise AssertionError("failed check must halt")
