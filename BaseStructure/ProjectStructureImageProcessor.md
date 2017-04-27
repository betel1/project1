

```python
#Load in tandem with Project 2

import tornado.web
import json
import io
import matplotlib.pyplot as plt
import pylab
import os
import time
from PIL import Image


while True:
    try:
        VOTES = json.load(open('votes.json'))
        Pltvotes = VOTES.values()
    except (IOError, ValueError):
        Pltvotes = [1,1,1,1,1]
        VOTES = [1,1,1,1,1]
    alpha = 0
    labels = 'Openness', 'Extraversion', 'Neuroticism', 'Agreeableness','Conscientiousness'
    sizes = Pltvotes
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','violet']
    explode = (0, 0, 0, 0, 0)
 

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
    plt.axis('equal')
    pylab.savefig('Pltvotes.png')
    time.sleep(2)
    os.remove('Pltvotes.png')
    plt.clf()
```


```python

```
