import egrammartools as eg


listi=[]

emos_raw, emos_freq=eg.emoticonfinder('/home/ps22344/Downloads/craigbalanced_0601')

listi.append(emos_raw)
listi.append(emos_freq)

print "listi\n\n---", [len(i) for i in listi]

rep_raw, rep_freq= eg.repeatedpunctuationfinder('/home/ps22344/Downloads/craigbalanced_0601')

listi.append(rep_raw)
listi.append(rep_freq)


leet_raw, leet_freq= eg.leetcounter('/home/ps22344/Downloads/craigbalanced_0601')

listi.append(leet_raw)
listi.append(leet_freq)


rebfor_raw, rebfor_freq= eg.rebusfinder_for('/home/ps22344/Downloads/craigbalanced_0601')


listi.append(rebfor_raw)
listi.append(rebfor_freq)

print "\n\n---", [len(i) for i in listi]


rebto_raw, rebto_freq= eg.rebusfinder_to('/home/ps22344/Downloads/craigbalanced_0601')

rebtoo_raw, rebtoo_freq= eg.rebusfinder_too('/home/ps22344/Downloads/craigbalanced_0601')

caps_raw, caps_freq=eg.capsfinder('/home/ps22344/Downloads/craigbalanced_0601', 0.5)

single_raw, single_freq=eg.singleletterfinder('/home/ps22344/Downloads/craigbalanced_0601')

cli_raw, clip_freq=eg.clippingcounter('/home/ps22344/Downloads/craigbalanced_0601')

acro_raw, acro_freq=eg.acronymcounter('/home/ps22344/Downloads/craigbalanced_0601')
