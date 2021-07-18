from A_math_generatorv2 import Strategy
from enum import Enum
import re

class PieceType(Enum):
    SYMBOL = 1
    MULTI_SYMBOL = 2
    SINGLE_DIGIT = 3
    DOUBLE_DIGIT = 4
    EQUAL_SIGN = 5
    BLANK = 6
def test_strategy():
    assert Strategy(show_stats=True) is not None

def test_product():
    assert Strategy().product(PieceType.DOUBLE_DIGIT,PieceType.SINGLE_DIGIT,PieceType.SYMBOL,PieceType.MULTI_SYMBOL,PieceType.EQUAL_SIGN,PieceType.SYMBOL,PieceType.SINGLE_DIGIT,PieceType.SINGLE_DIGIT,PieceType.SINGLE_DIGIT) is not None
pattern = r'^-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*==-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*$'
EQ_PATTERN = re.compile(pattern)
# def ultimate_test(piece_list, equation):
    