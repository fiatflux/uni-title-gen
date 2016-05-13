from random import choice
from random import random

SENTINEL = '.'

edges = {
    'start' : ([0.5,0.9,1.0],['prequalifier','qualifier', 'temporal']),
    'temporal' : ([0.5,0.9,1.0],['prequalifier','qualifier','position']),
    'prequalifier' : ([1.0],['qualifier']),
    'qualifier' : ([1.0],['position']),
    'position' : ([1.0],['linkage']),
    'linkage' : ([1.0],['org_type']),
    'org_type' : ([1.0],['org_scope']),
    'org_scope' : ([1.0],['org_purpose']),
    'org_purpose' : ([1.0],[SENTINEL])
}
tokens = {
    'temporal' : ['interim', 'acting', 'temporary'],
    'prequalifier' : ['associate', 'assistant', 'deputy', 'lead', 'executive', 'principal'],
    'qualifier' : ['associate', 'assistant', 'deputy', 'vice', 'deputy'],
    'position' : ['chancellor', 'provost', 'coordinator', 'manager', 'executive', 'chair',
            'liaison'],
    'role_linkage' : ['of', 'to', 'for'],
    'role_scope' : ['internal', 'external', 'academic', 'student', 'athletic', 'facilities'],
    'role' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate', 'maintenance'],
    'linkage' : ['of', 'to', 'for'],
    'org_type' : ['the office of', 'the committee on', 'the subcommittee for', 'the task force on'],
    'org_scope' : ['academic', 'community', 'neighborhood', 'dining', 'athletic', 'alumni',
        'donor', 'investor', 'employee'],
    'org_purpose' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate', 'services']
}

node = 'start'
prev_token = ''
output = []
while True:
    probs,e = edges[node]
    x = random()
    i = 0
    for j,p in enumerate(probs):
        if x < p:
            i = j
            break
    if e[j] == SENTINEL:
        break
    tok = choice(tokens[e[j]])
    if prev_token == tok:
        continue
    output.append(tok)
    prev_token = tok
    node = e[j]

print(' '.join(output))
