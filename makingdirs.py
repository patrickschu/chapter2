import os
os.chdir("/Users/ps22344/Downloads/craig_0125")

t=['adfiles2_output_0116', 'adfiles3_output_0116', 'adfiles4_output_0116', 'adfiles_output_0116', 'files2_output_0102','files3_output_0102', 'files4_output_0102', 'files5_output_0102',
  'files8_output_0102', 'files9_output_0102', 'files_output_0101']
  
for item in t:
	os.makedirs(item)
	
print "done"
