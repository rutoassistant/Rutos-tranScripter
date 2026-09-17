"""Tests for ArithmeticEnv operations in JAVS-tranScripter."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from Env.arithmeticEnv import ArithmeticEnv as AE


def test_add():
    assert AE.addFun('3', '5') == 'result =int(3 + 5)'
    assert AE.addFun('$v1', '3') == 'result =int(v1 + 3)'


def test_subtract():
    assert AE.subtractFun('10', '3') == 'result =10 - 3'
    assert AE.subtractFun('result', '3') == 'result =result - 3'


def test_multiply():
    assert AE.multiplyFun('4', '5') == 'result =4 * 5'


def test_divide():
    assert AE.divideFun('10', '2') == 'result =int(10 / 2)'


def test_power():
    assert AE.powerFun('2', '3') == 'result = 2 ** 3'


def test_modulo():
    assert AE.moduloFun('10', '3') == 'result = 10 % 3'


def test_lt():
    assert AE.ltFun('3', '5') == 'result = 3 < 5'


def test_gt():
    assert AE.gtFun('5', '3') == 'result = 5 > 3'


def test_eq():
    assert AE.eqFun('4', '4') == 'result = 4 == 4'


def test_ne():
    assert AE.neFun('4', '5') == 'result = 4 != 5'


def test_le():
    assert AE.leFun('3', '5') == 'result = 3 <= 5'


def test_ge():
    assert AE.geFun('5', '3') == 'result = 5 >= 3'


def test_increment():
    assert AE.incrementFun('5') == 'result = 5 + 1'


def test_decrement():
    assert AE.decrementFun('5') == 'result = 5 - 1'


def test_env_words_registered():
    words = AE.env_Words_and_WordAsFunction
    for w in ['power', 'modulo', 'lt', 'gt', 'eq', 'ne', 'le', 'ge', 'increment', 'decrement']:
        assert w in words, f'{w} not registered'


def test_arg_count_validation():
    for fn in [AE.powerFun, AE.moduloFun, AE.ltFun, AE.gtFun, AE.eqFun, AE.neFun, AE.leFun, AE.geFun]:
        try:
            fn('1')
            assert False, f'{fn.__name__} should reject 1 arg'
        except Exception:
            pass


if __name__ == '__main__':
    import traceback
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            try:
                fn()
                print(f'✓ {name}')
            except Exception:
                failures += 1
                print(f'✗ {name}')
                traceback.print_exc()
    print(f'\n{failures} failures')
    sys.exit(1 if failures else 0)