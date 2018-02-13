# donation_analytics
insight coding challenge

Testing: I performed 3 tests;
 Test 1: 7 records provided by CC
 Test 2: I created 20 records, verified the results with insight_testsuite
 Test 3: Downloaded data file from FEC and ran the test for 1million records. I could not upload the data file because the size is 166MB. the runtime was 21seconds. insight testsuite came back with PASS. Of 21 seconds, 16 seconds were spent in reading data due to slow disk.(I determined this by just running a program to read all records).
 
 The program generates 4 output files in the output dir:
 1) repeat_donors.txt                       ===> Output file as expected by the Coding Challange
 2) repeat_donors.txt.no_previous_year      ===> This contains records with no previous year donations(with record_id)
 3) repeat_donors.txt.invalid               ===> This contains invalid records(with record_id)
 4) repeat_donors.txt.first_time            ===> This contains first time donors(with record_id)

Script Name:   donation.py
Parameters.:   3 parameters. 1) Input file containing data, 2) Input file containing Percentile value and 3)output file

Limitations:   1) No parameters validation/error handling. The program assumes the input files are in the format as expected by the program(as described by the FEC (https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml)

The program manages two dictionaries:

1) Dictionary 1: Name of donor, ZIPCODE:     Year of contribution 
2) Dictionary 2: CMTYID,ZIP,YEAR,<CNT> :     TRANSACTION_AMOUNT

What does the program do?

a) The program opens first two files for reading and third file for writing. If open fails, it abruptly ends with an error message.
b) Assigns the percentile value to be used by the program from second file and closes immediately.
c) For every record of the first file/parameter:

  i)    Assigns 6 fields that we need to local variables
  ii)   Checks in the dictionary if the donor is a repeat donor. If NAME/ZIP as key does not exist in the dictionary, it adds key/year pair to the dictionary and continues
  iii)  If repeat donor, checks if there are any records in another dictionary for key CMTYID/ZIP/YEAR/1. If no records, writes an entry into dictionary (CMTYID,ZIP,YEAR,1:TRANSACTION_AMT.
  iv) If a record with the key CMTYID,ZIP,YEAR,1 was found, it reads all records with CMTYID,ZIP,YEAR,<CNT> (WHERE CNT is an integer from 1 to number of records with CMTYID,ZIP,YEAR already found. Calculates tot_amt, number of records and running percentile of contributions received; writes the details to output file.
