import logging
from random import choice
from random import random
import webapp2

SENTINEL = '.'

edges = {
    'start' : ([0.5,0.9,1.0],['prequalifier','qualifier', 'temporal']),
    'temporal' : ([0.5,0.9,1.0],['prequalifier','qualifier','position']),
    'prequalifier' : ([1.0],['qualifier']),
    'qualifier' : ([1.0],['position']),
    'position' : ([0.2,1.0],['role_scope','org_type']),
    'role_scope' : ([1.0],['role']),
    'role' : ([1.0],['linkage']),
    'linkage' : ([1.0],['org_type']),
    'org_type' : ([0.9,1.0],['org_scope','org_qualifier']),
    'org_qualifier' : ([1.0],['org_scope']),
    'org_scope' : ([1.0],['org_purpose']),
    'org_purpose' : ([1.0],[SENTINEL])
}
tokens = {
    'temporal' : ['Interim', 'Acting', 'Temporary'],
    'prequalifier' : ['Associate', 'Assistant', 'Deputy', 'Lead', 'Executive', 'Principal'],
    'qualifier' : ['Associate', 'Assistant', 'Deputy', 'Vice'],
    'position' : ['Chancellor of', 'Provost for', 'Coordinator of', 'Manager of', 'Executive for',
        'Chair of', 'Liaison to', 'Dean of', 'President of'],
    'role_scope' : ['Internal', 'External', 'Academic', 'Student', 'Athletic', 'Facilities',
        'Interdepartmental'],
    'role' : ['Affairs', 'Relations', 'Partnerships', 'Compliance', 'Climate', 'Maintenance',
        'Technology', 'Communications'],
    'linkage' : ['of', 'to', 'for'],
    'org_type' : ['the Office of', 'the Committee on', 'the Subcommittee for', 'the Task Force on'],
    'org_qualifier' : ['Strategic'],
    'org_scope' : ['Academic', 'Community', 'Neighborhood', 'Dining', 'Athletic', 'Alumni',
        'Donor', 'Investor', 'Employee', 'Learning'],
    'org_purpose' : ['Affairs', 'Relations', 'Partnerships', 'Compliance', 'Climate', 'Services',
        'Diversity', 'Technology', 'Communications', 'Planning', 'Outreach']
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
        if prev_token == tok and tok != 'deputy':
            continue
        output.append(tok)
        prev_token = tok
        node = e[j]

    return(' '.join(output))

PRECONTENT = """<!DOCTYPE html><html><head>
<title>University Title Generator</title>
<link href="style.css" rel="stylesheet" type="text/css" />
<meta property="og:image" content="suit.jpg" />
<meta name="description" content="Damning indictment of the corporatization of higher education, or
career finder? You decide!" />
<meta name="robots" content="nosnippet" />
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-77758304-1', 'auto');
  ga('send', 'pageview');
</script>
<script>
var trackOutboundLink = function(url) {
   ga('send', 'event', 'outbound', 'click', url, {
     'transport': 'beacon',
     'hitCallback': function(){document.location = url;}
   });
}
</script>

</head><body>
<div id="maincontent">
<form><input id="refreshbutton" type="submit" value="This title is not prestigious enough for me. Do you even know who I am?" /></form>
<p id="title">"""

POSTCONTENT = """</p>
</div>
<!--Fork me on github: https://github.com/fiatflux/uni-title-gen -->
</body></html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        title = generate_title()
        self.response.write(PRECONTENT)
        self.response.write(title)
        self.response.write(POSTCONTENT)
        logging.info('GeneratedTitle="%s"' % (title))

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ], debug=True)
