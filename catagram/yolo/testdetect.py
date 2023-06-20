import random
import os
from django.conf import settings

my_file = open(os.path.join(settings.BASE_DIR,
               "./catagram/yolo/cat_autocap.csv"), "r")

d = {}
l=[]
s = []
for i in my_file:
    line = str(i)
    line = line.strip('\n')
    line = line.split(',')
    if line[0] in d.keys():
        l.append(line[1])
        d.update({line[0]:l})
    else:
        l=[]
        d.update({line[0]:line[1]})
        l.append(line[1])

def detectword(w):
    k = list(d.keys())
    if w in k:
        #print(w)
        #return d[w]
        while (len(s) < 3 ):
            c = random.choice(d[w])
            if c not in s:
                s.append(c)
        #print(s)        
        return s

#detectword('catsleep')