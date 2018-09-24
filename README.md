# dbsnp
For constructing dbSNP build (151)

Built off Lon Phan's `rsjson_test.py` (lonphan@ncbi.nlm.nih.gov)

Includes script `rsjson_dbsnp.py` to parse dbSNP RS JSON object and create SQLITE database indexed by ID. 

Outputs SQLITE database: `dbsnp.151.db`
  
Each row contains rsid, chromosome, position, and function. Data will be duplicated for each of the rsid's merged rsids. 

## Running script

Create folder named `json_refsnp` in script's directory and place all compressed json `json.gz` files in folder.

Run `python refsnp_dbsnp.py` to execute the script.