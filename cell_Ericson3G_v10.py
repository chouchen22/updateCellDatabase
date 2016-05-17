#!/usr/bin/python
import csv     # imports the csv module
import sys      # imports the sys module
#import codecs
import pyproj
import time
from pyproj import Geod
g = Geod(ellps='WGS84')
wgs84 = pyproj.Proj("+init=EPSG:4326")
#lambert = pyproj.Proj('+proj=lcc +nadgrids=ntf_r93.gsb,null +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=44.100000000 +lon_0=0.000000000 +k_0=0.99987750 +lat_1=44.100000000 +x_0=600000.000 +y_0=3200000.000 +units=m +no_defs')
#lambert = pyproj.Proj('+title=Lambert II etendu +proj=lcc +nadgrids=ntf_r93.gsb,null +wktext +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=46.800000000 +lon_0=0.000000000 +k_0=0.99987742 +lat_1=46.800000000 +x_0=600000.000 +y_0=2200000.000 +units=m +no_defs')

lambert = pyproj.Proj('+title=Lambert II etendu +proj=lcc +nadgrids=ntf_r93.gsb,null +wktext +towgs84=-168.0000,-60.0000,320.0000 +a=6378249.2000 +rf=293.4660210000000 +pm=2.337229167 +lat_0=46.800000000 +lon_0=0.000000000 +k_0=0.99987742 +lat_1=46.800000000 +x_0=600000.000 +y_0=2200000.000 +units=m +no_defs')
e = pyproj.Proj('+init=IGNF:LAMBE')
file_json = open("geo3gericson.json",'w')
f = open(sys.argv[1], 'r') # opens the csv file
file_badRecords = open("Ericson3G_badRecords.csv", 'w')
nbRowCSV = 0
nbRowWithoutLati = 0
nbAzimutNotDigit = 0
listValeurFreq900 = ["1", "p-gsm", "e-gsm", "900", "U900", "U2100/U900", "2950", "3011", "3075"]
listValeurFreq2100 = ["4", "1800", "dcs1800", "U2100", "3011", "10564", "10639", "10712", "10787", "10812", "10836"]	
dbTime = time.strftime("%d%m%Y")
print("Debut traitement fichier CSV")
try:
	reader = csv.reader(f,delimiter=';')  # creates the reader object
	writer = csv.writer(file_badRecords,delimiter=';')
	next(reader, None)	# vire premiere ligne
	for row in reader:   # iterates the rows of the file in orders
		# pointeurs colonnes fichiers CSV
		LAC = row[6]
		TAC = 0
		CellID_fourni = row[16]
		cellName = row[24]
		coordX = row[41]
		coordY = row[42]
		azimut = row[67]
		address = row[19]
		#addressComplement = row[]
		city = row[21]
		postalCode = row[20]
		frequency = row[62]
		nbRowCSV = nbRowCSV + 1	
		if coordX == "":
			nbRowWithoutLati = nbRowWithoutLati + 1
			writer.writerow((nbRowCSV,row))
			continue
		if not azimut.isdigit() :
			nbAzimutNotDigit = nbAzimutNotDigit + 1
			writer.writerow((nbRowCSV,row))
			continue
		CellID = CellID_fourni
		if int(CellID_fourni) > 65535 :
			CellID = int(CellID_fourni)
			CellID = hex(CellID)
			CellID = int(CellID[-4:],16)
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
		radius=1000
		if frequency in listValeurFreq2100:
			radius=4400
			frequency="2100"
		elif frequency in listValeurFreq900:
			radius=9000
			frequency="900"
		orig_x,orig_y=pyproj.transform(e, wgs84,lat,longi)
		left_x,left_y,trash= g.fwd(orig_x,orig_y, int(azimut)-60, radius*0.8)
		right_x,right_y,trash= g.fwd(orig_x,orig_y, int(azimut)+60, radius*0.8)
		center_x,center_y,trash= g.fwd(orig_x,orig_y, azimut, radius)
		#creation ligne dans fichier JSON SANS complement adresse
		file_json.write("{\"TAC\" : "+ str(TAC) +",\"LAC\" : "+ str(LAC) +", \"CI\" :"+str(CellID)+", \"dbTime\" : "+ str(dbTime) + ", \"frequency\" : \""+ str(frequency) + "\",  \"RAT\" : \""+sys.argv[2]+"\", \"name\" : \""+cellName+"\",\"addr\" :\""+str(address).replace("\"", "").replace("\\", "-")+"\", \"code\" :\""+postalCode+"\", \"city\" :\""+str(city)+"\", \"antenna\" :["+str(orig_x)+","+str(orig_y)+"],  \"loc\" : { \"type\" : \"Polygon\", \"coordinates\" : [[["+str(orig_x)+","+str(orig_y)+ "],["+str(left_x)+","+str(left_y)+ "],["+str(center_x)+","+str(center_y)+ "],["+str(right_x)+","+str(right_y)+ "],["+str(orig_x)+","+str(orig_y)+ "]]] } }\n")	 
finally:
	print ("dbTime = ", dbTime)
	print ("nbRowCSV =", nbRowCSV)
	print ("nbRowWithoutLati =", nbRowWithoutLati)
	print ("nbAzimutNotDigit", nbAzimutNotDigit)
	f.close()      # closing
	file_json.close()
	file_badRecords.close()
	print("Fin traitement fichier CSV")
