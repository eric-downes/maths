import re


'''
build spaces from:
. := AND
| := conditional
! := NOT
( := open context
) := close context

'p(A.B.C|D+E)'
'''

PROBRE = re.compile(r'^p\(([!\.\+\|\(\)A-Z]+)\)$')
PARENRE = re.compile(r'\(([^)]+)')

def parse_lstr(lstr:str):
    if lstr.count('|') > 0: raise ValueError(f'Logic string cannot contain conditionals; {lstr}')
    m = PARENRE.findall(lstr)
    things = set(lstr.split('.'))
    
    
def parse_pstr(pstr:str):
    m = PROBRE.match(pstr)
    logic_str = m.groups()[0]
    if logic_str.count('|') > 1: raise ValueError(f'Probability string can only contain one conditional; {pstr}')
    args, conds = map(parse_lstr, logic.split('|',1))
    if not args: raise ValueError(f'Probability string must have at least one argument; {pstr}')
    if conds

    anded = arg.split('.')

parse_pstr('p(A.B.C|D.E)')
assert(m.groups()[0] == 'A.B.C|D.E')

# parsing

       


# understand complements
p = np.random.random()
prob = ProbabilityEngine()
prob.define('p(A)', p)
assert(prob.look('p(A)') == p)
assert(prob.calc('p(!A)') == 1-p)

# make a thing that can use Bayes' Law
p, q = np.random.random(2)
prob = ProbabilityEngine()
prob.define('p(A; B)', p)
prob.define('p(B)', q)
assert(prob.get('p(A)') p*q)

# Goal 2: parse generic logical expressions 



def get_context(s):
    m = re.search(r'^\p\((.*)\)$')
    if not m: return 

    
def ProbabilityEngine():
   pass 


class ProbabilitySpace:
    def __init__(self, space:set):
        self.space = space
        
'''
start off by using this:
https://booleanpy.readthedocs.io/en/latest/users_guide.html

0. make sure I can use basic AND:=*, OR:=+ etc
1. make sure I can 

1. extend to include the conditional |?
U := OR
'''

