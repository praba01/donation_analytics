#!/usr/bin/python
import sys
import subprocess
import datetime
import numpy as np

input_file_name                = sys.argv[1]
percentile_file_name           = sys.argv[2]
output_file_name               = sys.argv[3]

TRUE                           = 0
FALSE                          = 1
DONORZIP_YEAR                  = dict()
CMTYIDZIP_AMT                  = dict()
record_id                      = 0
lst                            = []
CNT                            = 1
TOT_AMT                        = 0

invalid_records_file           = output_file_name+".invalid"
first_time_records_file        = output_file_name+".first_time"
no_previous_year_file_name     = output_file_name+".no_previous_year"


try:
	input_file = open(input_file_name, "r")
except IOError:
	print "There was an error opening ", input_file_name
  	sys.exit()

try:
	input_file_percentile = open(percentile_file_name, "r")
except IOError:
	print "There was an error opening ", percentile_file_name
  	sys.exit()

try:
	output_file = open(output_file_name, "w")
except IOError:
	print "There was an error writing to", output_file_name
  	sys.exit()

try:
	invalid_file = open(invalid_records_file, "w")
except IOError:
	print "There was an error writing to", invalid_records_file
  	sys.exit()

try:
	first_time_file = open(first_time_records_file, "w")
except IOError:
	print "There was an error writing to", first_time_records_file
  	sys.exit()

try:
	no_previous_year_file = open(no_previous_year_file_name, "w")
except IOError:
	print "There was an error writing to", no_previous_year_file
  	sys.exit()



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
        	valid_dt =  TRUE
   	except ValueError:
        	valid_dt =  FALSE

   	if( len(OTHER) > 0 or len(ZIP) < 5      or len(NAME)    == 0 or 
            valid_dt == 1  or len(CMTY_ID) == 0 or len(TRN_AMT) == 0):

       		  return FALSE
   	else:
         	  return TRUE



def read_all_rec(CMTYID,YEAR,ZIP):
	global CNT 
        global TOT_AMT 
	global CMTYIDZIP_AMT
	global lst
	lst = []

	CNT = 1
        TOT_AMT = 0

	chk_tuple = (CMTYID,YEAR,ZIP,CNT)

	while chk_tuple in CMTYIDZIP_AMT:
		TOT_AMT = int(CMTYIDZIP_AMT[chk_tuple]) + int(TOT_AMT)	
		lst.append(CMTYIDZIP_AMT[chk_tuple])
		CNT += 1
		chk_tuple = (CMTYID,YEAR,ZIP,CNT)

     	return 


def skip_record(CMTY_ID,NAME,ZIP5,TRN_DT,TRN_AMT,OTHER):

	global DONORZIP_YEAR
	global CMTYIDZIP_AMT


    	if(valid_record(CMTY_ID,NAME,ZIP5,TRN_DT,TRN_AMT,OTHER) == FALSE):

        	rev_record = str(record_id)+"|"+CMTY_ID+"|"+ZIP5+"|"
                rev_record = rev_record+YEAR+"|"+TRN_AMT+"|"+TRN_AMT+"|1"+"\n"

        	invalid_file.write(rev_record)
    		
		return TRUE

    	if (input_tuple not in DONORZIP_YEAR): 
		DONORZIP_YEAR[input_tuple] = YEAR

        	rev_record = str(record_id)+"|"+CMTY_ID+"|"+ZIP5+"|"
                rev_record = rev_record+YEAR+"|"+TRN_AMT+"|"+TRN_AMT+"|1"+"\n"

        	first_time_file.write(rev_record)
		return TRUE
	
    	if( int(DONORZIP_YEAR[input_tuple]) >=  int(YEAR) ):

        	rev_record = str(record_id)+"|"+CMTY_ID+"|"+ZIP5+"|"
       		rev_record = rev_record+YEAR+"|"+TRN_AMT+"|"+TRN_AMT+"|1"+"\n"

        	no_previous_year_file.write(rev_record)
		return TRUE

    	if output_tuple not in CMTYIDZIP_AMT:
        	rev_record = CMTY_ID+"|"+ZIP5+"|"+YEAR+"|"+TRN_AMT+"|"
		rev_record = rev_record+TRN_AMT+"|1"+"\n"

  		output_file.write(rev_record)
		CMTYIDZIP_AMT[output_tuple] = TRN_AMT
		return TRUE

    	return FALSE


def  write_output_rec(CMTY_ID,YEAR,ZIP5,TRN_AMT):

	global CNT
	global TOT_AMT
	global CMTYIDZIP_AMT
        output_tuple                = (CMTY_ID,YEAR,ZIP5,CNT)

    	CMTYIDZIP_AMT[output_tuple] = TRN_AMT
    	TOT_AMT                    += int(TRN_AMT)
    	lst.append(TRN_AMT)
    	percentile           = calc_percentile(lst)

    	rev_record = CMTY_ID+"|"+ZIP5+"|"+YEAR+"|"
	rev_record = rev_record+str(percentile)+"|"
	rev_record = rev_record+str(TOT_AMT)+"|"+str(CNT)+"\n"

    	output_file.write(rev_record)



for line in input_file_percentile:
	PERCENTILE_VALUE = line

input_file_percentile.close()


for line in input_file:
    	lineID         = line.split("|")
    	CMTY_ID        = lineID[0]
    	NAME           = lineID[7]
    	ZIP            = lineID[10]
    	ZIP5           = ZIP[0:5]
    	TRN_DT         = lineID[13]
    	TRN_AMT        = lineID[14]
    	OTHER          = lineID[15]

    	record_id += 1
    	YEAR          = TRN_DT[4:]
    	output_tuple  = (CMTY_ID,YEAR,ZIP5,1)
    	input_tuple   = (NAME, ZIP5)

    	if(skip_record(CMTY_ID,NAME,ZIP5,TRN_DT,TRN_AMT,OTHER) == TRUE):
		continue

    	read_all_rec(CMTY_ID,YEAR,ZIP5)
    	write_output_rec(CMTY_ID,YEAR,ZIP5,TRN_AMT)



input_file.close()
output_file.close()
first_time_file.close()
no_previous_year_file.close()
invalid_file.close()
