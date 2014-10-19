"""
Using the CSV file, update the pet, breed, shelter, and species tables as necessary to import all info in the CSV into my pets database

"""


import psycopg2
import csv

def main(filename):

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




# If I ever want to go back and refactor my code to use a more permanent dictionary, I can use either readcsv or readcsv2 as a starting place.

# def readcsv(filename):
# 	""" Read the CSV and create a dictionary where name is the key for the values (tuple)"""
# 	with open(filename, "r") as f:
# 		reader = csv.reader(f)
# 		headers = next(reader)
# 		petdictionary = {}
# 		for row in reader:			
# 			if not row: continue
# 			petdictionary[row[0]] = row[1:]
# 			print "am adding dictionary value '{}'".format(row[1:])
# 			print petdictionary.keys()
# 	return petdictionary

# def readcsv2(filename):
# # If go this route, must iterate over row in csv	
# 	with open(filename, "r") as f:
# 		petdictionary2 = csv.DictReader(f)
# 	return petdictionary2




if __name__ == "__main__":
	main('pets_to_add.csv')

