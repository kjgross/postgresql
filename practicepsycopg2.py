"""
- opens and parses the CSV file, creating a dictionary of items to be inserted into the database.
- inserts a new row in the Pet table for each entry in the dictionary (NULL for missing values)
- Any breeds, species, or shelters that appear in the CSV that are NOT already in the database should be added.
- Your script will need to normalize for capitalization.
- think about what will be the most efficient in terms of making the fewest queries to the database.
"""

"""
1. Create the try to connect, except area
2. Define a cursor
3. Within the cursor, execute a query
4. Use a variable name to fetch them all back

"""
import psycopg2
import csv

try:
	conn=psycopg2.connect("dbname='pets'")
except:
	print "I am unable to connect to the database."

cur = conn.cursor()
try: 
## Why do these only return one column? There should be many columns returned.
	#cur.execute("""SELECT * from breed left outer join species on breed.species_id = species.id """)
	#cur.execute("""SELECT s.speciesname, s.species_id, b.breedname, b.id from species s join breed b on species.id = breed.species_id """)
	cur.execute("Select * from breed")
except:
	print "I can't SELECT from person."

rows = cur.fetchall()
print "\nRows: \n"
for row in rows:
	print "  ", row[1]

def readcsv(filename):
	""" Read the CSV and create a dictionary where name is the key for the values (tuple)"""
	with open(filename, "r") as f:
		reader = csv.reader(f)
		petdictionary = {}
## Need to skip the header row
		for row in reader:
			petdictionary[row[0]] = row[1:]
			print "am adding dictionary value '{}'".format(row[1:])
			print petdictionary.keys()
	return petdictionary

# ## In this section, I'll need to do capitalization normalization.

def addnewspecies(speciesname, filename):
	""" Add new species if it's not already in our system"""
	if cur.execute("select * from species where name = speciesname") == '':
		try:
			cur.execute("insert into species (name) values ('speciesname')")
			print "Adding '{}' to our db.".format(speciesname)
		except:
			print "Couldn't insert into species"
	else:
		print "'{}' is already a species in our db.".format(speciesname)

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



def main():
	#newdata = raw_input("what file do you want to insert?")
	print "welcome"
	#addnewspecies('fish',"pets_to_add.csv")
	readcsv("pets_to_add.csv")
	print "just read that guy"
	print petdictionary.keys()
	print "bye bye"
	#addnewspecies(species, newdata)
	#addnewbreed(breed, species, newdata)
	#addnewshelter(sheltername, newdata)



if __name__ == "__main__":
	main()

