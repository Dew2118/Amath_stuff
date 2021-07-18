from dataclasses import dataclass
from itertools import permutations, combinations, chain
from datetime import datetime
import re

@dataclass
class Piece:
  name: str
  function: list

# CONSTANT
# All pieces
P0 = Piece('0',['0'])
P1 = Piece('1',['1'])
P2 = Piece('2',['2'])
P3 = Piece('3',['3'])
P4 = Piece('4',['4'])
P5 = Piece('5',['5'])
P6 = Piece('6',['6'])
P7 = Piece('7',['7'])
P8 = Piece('8',['8'])
P9 = Piece('9',['9'])
P10 = Piece('10',['10'])
P11 = Piece('11',['11'])
P12 = Piece('12',['12'])
P13 = Piece('13',['13'])
P14 = Piece('14',['14'])
P15 = Piece('15',['15'])
P16 = Piece('16',['16'])
P17 = Piece('17',['17'])
P18 = Piece('18',['18'])
P19 = Piece('19',['19'])
P20 = Piece('20',['20'])
Pequal = Piece('=',['=='])
Pplus = Piece('+',['+'])
Pminus = Piece('-',['-'])
Pplusminus = Piece('+/-',['+','-'])
Pmul = Piece('*',['*'])
Pdiv = Piece('/',['/'])
Pmuldiv = Piece('*/',['*','/'])
#blank can be all of the pieces
Pblank = Piece('BLANK',['*','/','+','-','0','1','2','3','4','5','6','7','8','9','10',
'11','12','13','14','15','16','17','18','19','20','=='])
pattern = r'^-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*==-*([0-9]|[1-9][0-9]{1,2})([+-/*]([0-9]|[1-9][0-9]{1,2}))*$'
EQ_PATTERN = re.compile(pattern)
class Strategy:
    def __init__(self, measure_time_lapse = True) -> None:
        self.measure_time_lapse = measure_time_lapse

    def search_valid_equation(self,piece_list):
        timestamp = datetime.timestamp(datetime.now())
        result = []
        for func_list in self.get_all_func_list(piece_list):
            result.extend(self.sub_search_valid_equation(func_list))
        if self.measure_time_lapse:
            print('\n', self.__class__.__name__)
            print(f'{round(datetime.timestamp(datetime.now()) - timestamp,3)} seconds')
            print(f'all = {self.all}, c = {self.c}')
            print('-'*20, '\n')
        return set(result)

    def sub_search_valid_equation(self,func_list):
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
            if eq_str[0] in ['+','-','*','/','=']:
                continue
            if eq_str[i-1] in ['+','-','*','/','=']:
                continue
            if i+2 < len(eq_str):
                if eq_str[i+2] in ['+','-','*','/','=']:
                    continue
            if eq_str[-1] in ['+','-','*','/','=']:
                continue
            if not self.check(eq_str, ['+','*','/','-']):
                continue
            if not re.match(EQ_PATTERN, eq_str):
                continue
            c += 1
            if eval(eq_str):
                result.append(eq_str)
        self.all = all
        self.c = c
        return result

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

    def get_all_func_list(self,piece_list):
        func_list = []
        for p in piece_list:
            func_list.append(p.function)
        return self.product(*func_list)

    def check(self,str,constant_list):
        for constant in constant_list:
            i = str.find(constant)
            if str[i+1] in ['+','-','*','/','=']:
                return False
        return True
    
    def check_for_zeros(self,eq_str):
        for i,a in enumerate(eq_str):
            if a == '0' and i+1 < len(eq_str):
                if eq_str[i+1] in list('0123456789'):
                    return False
        return True

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)

def is_valid_equation(eq):
    return (re.match(EQ_PATTERN, eq))

pieces = list(flatten([[P0]*5, [P4]*5, [P8]*4, [P12]*2, [P16], [P20], [Pmul]*4, [Pdiv]*4, [Pplus]*4,[Pminus]*4,[P1]*6,[P5]*4,[P9]*4,[P13],[P17],[P2]*6,[P6]*4,[P10]*2, [P14], [P18], [P3]*5, [P7]*4, [P11], [P15], [P19], [Pplusminus]*5, [Pmuldiv] * 4, [Pequal]*11, [Pblank]*4]))
combi = combinations(pieces,9)
c = 0
last_c = 0
last_set = []
strategy = Strategy(False)

while True:
  a = list(next(combi))
  last_set = a.copy()
  if Pequal in a:
    c += 1
    result = strategy.search_valid_equation(a)
    if len(result) > 0:
      print(a,result)
      break
  if (c % 1000000 == 0) and (c != last_c):
    print(c)
    last_c = c