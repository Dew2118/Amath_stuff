from dataclasses import dataclass
from itertools import permutations, chain 
import cProfile
import re
from datetime import datetime
from enum import Enum

class PieceType(Enum):
    SYMBOL = 1
    MULTI_SYMBOL = 2
    SINGLE_DIGIT = 3
    DOUBLE_DIGIT = 4
    EQUAL_SIGN = 5
    BLANK = 6
    NEGATIVE = 7

@dataclass
class Piece:
  name: str
  function: list
  type: PieceType

# CONSTANT
# All pieces
P0 = Piece('0',['0'],PieceType.SINGLE_DIGIT)
P1 = Piece('1',['1'],PieceType.SINGLE_DIGIT)
P2 = Piece('2',['2'],PieceType.SINGLE_DIGIT)
P3 = Piece('3',['3'],PieceType.SINGLE_DIGIT)
P4 = Piece('4',['4'],PieceType.SINGLE_DIGIT)
P5 = Piece('5',['5'],PieceType.SINGLE_DIGIT)
P6 = Piece('6',['6'],PieceType.SINGLE_DIGIT)
P7 = Piece('7',['7'],PieceType.SINGLE_DIGIT)
P8 = Piece('8',['8'],PieceType.SINGLE_DIGIT)
P9 = Piece('9',['9'],PieceType.SINGLE_DIGIT)
P10 = Piece('10',['10'],PieceType.DOUBLE_DIGIT)
P11 = Piece('11',['11'],PieceType.DOUBLE_DIGIT)
P12 = Piece('12',['12'],PieceType.DOUBLE_DIGIT)
P13 = Piece('13',['13'],PieceType.DOUBLE_DIGIT)
P14 = Piece('14',['14'],PieceType.DOUBLE_DIGIT)
P15 = Piece('15',['15'],PieceType.DOUBLE_DIGIT)
P16 = Piece('16',['16'],PieceType.DOUBLE_DIGIT)
P17 = Piece('17',['17'],PieceType.DOUBLE_DIGIT)
P18 = Piece('18',['18'],PieceType.DOUBLE_DIGIT)
P19 = Piece('19',['19'],PieceType.DOUBLE_DIGIT)
P20 = Piece('20',['20'],PieceType.DOUBLE_DIGIT)
Pequal = Piece('=',['=='],PieceType.EQUAL_SIGN)
Pplus = Piece('+',['+'],PieceType.SYMBOL)
Pminus = Piece('-',['-'],[PieceType.NEGATIVE])
Pplusminus = Piece('+/-',['+','-'],PieceType.MULTI_SYMBOL)
Pmul = Piece('*',['*'],PieceType.SYMBOL)
Pdiv = Piece('/',['/'],PieceType.SYMBOL)
Pmuldiv = Piece('*/',['*','/'],PieceType.MULTI_SYMBOL)
#blank can be all of the pieces
Pblank = Piece('BLANK',['*','/','+','-','0','1','2','3','4','5','6','7','8','9','10',
'11','12','13','14','15','16','17','18','19','20','=='],PieceType.BLANK)


class Strategy:
    def __init__(self, show_stats = False) -> None:
        self.show_stats = show_stats

    def search_valid_equation(self, piece_list):
        result = []
        for piece_type_list in self.get_all_piece_type_list(piece_list):
            a = self.create_equation(self.check_valid(piece_type_list), piece_list)
            print(list(a))

    def product(self,*args, repeat=1):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        #pools = [tuple(pool) for pool in args] * repeat
        pools = [arg for arg in args]
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    def get_all_piece_type_list(self,piece_list):
        return self.product(*[[p.type.name] for p in piece_list])

    def check_valid(self,piece_type_list):
        result = []
        permute = permutations(piece_type_list)
        all = 0
        c = 0
        
        for equation in permute:
            # print(equation)
            all += 1
            if equation[0] in ['SYMBOL','EQUAL_SIGN']:
                continue
            #check if the first character is a symbol
            # print(equation)
            if equation[-1] in ['SYMBOL','EQUAL_SIGN','NEGATIVE']:
                continue
            #check if the first character is a symbol
            #check if ** (which is the exponent symbol in python) is in there because it is not allowed in A-math
            if '**' in equation:
                continue
            #find the index of the first '=' sign
            if 'EQUAL_SIGN' not in equation:
                continue
            i = equation.index('EQUAL_SIGN')
            #check if the character in front of '=' is a symbol
            if equation[i-1] in ['SYMBOL','EQUAL_SIGN','NEGATIVE']:
                continue
            #in case index of i (=) + 2 is more than the lenght of the equation
            if i+1 < len(equation):
                #check if the character in behind of '==' is a symbol
                if equation[i+1] in ['SYMBOL','EQUAL_SIGN']:
                    continue
            #check if the character in behind of a symbol is a symbol
            if not self.check(equation, ['SYMBOL','NEGATIVE']):
                continue
            #check if the expression matched which is that if there are leading 0s(0 is allowed but 03 or 0005 is not)
            if not self.check_for_double(piece_type_list):
                continue
            result.append(equation)
        return result

    def check(self,tuple,constant_list):
        for i in range(len(tuple) - 1):
            if tuple[i] in constant_list and tuple[i+1] in ['SYMBOL','NEGATIVE','EQUAL_SIGN']:
                return False
        return True

    def check_for_double(self,equation):
        # input - equation as tuple or list
        for i in range(len(equation) - 1):
            if equation[i] == 'DOUBLE_DIGIT' and (equation[i+1] == "SINGLE_DIGIT" or  equation[i-1] == "SINGLE_DIGIT"):
                return False
        return True

    def create_equation(self,piece_type_list, piece_list):
        # print(piece_type_list)
        # print(((p.function for p in t) for t in self.permutations(piece_list, piece_type_list)))
        print('HERE')
        return self.permutations(self.product(*[p for p in piece_list]), piece_type_list)

    def permutations(self, iterable, piece_type_list, r=None):
        # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
        # permutations(range(3)) --> 012 021 102 120 201 210
        pool = tuple(iterable)
        n = len(pool)
        print(pool)
        r = n if r is None else r
        if r > n:
            return
        indices = list(range(n))
        cycles = list(range(n, n-r, -1))
        result = tuple(pool[i] for i in indices[:r])[0]
        print(result)
        ptloresult = tuple(p.type.name for p in result)
        if ptloresult in piece_type_list:
            yield result
        while n:
            for i in reversed(range(r)):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i+1:] + indices[i:i+1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    result = tuple(pool[i] for i in indices[:r])
                    ptloresult = tuple(p.type.name for p in result)
                    if ptloresult in piece_type_list:
                        yield result
                    break
            else:
                return
        print('NO')

Strategy().search_valid_equation([Pplus,Pdiv,P3,Pequal,P2,P9,P2,Pmul,P1])