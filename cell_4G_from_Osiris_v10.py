#!/usr/bin/python
import csv     # imports the csv module
import sys      # imports the sys module
import time
import pyproj
from pyproj import Geod
g = Geod(ellps='WGS84')
wgs84 = pyproj.Proj("+init=EPSG:4326")
#lambert = pyproj.Proj('+proj=lcc +nadgrids=ntf_r93.gsb,null +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=44.100000000 +lon_0=0.000000000 +k_0=0.99987750 +lat_1=44.100000000 +x_0=600000.000 +y_0=3200000.000 +units=m +no_defs')
#lambert = pyproj.Proj('+title=Lambert II etendu +proj=lcc +nadgrids=ntf_r93.gsb,null +wktext +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=46.800000000 +lon_0=0.000000000 +k_0=0.99987742 +lat_1=46.800000000 +x_0=600000.000 +y_0=2200000.000 +units=m +no_defs')

lambert = pyproj.Proj('+title=Lambert II etendu +proj=lcc +nadgrids=ntf_r93.gsb,null +wktext +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=46.800000000 +lon_0=0.000000000 +k_0=0.99987742 +lat_1=46.800000000 +x_0=600000.000 +y_0=2200000.000 +units=m +no_defs')
e = pyproj.Proj('+init=IGNF:LAMBE')
file_json = open("geo4G_Osiris.json",'w')
f = open(sys.argv[1], 'r') # opens the csv file
file_badRecords = open("geo4G_Osiris_badRec.csv", 'wb')
nbRowCSV = 0
nbRowWithoutLAC = 0
nbRowWithoutLati = 0
nbAzimutNotDigit = 0
listValeurFreq800 = ["LTE800"]
listValeurFreq1800 = ["LTE1800"]
listValeurFreq2600 = ["LTE2600"]
dbTime = time.strftime("%d%m%Y")
print("Debut traitement fichier CSV")
try:
	reader = csv.reader(f,delimiter=';')  # creates the reader object
	writer = csv.writer(file_badRecords,delimiter=';')
	next(reader, None)	# vire premiere ligne
	for row in reader:   # iterates the rows of the file in orders
		# pointeurs colonnes fichiers CSV
		TAC = row[12]
		LAC = row[38]
		CellID_fourni = long(row[13])
		cellName = row[11]
		coordX = row[4]
		coordY = row[5]
		azimut = row[18]
		address = ""
		bande = row[17]
		addressComplement = ""
		city = row[43]
		postalCode = row[42]
		frequency = row[17]
		nbRowCSV = nbRowCSV + 1	
		if LAC == "":	# cellule en construction Pas de LAC
			nbRowWithoutLAC = nbRowWithoutLAC + 1
			writer.writerow((nbRowCSV,row))
			continue
		if coordX == "":
			nbRowWithoutLati = nbRowWithoutLati + 1
			writer.writerow((nbRowCSV,row))
			continue
		if not azimut.isdigit() :
			nbAzimutNotDigit = nbAzimutNotDigit + 1
			writer.writerow((nbRowCSV,row))
			continue
		CellID = CellID_fourni
		if CellID_fourni > 65535 :
			CellID = CellID_fourni%65536
		lat=coordX.decode('ascii', 'ignore')
		longi=coordY.decode('ascii', 'ignore')
		lat=lat.replace(' ','')
		longi=longi.replace(' ','')
		lat=lat.replace(',','')
		longi=longi.replace(',','')
		# MODIF ERIC => sert a virer 2 derniers 0 
		if  len(lat)>7 :
			lat=lat[:-2].decode('ascii', 'ignore')
			longi=longi[:-2].decode('ascii', 'ignore')
		# pas vu l info dans fichier csv 
		radius=5000
		if frequency in listValeurFreq2600:
			# radius=2200
			frequency="2600"
		elif frequency in listValeurFreq1800:
			# radius=4500
			frequency="1800"
		elif frequency in listValeurFreq800:
			# radius=4500
			frequency="800"				
		orig_x,orig_y=pyproj.transform(e, wgs84,lat,longi)
		left_x,left_y,trash= g.fwd(orig_x,orig_y, int(azimut)-60, radius*0.8)
		right_x,right_y,trash= g.fwd(orig_x,orig_y, int(azimut)+60, radius*0.8)
		center_x,center_y,trash= g.fwd(orig_x,orig_y, azimut, radius)
		#creation ligne dans fichier JSON SANS complement adresse
		file_json.write("{\"TAC\" : "+ str(TAC) +",\"LAC\" : "+ str(LAC) +", \"CI\" :"+str(CellID)+", \"dbTime\" : "+ str(dbTime) + ", \"frequency\" : \""+ str(frequency) + "\",  \"RAT\" : \""+sys.argv[2]+"\", \"name\" : \""+cellName+"\",\"addr\" :\""+str(address).replace("\"", "").replace("\\", "-")+"\", \"code\" :\""+postalCode+"\", \"city\" :\""+str(city)+"\", \"antenna\" :["+str(orig_x)+","+str(orig_y)+"],  \"loc\" : { \"type\" : \"Polygon\", \"coordinates\" : [[["+str(orig_x)+","+str(orig_y)+ "],["+str(left_x)+","+str(left_y)+ "],["+str(center_x)+","+str(center_y)+ "],["+str(right_x)+","+str(right_y)+ "],["+str(orig_x)+","+str(orig_y)+ "]]] } }\n")	 
finally:
	print ('nbRowCSV =', nbRowCSV)
	print ('nbRowWithoutLAC =', nbRowWithoutLAC)
	print ('nbRowWithoutLati =', nbRowWithoutLati)
	print ('nbAzimutNotDigit =', nbAzimutNotDigit)
	f.close()      # closing
	file_json.close()
	file_badRecords.close()
	print("fin traitement fichier CSV")
