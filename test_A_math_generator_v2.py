from A_math_generatorv2 import Pplus, Strategy
from A_math_generatorv2 import P1,P0,P2,P3,P4,Pplus,Pminus,Pequal,Pdiv,Pmul,P9
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

def test_check_valid():
    assert Strategy().check_valid([PieceType.SINGLE_DIGIT]) is not None
    # assert Strategy().check_valid([PieceType.SINGLE_DIGIT,PieceType.EQUAL_SIGN,PieceType.SINGLE_DIGIT,PieceType.]) == []

def test_permutations():
    assert [a for a in Strategy().permutations([P1,P2,Pplus],[('SYMBOL','SINGLE_DIGIT','SINGLE_DIGIT'),('DOUBLE_DIGIT')])] == [(Pplus, P1, P2),(Pplus,P2,P1)]
print([a for a in Strategy().permutations([Pplus,Pdiv,P3,Pequal,P2,P9,P2,Pmul,P1],[('SINGLE_DIGIT', 'SYMBOL', 'SINGLE_DIGIT', 'SINGLE_DIGIT', 'EQUAL_SIGN', 'SINGLE_DIGIT', 'SYMBOL', 'SYMBOL', 'SINGLE_DIGIT')])])
    
# def ultimate_test(piece_list, equation):
    