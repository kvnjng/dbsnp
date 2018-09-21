# Import Library
import csv,subprocess,sqlite3

# Create database
con = sqlite3.connect("C:\\Users\\jiangk3\\Desktop\\build dbSNP 151\\mitch json scripts\\snp151.db")

# Find RS Number
def get_coords(id):
	t=(id,)
	cur.execute("SELECT * FROM tbl_"+id[-1]+" WHERE id=?", t)
	return cur.fetchone()


# Automatically commit changes
with con:
	
	# Create cursor object
	con.text_factory = str
	cur=con.cursor()
	
	
	# Extract Merged SNP RS Numbers
	merged = open("C:\\Users\\jiangk3\\Desktop\\build dbSNP 151\\mitch json scripts\\chr21.txt").readlines()
	
	for snp_raw in merged:
		record = snp_raw.strip().split("\t")
		# id_old = snp[0]
		# id_new = snp[1]

		# print snp
		
		# record = get_coords(id_new)

		# print record
		
		# if record != None:
		if len(record) > 3:
			id, chr, bp, funct = record
			temp = (id, chr, bp, funct)
			# Insert data rows
			cur.execute("INSERT INTO tbl_"+id[-1]+" VALUES (?,?,?,?)", temp)
		else:
			id, chr, bp = record
			temp = (id, chr, bp, "NA")
			# Insert data rows
			cur.execute("INSERT INTO tbl_"+id[-1]+" VALUES (?,?,?,?)", temp)
	
	print "Updating table is completed."

	# Create index
	sql=("CREATE INDEX `index_0` ON `tbl_0` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_1` ON `tbl_1` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_2` ON `tbl_2` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_3` ON `tbl_3` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_4` ON `tbl_4` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_5` ON `tbl_5` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_6` ON `tbl_6` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_7` ON `tbl_7` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_8` ON `tbl_8` ( `id` );")
	cur.execute(sql)
	sql=("CREATE INDEX `index_9` ON `tbl_9` ( `id` );")
	cur.execute(sql)
	print "Table indexing is completed."

# Close the connection
con.close()