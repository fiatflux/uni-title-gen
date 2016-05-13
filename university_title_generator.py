from random import choice
from random import random

SENTINEL = '.'

edges = {
	'start' : ([0.5,0.9,1.0],['prequalifier','qualifier', 'temporal']),
	'temporal' : ([0.5,1.0],['prequalifier','qualifier']),
	'prequalifier' : ([1.0],['qualifier']),
	'qualifier' : ([1.0],['position']),
	'position' : ([1.0],['linkage']),
	'linkage' : ([1.0],['org_type']),
	'org_type' : ([1.0],['org_scope_linkage']),
	'org_scope_linkage' : ([1.0],['org_scope']),
	'org_scope' : ([1.0],['org_purpose']),
	'org_purpose' : ([1.0],[SENTINEL])
}
tokens = {
	'temporal' : ['interim', 'acting', 'temporary'],
	'prequalifier' : ['associate', 'assistant', 'deputy', 'lead', 'executive'],
	'qualifier' : ['associate', 'assistant', 'deputy', 'vice', 'deputy'],
	'position' : ['chancellor', 'provost', 'coordinator', 'manager', 'executive', 'chair', 'coach'],
	'role_linkage' : ['of', 'to', 'for'],
	'role_scope' : ['internal', 'external', 'academic', 'student', 'athletic'],
	'role' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate'],
	'linkage' : ['of', 'to', 'for'],
	'org_type' : ['the office', 'the committee', 'the subcommittee', 'the task force'],
	'org_scope_linkage' : ['on', 'of', 'for'],
	'org_scope' : ['academic', 'community', 'neighborhood', 'dining', 'athletic'],
	'org_purpose' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate']
}

node = 'start'
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
	print choice(tokens[e[j]]),
	node = e[j]
