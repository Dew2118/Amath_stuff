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
Pminus = Piece('-',['-'],PieceType.SYMBOL)
Pplusminus = Piece('+/-',['+','-'],PieceType.MULTI_SYMBOL)
Pmul = Piece('*',['*'],PieceType.SYMBOL)
Pdiv = Piece('/',['/'],PieceType.SYMBOL)
Pmuldiv = Piece('*/',['*','/'],PieceType.MULTI_SYMBOL)
#blank can be all of the pieces
Pblank = Piece('BLANK',['*','/','+','-','0','1','2','3','4','5','6','7','8','9','10',
'11','12','13','14','15','16','17','18','19','20','=='],PieceType.BLANK)

pattern = r'^-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*==-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*$'
EQ_PATTERN = re.compile(pattern)


class Strategy1:
    def __init__(self, measure_time_lapse = True) -> None:
        self.measure_time_lapse = measure_time_lapse

    def search_valid_equation(self,piece_list):
        timestamp = datetime.timestamp(datetime.now())
        result = []
        for func_list in self.get_all_func_list(piece_list):
            result.extend(self.sub_search_valid_equation(func_list, piece_list))
        if self.measure_time_lapse:
            print('\n', self.__class__.__name__)
            print(f'{round(datetime.timestamp(datetime.now()) - timestamp,3)} seconds')
            print(f'all = {self.all}, c = {self.c}')
            print('-'*20, '\n')
        return set(result)

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

    def sub_search_valid_equation(self, func_list, piece_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result

    def get_all_func_list(self,piece_list):
        func_list = [p.function for p in piece_list]
        return self.product(*func_list)


class Strategy2(Strategy1):
    def sub_search_valid_equation(self, func_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            # print(eq_str)
            # break
            if '**' in eq_str:
                continue
            if eq_str[0] in ['+','*','/','=']:
                continue
            if eq_str[-1] in ['+','-','*','/','=']:
                continue
            # print(eq_str)
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result


class Strategy3(Strategy1):
    def sub_search_valid_equation(self, func_list):
        
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            # print(eq_str)
            # break
            if not re.match(EQ_PATTERN, eq_str):
                continue
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result


class Strategy4(Strategy1):
    def sub_search_valid_equation(self, func_list, piece_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            if '**' in eq_str:
                continue
            if eq_str[0] in ['+','*','/','=']:
                continue
            if eq_str[-1] in ['+','-','*','/','=']:
                continue
            if not re.match(EQ_PATTERN, eq_str):
                continue
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result


class Strategy5(Strategy1):
    def sub_search_valid_equation(self, func_list, piece_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            if '**' in eq_str:
                continue
            l = eq_str.split('==')
            for e in l:
                if e != '':
                    if e[0] in ['+','*','/','=']:
                        continue
                    if e[-1] in ['+','-','*','/','=']:
                        continue
            if not re.match(EQ_PATTERN, eq_str):
                continue
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result


class Strategy6(Strategy1):
    def sub_search_valid_equation(self, func_list, piece_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            eq_str = ''.join(equation)
            if '**' in eq_str:
                continue
            i = eq_str.find('=')
            if eq_str[0] in ['+','*','/','=']:
                continue
            if eq_str[i-1] in ['+','-','*','/','=']:
                continue
            if i+2 < len(eq_str):
                if eq_str[i+2] in ['+','*','/','=']:
                    continue
            if eq_str[-1] in ['+','-','*','/','=']:
                continue
            # print(eq_str)
            if not re.match(EQ_PATTERN, eq_str):
                continue
            try:
                c += 1
                if eval(eq_str):
                    result.append(eq_str)
            except SyntaxError:
                pass
        self.all = all
        self.c = c
        return result


class Strategy7(Strategy1):
    def sub_search_valid_equation(self,func_list, piece_list):
        result = []
        permute = permutations(func_list)
        all = 0
        c = 0
        for equation in permute:
            all += 1
            if equation[0] in ['+','*','/','=']:
                continue
            #check if the first character is a symbol
            # print(equation)
            if equation[-1] in ['+','-','*','/','=']:
                continue
            #check if the first character is a symbol
            #check if ** (which is the exponent symbol in python) is in there because it is not allowed in A-math
            if '**' in equation:
                continue
            eq_str = ''.join(equation)
            #find the index of the first '=' sign
            i = eq_str.find('=')
            #check if the character in front of '=' is a symbol
            if eq_str[i-1] in ['+','-','*','/','=']:
                continue
            #in case index of i (=) + 2 is more than the lenght of the equation
            if i+2 < len(eq_str):
                #check if the character in behind of '==' is a symbol
                if eq_str[i+2] in ['+','*','/','=']:
                    continue
            #check if the character in behind of a symbol is a symbol
            if not self.check(eq_str, ['+','*','/','-']):
                continue
            #check if the expression matched which is that if there are leading 0s(0 is allowed but 03 or 0005 is not)
            if not re.match(EQ_PATTERN, eq_str):
                continue
            if not self.check_for_double(piece_list):
                continue
            c += 1
            #check if the equation is true
            if eval(eq_str):
                result.append(eq_str)
        self.all = all
        self.c = c
        return result

    def check(self,str,constant_list):
        for constant in constant_list:
            i = str.find(constant)
            if str[i+1] in ['+','-','*','/','=']:
                return False
        return True

    def check_for_double(self,equation):
        # input - equation as tuple or list
        for i in range(len(equation) - 1):
            if equation[i].type.name == 'DOUBLE_DIGIT' and (equation[i+1].type.name == "SINGLE_DIGIT" or  equation[i-1].type.name == "SINGLE_DIGIT"):
                return False
        return True

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


if __name__ == '__main__':
    # piece_list = [Pplus,Pdiv,P3,Pequal,P2,P9,P2,Pmul,P1]
    piece_list =[Pplus,Pdiv,P3,Pequal,P2,P9,P2,Pmul,P1]
    strategy_list = []
    # strategy_list.append(Strategy1())
    # strategy_list.append(Strategy2())
    # strategy_list.append(Strategy3())
    # strategy_list.append(Strategy4())
    # strategy_list.append(Strategy5())
    # strategy_list.append(Strategy6())
    strategy_list.append(Strategy7())
    standard = Strategy1(False).search_valid_equation(piece_list)
    for s in strategy_list:
        r = s.search_valid_equation(piece_list)
        print(r)
        # assert r == standard
cProfile.run('Strategy7().search_valid_equation([Pplus,Pdiv,P3,Pequal,P2,P9,P2,Pmul,P1])')