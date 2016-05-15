import logging
from math import log, sqrt
from random import choice, lognormvariate, random
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

base_salaries = {
        'Chancellor of' : 400000,
        'Provost for' : 300000,
        'Coordinator of' : 80000,
        'Manager of' : 160000,
        'Executive for' : 250000,
        'Chair of' : 150000,
        'Liaison to' : 80000,
        'Dean of' : 250000,
        'President of' : 250000
}

def generate_title():
    node = 'start'
    prev_token = ''
    output = []

    num_qualifiers = 0
    has_temporal = False
    has_infix_role = False
    is_strategic = False
    is_executive = False
    is_athletic = False
    is_diversity = False
    is_finance = False
    is_academic = False
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

        node = e[j]

        if not num_qualifiers:
            if node == 'position':
                # Handle pre-position salary adjustments.
                if output[0] in tokens['temporal']:
                    has_temporal = True
                    num_qualifiers = len(output) - 1
                else:
                    num_qualifiers = len(output)
                base_salary = base_salaries[tok]
            elif tok == 'Executive' or tok == 'Principal':
                is_executive = True
        elif node == 'role':
            has_infix_role = True
        elif tok == 'Strategic':
            is_strategic = True
        elif tok == 'Athletic':
            is_athletic = True
        elif tok == 'Diversity':
            is_diversity = True
        elif tok == 'Donor' or tok == 'Investor':
            is_finance = True
        elif tok == 'Learning' or tok == 'Academic':
            is_academic = True

        output.append(tok)
        prev_token = tok
    
    multiplier = num_qualifiers**-1.5
    if has_temporal:
        multiplier *= 0.9
    if has_infix_role:
        multiplier *= 0.9
    if is_executive:
        multiplier *= 1.3
    if is_strategic:
        multiplier *= 1.1
    if is_athletic:
        multiplier *= 1.5
    if is_diversity:
        multiplier *= 0.8
    if is_finance:
        multiplier *= 1.5
    if is_academic:
        multiplier *= 0.8

    m = base_salary*multiplier
    v = (base_salary*0.05)**2
    phi = sqrt(v + m**2)
    mu = log(m**2/phi)
    sigma = sqrt(log(phi**2/m**2))

    return(' '.join(output), lognormvariate(mu, sigma))

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
<p id="title">"""

POSTCONTENT = """
<form><input id="refreshbutton" type="submit" value="This title is not prestigious enough for me. Do you even know who I am?" /></form>
</div>
<!--Fork me on github: https://github.com/fiatflux/uni-title-gen -->
</body></html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        title,salary = generate_title()
        self.response.write(PRECONTENT)
        self.response.write(title)
        self.response.write('</p></div><div id="footer"><p id="salary">Estimated salary: $%s</p>' % format(int(salary), ',d'))
        self.response.write(POSTCONTENT)
        logging.info('GeneratedTitle="%s"' % (title))
        logging.info('GeneratedSalary="%d"' % (salary))

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ], debug=True)
