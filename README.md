# dbsnp
For constructing dbSNP build (151)

Built off Lon Phan's `rsjson_test.py` (lonphan@ncbi.nlm.nih.gov)

Includes script `rsjson_dbsnp.py` to parse dbSNP RS JSON object and create SQLITE database indexed by ID. 

- Outputs SQLITE database: `dbsnp.rs.151.db`

Includes script `chrjson_dbsnp.py` to parse dbSNP RS JSON object and create SQLITE database indexed by chromosome. 

- Outputs SQLITE database: `dbsnp.chr.151.db`
  
Each row contains rsid, chromosome, position, and function. Data will be duplicated for each of the rsid's merged rsids. 

## Running script

Create folder named `json_refsnp` in script's directory and place all compressed json `json.gz` files in folder.

Run `python rsjson_dbSNP.py` to execute the script to build SQLite database indexed by RS number.

Run `python chrjson_dbSNP.py` to execute the script to build SQLite database indexed by chromosome.