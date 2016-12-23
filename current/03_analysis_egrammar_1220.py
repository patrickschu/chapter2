import egrammartools as eg
import numpy as np
import time

completestart=time.time()
listi=[]
dir="/home/ps22344/Downloads/craigbalanced_0601"

rep_raw, rep_freq= eg.repeatedpunctuationfinder(dir)
listi.append(np.array(rep_freq))


leet_raw, leet_freq= eg.leetcounter(dir)
listi.append(np.array(leet_freq))


rebfor_raw, rebfor_freq= eg.rebusfinder_for(dir)
listi.append(np.array(rebfor_freq))

rebto_raw, rebto_freq= eg.rebusfinder_to(dir)
listi.append(np.array(rebto_freq))

rebtoo_raw, rebtoo_freq= eg.rebusfinder_too(dir)
listi.append(np.array(rebtoo_freq))

caps_raw, caps_freq=eg.capsfinder(dir, 0.5)
listi.append(np.array(caps_freq))

single_raw, single_freq=eg.singleletterfinder(dir)
listi.append(np.array(single_freq))

clip_raw, clip_freq=eg.clippingcounter(dir)
listi.append(np.array(clip_freq))

acro_raw, acro_freq=eg.acronymcounter(dir)
listi.append(np.array(acro_freq))

emos_raw, emos_freq=eg.emoticonfinder(dir)
listi.append(np.array(emos_freq))

# # for x in listi:
	# # print "!!!!!\n\n", x
	
t=np.column_stack(listi)

print type(t), t.shape
completeend=time.time()

print "This took us {} minutes. So slow!".format((completeend-completestart)/60)