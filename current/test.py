import numpy as np

t=np.array([[1,1], [2,2]])


print t, "\n---"

print np.column_stack((t, [[1000,1000,0], [2000,2000,0]]))