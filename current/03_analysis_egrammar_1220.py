import egrammartools as eg
import numpy as np

listi=[]

emos_raw, emos_freq=eg.emoticonfinder('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(emos_freq)

rep_raw, rep_freq= eg.repeatedpunctuationfinder('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(rep_freq)


leet_raw, leet_freq= eg.leetcounter('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(leet_freq)


rebfor_raw, rebfor_freq= eg.rebusfinder_for('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(rebfor_freq)

rebto_raw, rebto_freq= eg.rebusfinder_to('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(rebto_freq)

rebtoo_raw, rebtoo_freq= eg.rebusfinder_too('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(rebtoo_freq)

caps_raw, caps_freq=eg.capsfinder('/home/ps22344/Downloads/craigbalanced_0601', 0.5)
listi.append(caps_freq)

single_raw, single_freq=eg.singleletterfinder('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(single_freq)

clip_raw, clip_freq=eg.clippingcounter('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(clip_freq)

acro_raw, acro_freq=eg.acronymcounter('/home/ps22344/Downloads/craigbalanced_0601')
listi.append(acro_freq)

# for x in listi:
	# print "!!!!!\n\n", x
	
t=np.column_stack(listi)

#print t.shape
