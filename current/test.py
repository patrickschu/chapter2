import re



fes=['we', 'are', 'together', 'to', 'be', 'free']
fes=['we', 'are', 'together']
print len(fes)
print fes.index('are')
print fes[3]
print fes.index('are')+1

context=[-1,0,1]

print [fes[fes.index('together')+t] for t in context]

print fes[-1]