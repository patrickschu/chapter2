import egrammartools as eg
import numpy as np
import time

completestart=time.time()
listi=[]

# emos_raw, emos_freq=eg.emoticonfinder('/home/ps22344/Downloads/craig_0208')
# listi.append(np.array(emos_freq))

# rep_raw, rep_freq= eg.repeatedpunctuationfinder('/home/ps22344/Downloads/craig_0208')
# listi.append(np.array(rep_freq))


leet_raw, leet_freq= eg.leetcounter('/home/ps22344/Downloads/craig_0208')
listi.append(np.array(leet_freq))


# rebfor_raw, rebfor_freq= eg.rebusfinder_for('/home/ps22344/Downloads/craig_0208')
# listi.append(rebfor_freq)

# rebto_raw, rebto_freq= eg.rebusfinder_to('/home/ps22344/Downloads/craig_0208')
# listi.append(rebto_freq)

# rebtoo_raw, rebtoo_freq= eg.rebusfinder_too('/home/ps22344/Downloads/craig_0208')
# listi.append(rebtoo_freq)

# caps_raw, caps_freq=eg.capsfinder('/home/ps22344/Downloads/craig_0208', 0.5)
# listi.append(caps_freq)

# single_raw, single_freq=eg.singleletterfinder('/home/ps22344/Downloads/craig_0208')
# listi.append(single_freq)

# clip_raw, clip_freq=eg.clippingcounter('/home/ps22344/Downloads/craig_0208')
# listi.append(clip_freq)

# acro_raw, acro_freq=eg.acronymcounter('/home/ps22344/Downloads/craig_0208')
# listi.append(acro_freq)

# # for x in listi:
	# # print "!!!!!\n\n", x
	
t=np.column_stack(listi)

print type(t), t.shape
completeend=time.time()

print "This took us {} minutes. So slow!".format((completeend-completestart)/60)