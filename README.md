# dbsnp
For constructing dbSNP build (151)

Built off Lon Phan's `rsjson_test.py` (lonphan@ncbi.nlm.nih.gov)

Includes script `rsjson_dbsnp.py` to parse dbSNP RS JSON object. 
Writes output to text file: `chr_<chromosome of input file>.txt`
  
Each row contains rsid, chromosome, position, and function. Data will be duplicated for each of the rsid's merged rsids. 

## Running script

Run `python refsnp_dbsnp.py -i refsnp-sample.json.gz` to execute the script on included sample input file.