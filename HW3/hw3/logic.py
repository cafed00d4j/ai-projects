# AD
# AI HW3

from collections import namedtuple
from string import ascii_lowercase
from string import ascii_uppercase

Rule = namedtuple('Rule', ['lhs', 'rhs'])

r1 = Rule(lhs=['HasSymptom(x,Diarrhea)'], rhs='LostWeight(x)')
r2 = Rule(lhs=['LostWeight(x)', 'Diagnosis(x,LikelyInfected)'], rhs='Diagnosis(x,Infected)')
r3 = Rule(lhs=['HasTraveled(x,Tiberia)', 'HasFever(x)'], rhs='Diagnosis(x,LikelyInfected)')
kb1 ={}
kb1['Rules'] = [r1,r2,r3]
kb1['Facts'] = ["HasTraveled(John,Tiberia)", "HasFever(John)", "HasSymptom(John,Diarrhea)"]
inferred = []


def get_args(x):
    # chcek if x == Knows(jo, jan)
    # if yes, then return (jo, jan) or [x, jan]
    first = x.index('(') + 1
    last = x.index(')')
    arg_list = x[first:last].split(',')
    arg_list = [each.strip() for each in arg_list]
    return arg_list

def op(x):
    # op('Knows(John, x)')
    # 'Knows'
    return x.split('(')[0]
    
def is_variable(x):
    return type(x) == type(str()) and x in ascii_lowercase
    
def is_compound(x):
    return '(' in x
    
def is_list(x):
    return type(x) == type(list()) or type(x) == type(tuple())


def unify_var(var, x, theta):
    print 'in unify-var', ' unifying --', var, x, theta 
    if var in theta:
        val = theta[var]
        return unify(val, x, theta)
    elif x in theta:
        val = theta[x]
        return unify(var, val, theta)
    # Uncommnet for occur check. not needed fr hw3
    # elif occur_check(var, x): return 'failure'
    else:
        theta[var] = x
        print 'adding to theta ', var, ' := ', x
        return theta
##
##def equivalent(x, y):
##    # >>> equivalent('Weapon(x)', 'Weapon(y)')
##    # >>> True
##    # >>> equivalent('Weapon(x)', 'Weapon(x)')
##    # >>> True
##    # >>> equivalent('Weapon(x,z)', 'Weapon(y,a)')
##    # >>> True
##    # >>> equivalent('Weapon(M1)', 'Weapon(x)')
##    # >>> False
##    return all([each_x_arg in ascii_lowercase for each_x_arg in get_args(x)])\
##           and all([each_y_arg in ascii_lowercase for each_y_arg in get_args(y)])\
##           and op(x) == op(y)\
##           and len(x) == len(y)

def unify(x, y, theta):
    if type(theta) == type(None):
        print 'in unify(x,y,theta); encountered theta nonetype'
        import pdb; pdb.set_trace();
    if theta == 'failure':
        return 'failure'
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif is_compound(x) and is_compound(y):
        # TODO: Standardize variables
        return unify(get_args(x), get_args(y),unify(op(x), op(y), theta))
    elif is_list(x) and is_list(y):
        x_first = x[0]
        x_rest = x[1:len(x)]
        y_first = y[0]
        y_rest = y[1:len(y)]
        
        return unify(x_rest, y_rest, unify(x_first, y_first, theta))
    else:
        return 'failure'
   

def first_sentence(goals):
    return goals[0]

def rest_sentence(goals):
    return goals[1:len(goals)]


def subst(theta, q):
    # theta = {x/John}
    # q = Evil(x)
    # subst(theta, q) = Evil(John)
    ##
    ##    >>> th = {'i':'Jo'}
    ##    >>> q
    ##    'Evil(x,u,i,o)'
    ##    >>> subst(th,q)
    ##    'Evil(x,u,Jo,o)'

#    print 'trying to sub ', theta, ' into ', q
    argsq = get_args(q)
    opq = op(q)
    for each in theta:
        if each in q:
            argsq [argsq.index(each)] = theta[each]
    arg_str = ','.join(argsq)
    result = opq + '(' + arg_str + ')' 
#    print 'subbing ', theta, q, ' ---> ', result
    return result




def is_constant(x):
    return x[0] in ascii_uppercase

def equal(x, y):
    if is_constant(x) and is_constant(y):
        return x == y
    else:
        return True

def check_args_match(list1, list2):
    i = 0
    while i < len(list1):
        each1 = list1[i]
        each2 = list2[i]
        if not equal(each1, each2):
            return False
        i += 1
    return True



### FIXE Matches... using this inside fetch_rules if conditon causes lot of failure printslbut gives corrct output
def matches(goal, candidate):
    # BUG MAJOR: Fails on mathces('Knows(Jon, Amy)', 'Knows(x,y)')
    # Diagnos(x,Infected) matches rule r2 LostWeight(x)&Diagnosis(x,LikelyInfected)=>Diagnosis(x,Infected)
    # but Diagnois(x,Infected) shoudlnt match r3 HasTraveled(x,Tiberia)&HasFever(x)=>Diagnosis(x,LikelyInfected)
    gname = op(goal)
    goal_arg = get_args(goal)
    cand_arg = get_args(candidate)
    if gname not in candidate:
        return False
    elif len(goal_arg) != len(cand_arg):
        return False
    else:
        return check_args_match(goal_arg, cand_arg)
       

go = 'Diagnosis(John, Infected)'



#############################################################################
##def fetch_rules_for_goal(KB, goal):
##    # goal is of the form 'LostWeight(John)'
##    # or 'HasFever(John)'
##    ####### 
##    # Change to function that returns a list
##    # rules = []
##    # ....
##    # rules.appned(rule)
##    # return rules
##    # import pdb; pdb.set_trace()
##    gname = op(goal)
##    for rule in KB['Rules']:
##        # This is considton is jsut checking ig gname matches rule.rhs --
##        # Diagnos(x,Infected) matches rule r2 LostWeight(x)&Diagnosis(x,LikelyInfected)=>Diagnosis(x,Infected)
##        # but Diagnois(x,Infected) shoudlnt match r3 HasTraveled(x,Tiberia)&HasFever(x)=>Diagnosis(x,LikelyInfected)
##        #if matches(goal, rule.rhs): #FIXME returns Diagnosis(x,Infected) when goal is Diagnosis(John, LikeleyInfected)
##        if matches(goal, rule.rhs):
##            yield rule
##
###            rules.append(rule)
###    if not rules:
###        rules.append(goal)
###    return rules
##


def fetch_rules_for_goal(KB, goal):
    # goal is of the form 'LostWeight(John)'
    # or 'HasFever(John)'
    ####### 
    # Change to function that returns a list
    # rules = []
    # ....
    # rules.appned(rule)
    # return rules
    # import pdb; pdb.set_trace()
    gname = op(goal)
    garg = get_args(goal)
    rules = []
    for rule in KB['Rules']:
        if matches(goal, rule.rhs):
            rules.append(rule)
    return rules

##########################################################################

f1 = fetch_rules_for_goal(kb1, 'LostWeight(x)')
f2 = fetch_rules_for_goal(kb1, 'HasSymptom(x,Diarrhea)')

# FIXME: above
# fetch_rules_for_goal(kb, 'HasSymptom(John, Diarrhea)')
# does not work

def fol_bc_or(KB, goal, theta):
##    print goal, theta
##    # check if goal is present as fact in KB
##    facts = KB['Facts']
##    # Remove following method for efficieny
##    facts = [each.replace(' ', '') for each in facts]
##    if goal in facts:
##        print goal, ' is present in KB as fact'
##        yield theta
    for rule in fetch_rules_for_goal(KB, goal):
        # Standardize variables
        # For hw3 we assume there is onyl one variable
        lhs = rule.lhs
        rhs = rule.rhs
#        print 'unifying ', rhs, ' wtih goal=', goal, ' theta=', theta
        u = unify(rhs, goal, theta)
        for theta_prime in fol_bc_and(KB, lhs, u):
            yield theta_prime
    if goal in KB['Facts']:
#        print theta, ' and ', goal, ' goal in facts'
        yield theta
##    elif goal not in inferred:
##        print 'trying to infer ', goal
##        yield theta
    else:
#        print theta, ' goal=', goal, ' failing'
        yield 'failure'

def fol_bc_and(KB, goals, theta):
    # Test fol_bc_and(kb, ['HasSymptom(x,Diarrhea)'], {})
    if theta == 'failure':
#        print 'faling ', goals, ' for ', theta
        return
    elif len(goals) == 0:
       yield theta
    else:
        print goals
        f = first_sentence(goals)
        r = rest_sentence(goals)
        s = subst(theta, f)
        for theta_prime in fol_bc_or(KB, s, theta):
            for theta_double_prime in fol_bc_and(KB, r, theta_prime):
                yield theta_double_prime

def fol_bc_ask(KB, query, theta):
    return fol_bc_or(KB, query, theta)

theta = {}
f = fol_bc_ask(kb1, 'Diagnosis(John, Infected)', theta)


theta3 = {}
kb3 = {'Rules': [Rule(lhs=['American(x)', 'Weapon(y)', 'Sells(x,y,z)', 'Hostile(z)'], rhs='Criminal(x)'), Rule(lhs=['Missile(y)', 'Owns(Nono,y)'], rhs='Sells(West,y,Nono)'), Rule(lhs=['Missile(y)'], rhs='Weapon(y)'), Rule(lhs=['Enemy(z,America)'], rhs='Hostile(z)')], 'Facts': ['American(West)', 'Enemy(Nono,America)', 'Owns(Nono,M)', 'Missile(M)']}
f3 = fol_bc_ask(kb3,'Criminal(West)', theta3)


t3 = {}

kb4={}
r4 = Rule(lhs=['Bo(x)'],rhs='Ap(x)')
kb4['Rules'] = [r4]
kb4['Facts'] = ['Bo(Jo)']
q = fol_bc_ask(kb4, 'Ap(Jo)', t3)

# print next(q)


def is_rule(clause):
    return '=>' in clause

def is_fact(clause):
    return '=>' not in clause

def make_rule(clause):
    r = clause.split('=>')
    rhs = r[1]
    lhs = r[0].split('&')
    r = Rule(lhs, rhs)
    return r
    
def read_input():
    f = file('input.txt', 'rU')

    query = f.readline()[:-1]
    num_clauses = int(f.readline()[:-1])
    
    kb = {}
    kb ['Rules'] = []
    kb ['Facts'] = []
    
    for clause in f:
        clause = clause[:-1]
        if is_rule(clause):
            r = make_rule(clause)
            kb['Rules'].append(r)
        elif is_fact(clause):
            kb['Facts'].append(clause)
    return [kb, query]

[kb, query] = read_input()
theta = {}
question = fol_bc_ask(kb, query, theta)
answer = next(question)

if answer != 'failure':
    answer = 'TRUE'
else:
    answer = 'FALSE'

with open('output.txt', 'w') as f:
    f.write('\n'.join([answer]))

#
##th = {}
##unify('Knows(John,x)', 'Knows(y,Bill)', th)
##print th
##
##th = {}
##unify('Knows(John,x)', 'Knows(y,Mother(y))', th)
##print th


