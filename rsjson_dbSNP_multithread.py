import json
import gzip
import os
import sqlite3
import subprocess
import time
start_time = time.time() # measure script's run time


# create tables in database
def createTables(cur):
	for i in xrange(0, 10): # 1-10 inclusive
		cur.execute("CREATE TABLE `tbl_" + str(i) + "` (`id` INTEGER, `chromosome` TEXT, `position` TEXT, `function` TEXT);")
	print "Table creation is completed."


# index database by id after insertions completed
def indexDB(cur):
	for i in xrange(0, 10): # 1-10 inclusive
		cur.execute("CREATE INDEX `index_" + str(i) + "` ON `tbl_" + str(i) + "` ( `id` );")

		# "CREATE INDEX `index_%s` ON `tbl_%s` ( `id` );" % (i, i)
	print "Table indexing is completed."


def createSubprocess(filename):
	args = ["python", "rsjson_dbSNP_sub.py", filename]
	process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return process


def insertRows(tmp_dir, cur):
	for filename in os.listdir(tmp_dir):
		with open(tmp_dir + filename) as fp:
			lines = fp.readlines()
			for row in lines:
				id, chr, bp, funct = row.split('\t')
				temp = (id, chr, bp, funct)
				# Insert data rows
				cur.execute("INSERT INTO tbl_"+id[-1]+" VALUES (?,?,?,?)", temp)
	print "Table insertion is completed."


def main():
	tmp_dir = "tmp/"
	# create tmp directory
	if not os.path.exists(tmp_dir):
		os.makedirs(tmp_dir)

	# iterate through each file in directory
	input_dir = 'json_refsnp/'
	processes = []
	for filename in os.listdir(input_dir):
		print "start subprocess for: " + filename.split('.')[0]
		# create subprocess for each file
		processes.append(createSubprocess(filename))

	exit_codes = [p.wait() for p in processes]
	print exit_codes
	if (len(exit_codes) == 24 and all(x == 0 for x in exit_codes)):
		print "success! :)"
		# create database
		con = sqlite3.connect("dbsnp.rs.151.db")
		with con:
			# Create cursor object
			con.text_factory = str
			cur = con.cursor()
			# create tables
			createTables(cur)
			# insert rows into tables
			insertRows(tmp_dir, cur)
			# index sqlite database by id once insertions are completed
			indexDB(cur)
			print "dbSNP 151 completed!"
		# Close the connection
		con.close()
	else:
		print "failure! :("
	
	# print script's run time when finshed
	print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
	main()

