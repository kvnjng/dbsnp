import argparse
import json
import gzip
import csv
import os

import time
start_time = time.time() # measure script's run time

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
			if is_chrom == True and assembly == "GRCh37.p13":
				# assemblies.append("=".join([assembly,str(position)]))
				position = str(pos)
	return position
			

# find sequence change
def getAnnotations(primary_refsnp):
	annotations = []
	for i in primary_refsnp['allele_annotations']:
		try:
			a = i['assembly_annotation'][0]['genes'][0]['rnas'][0]['protein']['sequence_ontology'][0]['name']
			annotations.append(a.replace('_variant', ''))
		except:
			continue
	return list(set(annotations))


def writeOutput(rsids, chromosome, position, annotations):
	# print rsids
	# print position
	# print annotations
	# print ""
	with open('chr_' + chromosome + '.txt', 'a') as f:
		# if len(rsids) > 0 and len(position) > 0 and len(annotations) > 0:
		# 	f.write('\t'.join([','.join(rsids), position, ','.join(annotations)]) + '\n')
		# elif len(rsids) > 0 and len(position) > 0 and len(annotations) == 0:
		# 	f.write('\t'.join([','.join(rsids), position]) + '\n')
		# else:
		# 	pass
		if len(rsids) > 0:
			for rsid in rsids:
				if len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) > 0:
					f.write('\t'.join([rsid, chromosome, position, ','.join(annotations)]) + '\n')
				elif len(rsid) > 0 and len(chromosome) > 0 and len(position) > 0 and len(annotations) == 0:
					f.write('\t'.join([rsid, chromosome, position]) + '\n')
				else:
					pass

# main

# iterate through each file in directory
input_dir = 'json_refsnp/'
for filename in os.listdir(input_dir):
	cnt = 0
	with gzip.open(input_dir + filename, 'rb') as f_in:
		for line in f_in:
			rs_obj = json.loads(line.decode('utf-8'))
			if 'primary_snapshot_data' in rs_obj:
				# print rs_obj['refsnp_id']
				rsids = getRSIDs(rs_obj)
				chromosome = getChromosome(f_in)
				position = getPosition(rs_obj)
				annotations = getAnnotations(rs_obj['primary_snapshot_data'])
				writeOutput(rsids, chromosome, position, annotations)
				# print("")
			cnt = cnt + 1
			if (cnt > 20):
				break

print("--- %s seconds ---" % (time.time() - start_time)) # measure script's run time