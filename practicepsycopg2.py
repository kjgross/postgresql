"""
- opens and parses the CSV file, creating a dictionary of items to be inserted into the database.
- inserts a new row in the Pet table for each entry in the dictionary (NULL for missing values)
- Any breeds, species, or shelters that appear in the CSV that are NOT already in the database should be added.
- Your script will need to normalize for capitalization.
- think about what will be the most efficient in terms of making the fewest queries to the database.
"""

"""
1. Connect to database
2. Define a cursor
3. Within the cursor, execute a query
4. Use a variable name to fetch them all back

"""

import psycopg2
import csv

conn=psycopg2.connect("dbname='pets'")
cur = conn.cursor()

## This code is for making sure my connection is sound. It now works!
# try: 
# 	#cur.execute("""SELECT * from breed left outer join species on breed.species_id = species.id """)
# 	#cur.execute("""SELECT s.speciesname, s.species_id, b.breedname, b.id from species s join breed b on species.id = breed.species_id """)
# 	#cur.execute("Select * from breed")
# except:
# 	print "I can't SELECT from person."

# rows = cur.fetchall()
# print "\nRows: \n"
# for row in rows:
# 	print "  ", row

def readcsv(filename):
	""" Read the CSV and create a dictionary where name is the key for the values (tuple)"""
	with open(filename, "r") as f:
		reader = csv.reader(f)
		headers = next(reader)
		petdictionary = {}
		for row in reader:			
			if not row: continue
			petdictionary[row[0]] = row[1:]
			print "am adding dictionary value '{}'".format(row[1:])
			print petdictionary.keys()
	return petdictionary

def readcsv2(filename):
	with open(filename, "r") as f:
		petdictionary2 = csv.DictReader(f)
	return petdictionary2


"""
Headers looks like:
{'Name': ['age', 'breedname', 'species name', 'shelter name', 'adopted']}
Dictionary looks like"
{'Titchy': ['12','mixed','cat','BCSPCA', '1'], 
'Ginger': ['1', 'labradoodle', 'dog', '', '1'],
etc., }

I think I want my dictionary to look like (dictionary of dictionaries):
petdictionary = {
"Titchy": {Name": "Titchy", "age": "12", "breedname": "mixed", "species name": "cat", "shelter name": "BCSPCA", "adopted":"1"}
,"Ginger": {"Name":Ginger", "age":"1", "breedname": "labradoodle", "species name": "dog", "shelter name": "", "adopted":"1"}
 }
"""

def main():
	#newdata = raw_input("what file do you want to insert?")
	print "welcome"
	#addnewspecies('fish',"pets_to_add.csv")
	#petdictionary1 = readcsv("pets_to_add.csv")
	petdictionary2 = readcsv2("pets_to_add.csv")
	"""
	petdictionary1 = {"Titchy":{"Name": "Titchy", "age": "12", "breedname": "mixed", "species name": "cat", "shelter name": "BCSPCA", "adopted": "1"},
"Ginger":{"Name": "Ginger", "age": "1", "breedname": "labradoodle", "species name": "dog", "shelter name": "", "adopted": "1"}
}
"""
	print "just read that guy"
	for line in petdictionary2:
		print line["Name"]
	print "query time"
## This isn't inserting..  but it runs ok.
	#query = ('insert into pet (name, age, adopted) VALUES (%(Name)s, %(age)s, %(adopted)s)') 
	#cur.execute(query, petdictionary1["Titchy"])

## code runs, but nothing is actually inserted
	cur.execute("INSERT INTO pet (name) VALUES (%s)", ('speckles',))

	print "query done, check your db"
	#addnewspecies(species, newdata)
	#addnewbreed(breed, species, newdata)
	#addnewshelter(sheltername, newdata)




def addpetname(headers, petdictionary):
	pass
	#namequery = ('insert into pet (%s) Values (%s)' % (name, Name))
	# petdictionary has columns: 
	# Name, age, breed name, species name, shelter name, adopted
	# pet table has columns:
	#  id | name | age | adopted | dead | breed_id | shelter_id

	# Name, age, adopted I can fill in without checking anything
	# ID will be determined on inserting the first time
	# dead will stay null
	# species_id will have to be determined based on species name (tho not inserted, still need to do to make breed work properly)
	# then breed_id will have to be determined based on breed name
	# shelter id will be determined by shelter name

	












# ## In this section, I'll need to do capitalization normalization.

# def addnewspecies(speciesname, filename):
# 	""" Add new species if it's not already in our system"""
# 	sqlquery = "select * from %s where %s = speciesname"
# 	cur.executemany("""INSERT INTO species(name) VALUES (%(speciesname)s)""", petdictionary)



# 	if cur.execute(sqlquery, species, speciesname) == '':
# 		try:
# 			#cur.execute("""insert into species (name) values (%(speciesname)s)""",petdictionary)
# 			print "Adding '{}' to our db.".format(speciesname)
# 		except:
# 			print "Couldn't insert into species"
# 	else:
# 		print "'{}' is already a species in our db.".format(speciesname)

# def addnewbreed(breedname, species, filename):
# 	""" Add new breed if it's not already in our system"""
# 	if cur.execute("select * from breed where name = breedname") == '':
# 		try:
#			cur.execute("insert into breed (name, species_id) values ('breedname', (select id from species where name = species)")
#			print "Adding '{}' to our db.".format(breedname)
#		except:
#			print "Couldn't insert into breed"
# 	else:
# 		print "'{}' is already a breed in our db.".format('breedname')


# def addnewshelter(sheltername, filename):
# 	""" Add new shelter if it's not already in our system"""
# 	if cur.execute("select * from shelter where name = sheltername") == '':
#		try:
# 			cur.execute("insert into shelter (name) values ('sheltername')")
#			print "Adding '{}' to our db.".format(sheltername)
#		except:
#			print "Couldn't insert into shelter"
# 	else:
# 		print "'{}' is already a species in our db.".format(sheltername)



# def write():
# 	""" Write the contents of the dictionary out to new rows in the pets DB"""
# 	# Will use new breed/species foreign keys created in checkfornewcontent()







if __name__ == "__main__":
	main()

