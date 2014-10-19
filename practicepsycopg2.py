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



import psycopg2
import csv

def main2(filename):

	with open(filename, "r") as f:

		reader = csv.DictReader(f, skipinitialspace = True)

		conn=psycopg2.connect("dbname='pets'")
		cur = conn.cursor()

		for row in reader:
			print "going through a new pet"
			# add the name into pet, creating the new row
			cur.execute("INSERT INTO pet (name) VALUES (%(Name)s) RETURNING id", row)
			rowpet_id = cur.fetchone()

			# add age if it exists
			if row["age"]:
				cur.execute("UPDATE pet SET age = (%(age)s) WHERE id = (%(id)s)", {'age': row["age"], 'id': rowpet_id})

			# add adopted if it exists
			if row["adopted"]:
				cur.execute("UPDATE pet SET adopted = (%(adopted)s) WHERE id = (%(id)s)", {'adopted': row["adopted"], 'id': rowpet_id})

			# add the shelter id if it exists
			if row["shelter name"]:
				cur.execute("SELECT id from shelter WHERE UPPER(name) = UPPER(%(sheltername)s)", {'sheltername':row["shelter name"]})
				if not cur.fetchone():
					cur.execute("INSERT INTO shelter (name) VALUES (%(sheltername)s) RETURNING id", {'sheltername':row["shelter name"]})
				cur.execute("UPDATE pet SET shelter_id = (SELECT id from shelter WHERE UPPER(name) = UPPER(%(sheltername)s)) WHERE id = (%(id)s)", {'sheltername':row['shelter name'], 'id': rowpet_id})

			# If species name not in species, add that. 
			# Then, if breed name not in breed, add that with its species id. Finally update pet.
			if row["species name"]:
				cur.execute("SELECT id from species WHERE UPPER(name) = UPPER(%(speciesname)s)", {'speciesname':row["species name"]})
				if not cur.fetchone():
					cur.execute("INSERT INTO species (name) VALUES (%(speciesname)s) RETURNING id", {'speciesname':row["species name"]})

			if row["breed name"]:
				cur.execute("SELECT id from breed WHERE UPPER(name) = UPPER(%(breedname)s)", {'breedname':row["breed name"]})
				if not cur.fetchone():
					cur.execute("INSERT INTO breed (name, species_id) VALUES (%(breedname)s, SELECT id FROM species WHERE UPPER(name) = UPPER(%(speciesname)s))", {'breedname':row['breed name'], 'speciesname':row['species name']})
				
			if row["breed name"] and row["species name"]:
				print "I SHOULD BE UPDATING PETS"
				cur.execute("SELECT id from breed WHERE UPPER(name) = UPPER(%(breedname)s)", {'breedname':row['breed name']})
				rowbreed_id = cur.fetchone()
				cur.execute("UPDATE pet SET breed_id = (%(breedid)s) where id = (%(id)s)", {'breedid':rowbreed_id, 'id':rowpet_id})


			conn.commit()
			print "Done with that pet"

	cur.close()
	conn.close()
















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
# If go this route, must iterate over row in csv	
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
# con.commit
	print "query done, check your db"
	#addnewspecies(species, newdata)
	#addnewbreed(breed, species, newdata)
	#addnewshelter(sheltername, newdata)





if __name__ == "__main__":
	main2('pets_to_add.csv')

