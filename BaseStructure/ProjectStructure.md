



```python
#Load the Image Processor in tandem.

import tornado.web
import json
import io
import matplotlib.pyplot as plt
import pylab
import os
import time
from PIL import Image

    
PORT = 9137

COLORS = (
    'A',
    'B',
    'C'
)

# Ten-Item Personality Inventory (TIPI)
# http://gosling.psy.utexas.edu/wp-content/uploads/2014/09/tipi.pdf
# Preceded by the header: 'I see myself as:'

try:
    os.remove('votes.json')
    os = {}
except (OSError):
    os = {}
    
try:
    VOTES = json.load(open('votes.json'))
except (IOError, ValueError):
    VOTES = {}

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        # Calculate the score for each personality trait
        Extraversion = float(int(self.get_argument("q01", 0)) + int(self.get_argument("q06", 0)))/2
        Agreeableness = float(int(self.get_argument("q02", 0)) + int(self.get_argument("q07", 0)))/2
        Conscientiousness = float(int(self.get_argument("q03", 0)) + int(self.get_argument("q08", 0)))/2
        Neuroticism = float(int(self.get_argument("q04", 0)) + int(self.get_argument("q09", 0)))/2
        Openness = float(int(self.get_argument("q05", 0)) + int(self.get_argument("q10", 0)))/2
        
        # Load the scores into dictionary
        VOTES['Extraversion'] = VOTES.get('Extraversion', 0) + Extraversion
        VOTES['Agreeableness'] = VOTES.get('Agreeableness', 0) + Agreeableness
        VOTES['Conscientiousness'] = VOTES.get('Conscientiousness', 0) + Conscientiousness
        VOTES['Neuroticism'] = VOTES.get('Neuroticism', 0) + Neuroticism
        VOTES['Openness'] = VOTES.get('Openness', 0) + Openness
        json.dump(VOTES, open('votes.json', 'w'))
        self.render('responses.html', colors=COLORS, votes=VOTES)

class ResultsHandler(tornado.web.RequestHandler):
    def get(self):
        global VOTES
        self.render('results.html', votes=VOTES)
        time.sleep(10)
        VOTES = {}

# BE SURE TO TURN OFF DEBUG IN PROD
Application = tornado.web.Application([
        (r"/", FormHandler),
        (r"/results", ResultsHandler),
        (r"/files/(.*)", tornado.web.StaticFileHandler, {'path': '.'}),
    ], debug=True)

Application.listen(PORT)
```


```python
%%file responses.html
<html>
<script src="https://use.fontawesome.com/a7c9ccc168.js"></script>
<title>Ten Item Personality Inventory</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
<body>
<div class="w3-container w3-teal">
  <h1>Ten Item Personality Inventory (TIPI)</h1>
</div>

<form>
<table class="grid" cellspacing="50">

<tr>

    <td></td>

    <td>Disagree<br>strongly</td>

    <td>Disagree<br>moderately</td>

    <td>Disagree<br>a little</td>

    <td>Neither agree<br/>nor disagree</td>

    <td>Agree<br>a little</td>

    <td>Agree<br>moderately</td>

    <td>Agree<br>strongly</td>

</tr>

<tr>

    <td class="griditem">1. Extraverted, enthusiastic.</td>

    <td><input type=radio  name="q01" value=1></td>

    <td><input type=radio  name="q01" value=2></td>

    <td><input type=radio  name="q01" value=3></td>

    <td><input type=radio  name="q01" value=4></td>

    <td><input type=radio  name="q01" value=5></td>

    <td><input type=radio  name="q01" value=6></td>

    <td><input type=radio  name="q01" value=7></td>

</tr>

<tr>

    <td class="griditem">2. Critical, quarrelsome.</td>

    <td><input type=radio  name="q02" value=7></td>

    <td><input type=radio  name="q02" value=6></td>

    <td><input type=radio  name="q02" value=5></td>

    <td><input type=radio  name="q02" value=4></td>

    <td><input type=radio  name="q02" value=3></td>

    <td><input type=radio  name="q02" value=2></td>

    <td><input type=radio  name="q02" value=1></td>

</tr>

<tr>

    <td class="griditem">3. Dependable, self-disciplined.</td>

    <td><input type=radio  name="q03" value=1></td>

    <td><input type=radio  name="q03" value=2></td>

    <td><input type=radio  name="q03" value=3></td>

    <td><input type=radio  name="q03" value=4></td>

    <td><input type=radio  name="q03" value=5></td>

    <td><input type=radio  name="q03" value=6></td>

    <td><input type=radio  name="q03" value=7></td>

</tr>

<tr>

    <td class="griditem">4. Anxious, easily upset.</td>

    <td><input type=radio  name="q04" value=7></td>

    <td><input type=radio  name="q04" value=6></td>

    <td><input type=radio  name="q04" value=5></td>

    <td><input type=radio  name="q04" value=4></td>

    <td><input type=radio  name="q04" value=3></td>

    <td><input type=radio  name="q04" value=2></td>

    <td><input type=radio  name="q04" value=1></td>

</tr>

<tr>

    <td class="griditem">5. Open to new experiences, complex.</td>

    <td><input type=radio  name="q05" value=1></td>

    <td><input type=radio  name="q05" value=2></td>

    <td><input type=radio  name="q05" value=3></td>

    <td><input type=radio  name="q05" value=4></td>

    <td><input type=radio  name="q05" value=5></td>

    <td><input type=radio  name="q05" value=6></td>

    <td><input type=radio  name="q05" value=7></td>

</tr>

<tr>

    <td class="griditem">6. Reserved, quiet.</td>

    <td><input type=radio  name="q06" value=7></td>

    <td><input type=radio  name="q06" value=6></td>

    <td><input type=radio  name="q06" value=5></td>

    <td><input type=radio  name="q06" value=4></td>

    <td><input type=radio  name="q06" value=3></td>

    <td><input type=radio  name="q06" value=2></td>

    <td><input type=radio  name="q06" value=1></td>

</tr>

<tr>

    <td class="griditem">7. Sympathetic, warm.</td>

    <td><input type=radio  name="q07" value=1></td>

    <td><input type=radio  name="q07" value=2></td>

    <td><input type=radio  name="q07" value=3></td>

    <td><input type=radio  name="q07" value=4></td>

    <td><input type=radio  name="q07" value=5></td>

    <td><input type=radio  name="q07" value=6></td>

    <td><input type=radio  name="q07" value=7></td>

</tr>

<tr>

    <td class="griditem">8. Disorganized, careless.</td>

    <td><input type=radio  name="q08" value=7></td>

    <td><input type=radio  name="q08" value=6></td>

    <td><input type=radio  name="q08" value=5></td>

    <td><input type=radio  name="q08" value=4></td>

    <td><input type=radio  name="q08" value=3></td>

    <td><input type=radio  name="q08" value=2></td>

    <td><input type=radio  name="q08" value=1></td>

</tr>

<tr>

    <td class="griditem">9. Calm, emotionally stable.</td>

    <td><input type=radio  name="q09" value=1></td>

    <td><input type=radio  name="q09" value=2></td>

    <td><input type=radio  name="q09" value=3></td>

    <td><input type=radio  name="q09" value=4></td>

    <td><input type=radio  name="q09" value=5></td>

    <td><input type=radio  name="q09" value=6></td>

    <td><input type=radio  name="q09" value=7></td>

</tr>

<tr>

    <td class="griditem">10. Disorganized, careless.</td>

    <td><input type=radio  name="q10" value=7></td>

    <td><input type=radio  name="q10" value=6></td>

    <td><input type=radio  name="q10" value=5></td>

    <td><input type=radio  name="q10" value=4></td>

    <td><input type=radio  name="q10" value=3></td>

    <td><input type=radio  name="q10" value=2></td>

    <td><input type=radio  name="q10" value=1></td>

</tr>

</table>
<input class="form-control" type="submit" value="Submit">
</form>
</div>
<b>Click here:</b> <a href="/results"> <i class="fa fa-heartbeat fa-5x"></i></a>
</html>
```


```python
%%file results.html
<html>
<title>Ten Item Personality Inventory</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css">
<body>

<div class="w3-container w3-teal">
  <h1>Ten Item Personality Inventory (TIPI)</h1>
</div>
<body>

<div class="row">

<div class="col-md-6">
<h2>Results</h2>
<table class="table table-striped table-bordered">
<thead><th>Personality</th><th>Score</th></thead>
<tbody>
{% for vote, personality in sorted(votes.items(), key=lambda p: p[1], reverse=True) %}
    <tr><td>{{ vote }}</td><td>{{ personality }}</td></tr>
{% end %}
</tbody>
</table>
</div>

</div>
</div>
</body>
<body>

<h2>Distribution</h2>
<img src="/files/Pltvotes.png">

<h2>What does this mean?</h2>

<a href="https://www.ocf.berkeley.edu/~johnlab/pdfs/2008chapter.pdf" align = bottom target="blank">  <h2>(Click here for more information)</h2>
<img src="/files/FiveFactor.jpg" align = left> 

<iframe width="350" height="350"
src="https://www.youtube.com/embed/xXATiPciG8o" align = right>
</iframe>
</body>
</html>
```


```python

```
