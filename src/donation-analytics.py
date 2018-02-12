#!/usr/bin/python
import sys
import subprocess
import datetime
import numpy as np

input_file_name           = sys.argv[1]
percentile_file_name       = sys.argv[2]
output_file_name          = sys.argv[3]
try:
  input_file = open(input_file_name, "r")
except IOError:
  print "There was an error opening ", file_name
  sys.exit()

try:
  input_file_percentile = open(percentile_file_name, "r")
except IOError:
  print "There was an error opening ", file_name
  sys.exit()

try:
  output_file = open(output_file_name, "w")
except IOError:
  print "There was an error writing to", output_file_name
  sys.exit()

for line in input_file_percentile:
	PERCENTILE_VALUE = line

input_file_percentile.close()


def calc_percentile(curr_list):
        n = len(curr_list)
	curr_list.sort()
     	ord_rank = (float(PERCENTILE_VALUE)/float(100)) * n
        if (ord_rank < 1):
            return curr_list[0]
        ord_rank_dec = ord_rank // 1

	if (ord_rank  - ord_rank_dec < 0.5):
            idx = ord_rank_dec - 1
	else:
            idx = ord_rank_dec 
        return curr_list[int(idx)]


def valid_record(CMTY_ID,NAME,ZIP,DT,TRN_AMT,OTHER):
   try:
        datetime.datetime.strptime(DT, '%m%d%Y')
        valid_dt=0
   except ValueError:
        valid_dt=1

   if( len(OTHER) > 0 or len(ZIP) < 5 or len(NAME) == 0 or valid_dt == 1 or len(CMTY_ID) == 0 or len(TRN_AMT) == 0):
         return 1
   else:
         return 0

input = dict()
output = dict()


def read_all_rec(CMTYID,YEAR,ZIP):
	global CNT 
	global TOT_AMT 
	global lst 
    	lst = []
        CNT = 1
        TOT_AMT = 0
	chk_tuple = (CMTYID,YEAR,ZIP,CNT)
	while chk_tuple in output:
		TOT_AMT = int(output[chk_tuple]) + int(TOT_AMT)	
		lst.append(output[chk_tuple])
		CNT += 1
		chk_tuple = (CMTYID,YEAR,ZIP,CNT)

     	return TOT_AMT, CNT



for line in input_file:
    lineID         = line.split("|")
    CMTY_ID        = lineID[0]
    NAME           = lineID[7]
    ZIP            = lineID[10]
    ZIP5           = ZIP[0:5]
    TRN_DT         = lineID[13]
    TRN_AMT        = lineID[14]
    OTHER          = lineID[15]

    if(valid_record(CMTY_ID,NAME,ZIP5,TRN_DT,TRN_AMT,OTHER) != 0):
        continue

    YEAR          = TRN_DT[4:]
    output_tuple  = (CMTY_ID,YEAR,ZIP5,1)
    input_tuple   = (NAME, ZIP5)

    if (input_tuple not in input): 
	input[input_tuple] = YEAR
        continue
        
    if( int(input[input_tuple]) >=  int(YEAR) ):
	continue

    if output_tuple not in output:
        rev_record = CMTY_ID+"|"+ZIP5+"|"+YEAR+"|"+TRN_AMT+"|"+TRN_AMT+"|1"+"\n"
  	output_file.write(rev_record)
	output[output_tuple] = TRN_AMT
	continue

    read_all_rec(CMTY_ID,YEAR,ZIP5)
    output_tuple         = (CMTY_ID,YEAR,ZIP5,CNT)
    output[output_tuple] = TRN_AMT
    TOT_AMT             += int(TRN_AMT)
    lst.append(TRN_AMT)
    percentile           = calc_percentile(lst)
    rev_record = CMTY_ID+"|"+ZIP5+"|"+YEAR+"|"+str(percentile)+"|"+str(TOT_AMT)+"|"+str(CNT)+"\n"
    output_file.write(rev_record)

input_file.close()
output_file.close()
