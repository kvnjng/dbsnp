import json
import gzip
import os
import sqlite3
import time
start_time = time.time() # measure script's run time

# create database
con = sqlite3.connect("dbsnp.151.db")

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
	cur.execute("CREATE TABLE `tbl_0` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_1` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_2` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_3` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_4` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_5` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_6` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_7` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_8` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	cur.execute("CREATE TABLE `tbl_9` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	print "Table creation is completed."

# write output from parsing json files
def createRow(rsids, chromosome, position, annotations, cur):
	if len(rsids) > 0:
		for rsid in rsids:
			if len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) > 0:
				writeDB([rsid, chromosome, position, ','.join(annotations)], cur)
			elif len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) == 0:
				# if no annotations, insert NA
				writeDB([rsid, chromosome, position, 'NA'], cur)
			else:
				pass


# write row to sqlite database
def writeDB(row, cur):
	id, chr, bp, funct = row
	temp = (id, chr, bp, funct)
	# Insert data rows
	cur.execute("INSERT INTO tbl_"+id[-1]+" VALUES (?,?,?,?)", temp)


# index database by id after insertions completed
def indexDB(cur):
	cur.execute("CREATE INDEX `index_0` ON `tbl_0` ( `id` );")
	cur.execute("CREATE INDEX `index_1` ON `tbl_1` ( `id` );")
	cur.execute("CREATE INDEX `index_2` ON `tbl_2` ( `id` );")
	cur.execute("CREATE INDEX `index_3` ON `tbl_3` ( `id` );")
	cur.execute("CREATE INDEX `index_4` ON `tbl_4` ( `id` );")
	cur.execute("CREATE INDEX `index_5` ON `tbl_5` ( `id` );")
	cur.execute("CREATE INDEX `index_6` ON `tbl_6` ( `id` );")
	cur.execute("CREATE INDEX `index_7` ON `tbl_7` ( `id` );")
	cur.execute("CREATE INDEX `index_8` ON `tbl_8` ( `id` );")
	cur.execute("CREATE INDEX `index_9` ON `tbl_9` ( `id` );")
	print "Table indexing is completed."


def main():
	# Automatically commit changes
	with con:
		# Create cursor object
		con.text_factory = str
		cur = con.cursor()
		# create tables
		createTables(cur)
		# iterate through each file in directory
		input_dir = 'json_refsnp/'
		for filename in os.listdir(input_dir):
			# cnt = 0
			with gzip.open(input_dir + filename, 'rb') as f_in:
				for line in f_in:
					rs_obj = json.loads(line.decode('utf-8'))
					if 'primary_snapshot_data' in rs_obj:
						rsids = getRSIDs(rs_obj)
						chromosome = getChromosome(f_in)
						position = getPosition(rs_obj)
						annotations = getAnnotations(rs_obj['primary_snapshot_data'])
						# create and insert row into sqlite database
						createRow(rsids, chromosome, position, annotations, cur)
					# cnt = cnt + 1
					# if (cnt > 500):
					# 	break
		print "Table insertion is completed."
		# index sqlite database by id once insertions are completed
		indexDB(cur)
	# Close the connection
	con.close()
	# print script's run time when finshed
	print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
	main()

