import sys
import os
import gzip
import json

# find merged rs numbers
def getRSIDs(primary_refsnp):
	rsids = []
	# append rsid reference
	rsids.append(primary_refsnp['refsnp_id'])
    # append rsid merges
	for i in primary_refsnp['dbsnp1_merges']:
		rsids.append(i['merged_rsid'])
	return rsids


# find chromosome
def getChromosome(f_in):
	return f_in.name.split('.')[0].split('-')[1][3:]


# find GRCh37 genomic position
def getPosition(primary_refsnp):
	position = ''
	for i in primary_refsnp['primary_snapshot_data']['placements_with_allele']:
		if len(i['placement_annot']['seq_id_traits_by_assembly']) > 0:
			assembly = i['placement_annot']['seq_id_traits_by_assembly'][0]['assembly_name']
			is_chrom = i['placement_annot']['seq_id_traits_by_assembly'][0]['is_chromosome']
			pos = i['alleles'][0]['allele']['spdi']['position']
			# only choose bp from GRCh37.p13
			if is_chrom == True and assembly == "GRCh37.p13":
				position = str(pos)
	return position
			

# find sequence change
def getAnnotations(primary_refsnp):
	annotations = []
	for i in primary_refsnp['allele_annotations']:
		try:
			a = i['assembly_annotation'][0]['genes'][0]['rnas'][0]['protein']['sequence_ontology'][0]['name']
			annotations.append(a.replace('_variant', '')) # clean up text by trimming off '_variant'
		except:
			continue
	return list(set(annotations))


# create tables in database
def createTables(cur):
	for i in xrange(0, 10): # 1-10 inclusive
		cur.execute("CREATE TABLE `tbl_" + str(i) + "` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	print "Table creation is completed."

# write output from parsing json files
def createRow(rsids, chromosome, position, annotations, tmp_dir, filename):
	if len(rsids) > 0:
		for rsid in rsids:
			if len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) > 0:
				writeTmp([rsid, chromosome, position, ','.join(annotations)], tmp_dir, filename)
			elif len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) == 0:
				# if no annotations, insert NA
				writeTmp([rsid, chromosome, position, 'NA'], tmp_dir, filename)
			else:
				pass

# write row to text file
def writeTmp(row, tmp_dir, filename):
    with open(tmp_dir + filename.split('.')[0] + ".out.txt", "a") as output:
    	output.write('\t'.join(row) + '\n')

def main():
    tmp_dir = "tmp/"
    filename = sys.argv[1]

    input_dir = 'json_refsnp/' 
    with gzip.open(input_dir + filename, 'rb') as f_in:
        try:
            # cnt = 0
            for line in f_in:
                try:
                    rs_obj = json.loads(line.decode('utf-8'))
                    if 'primary_snapshot_data' in rs_obj:
                        rsids = getRSIDs(rs_obj)
                        chromosome = getChromosome(f_in)
                        position = getPosition(rs_obj)
                        annotations = getAnnotations(rs_obj['primary_snapshot_data'])
                        # create and insert row into sqlite database
                        createRow(rsids, chromosome, position, annotations, tmp_dir, filename)
                        # cnt = cnt + 1
                        # if (cnt > 100):
                        #     break
                except:
                    print "there was an error with line in file: " + str(line)
        except:
            print "there was an error with input file: " + str(filename)

if __name__ == "__main__":
	main()

