import webapp2

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
    'org_type' : ([0.9,1.0],['org_scope','org_qualifier']),
    'org_qualifier' : ([1.0],['org_scope']),
    'org_scope' : ([1.0],['org_purpose']),
    'org_purpose' : ([1.0],[SENTINEL])
}
tokens = {
    'temporal' : ['interim', 'acting', 'temporary'],
    'prequalifier' : ['associate', 'assistant', 'deputy', 'lead', 'executive', 'principal'],
    'qualifier' : ['associate', 'assistant', 'deputy', 'vice', 'deputy'],
    'position' : ['chancellor', 'provost', 'coordinator', 'manager', 'executive', 'chair',
            'liaison', 'dean'],
    'role_linkage' : ['of', 'to', 'for'],
    'role_scope' : ['internal', 'external', 'academic', 'student', 'athletic', 'facilities'],
    'role' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate', 'maintenance'],
    'linkage' : ['of', 'to', 'for'],
    'org_type' : ['the office of', 'the committee on', 'the subcommittee for', 'the task force on'],
    'org_qualifier' : ['strategic'],
    'org_scope' : ['academic', 'community', 'neighborhood', 'dining', 'athletic', 'alumni',
        'donor', 'investor', 'employee'],
    'org_purpose' : ['affairs', 'relations', 'partnerships', 'compliance', 'climate', 'services',
        'diversity']
}

def generate_title():
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

    return(' '.join(output))

PRECONTENT = """<!DOCTYPE html><html><head>
<title>University Title Generator</title>
<link href="style.css" rel="stylesheet" type="text/css" />
<meta name="description" content="What will be your next title at an R1 institution?" />
<meta name="robots" content="nosnippet" />
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-77758304-1', 'auto');
  ga('send', 'pageview');
</script>

</head><body>
<div id="header">

</header>
<div id="maincontent">
<p id="text">"""

POSTCONTENT = """</p>
</div>
</body></html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        title = generate_title()
        self.response.write(PRECONTENT)
        self.response.write(title)
        self.response.write(POSTCONTENT)

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ], debug=True)
