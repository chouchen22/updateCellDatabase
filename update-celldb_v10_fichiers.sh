#!/bin/bash
echo "suppression des fichiers JSON existants"
rm *.json


echo -e "\n cellules4G : copie du fichier csv pour analyse des differences "
cp cellules4G.csv cellules4G-previous.csv
echo -e "\n cellules 4G : traitement fichier CSV venant de  OSIRIS "
./cell_4G_from_Osiris_v10.py cellules4G.csv 4g
iconv -f ISO-8859-1 -t UTF-8 geo4G_Osiris.json -o geo4G_Osiris2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo4G_Osiris2.json --upsert --upsertFields LAC,CI

echo -e "\n alcatel2g : copie du fichier csv pour analyse des differences "
cp alcatel2G.csv alcatel2G-previous.csv
echo -e "\n alcatel2g : téléchargement fichier CSV venant de  TOPO FTP en cours..."
./cell_Alcatel2G_v10.py alcatel2G.csv 2g
iconv -f ISO-8859-1 -t UTF-8 geo2galcatel.json -o geo2galcatel2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo2galcatel2.json --upsert --upsertFields LAC,CI 

echo -e "\n Ericsson2G : copie du fichier csv pour analyse des differences "
cp Ericsson2G.csv Ericsson2G-previous.csv
echo -e "\n Ericsson2G : téléchargement fichier CSV venant de  TOPO FTP en cours..."
./cell_Ericson2G_v10.py Ericsson2G.csv 2g
iconv -f ISO-8859-1 -t UTF-8 geo2gericson.json -o geo2gericson2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo2gericson2.json --upsert --upsertFields LAC,CI

echo -e "\n Ericsson3G : copie du fichier csv pour analyse des differences "
cp Ericsson3G.csv Ericsson3G-previous.csv
echo -e "\n Ericsson3G: téléchargement fichier CSV venant de  TOPO FTP en cours..."
./cell_Ericson3G_v10.py Ericsson3G.csv 3g
iconv -f ISO-8859-1 -t UTF-8 geo3gericson.json -o geo3gericson2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo3gericson2.json --upsert --upsertFields LAC,CI

echo -e "\n Motorola2g : copie du fichier csv pour analyse des differences "
cp Motorola2g.csv Motorola2g-previous.csv
echo -e "\n Motorola2g: téléchargement fichier CSV venant de  TOPO FTP en cours..."
./cell_motorola2g_v10.py Motorola2g.csv 2g
iconv -f ISO-8859-1 -t UTF-8 geo2gmoto.json -o geo2gmoto2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo2gmoto2.json --upsert --upsertFields LAC,CI


echo -e "\n Nortel3G : copie du fichier csv pour analyse des differences "
cp Nortel3G.csv Nortel3G-previous.csv
echo -e "\n nortel3g : téléchargement fichier CSV venant de  TOPO FTP  en cours..."
./cell_Nortel3g_v10.py Nortel3G.csv 3g
iconv -f ISO-8859-1 -t UTF-8 geo3gNortel.json -o geo3gNortel2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo3gNortel2.json --upsert --upsertFields LAC,CI

echo -e "\n Nortel2G : copie du fichier csv pour analyse des differences "
cp Nortel2G.csv Nortel2G-previous.csv
echo -e "\n nortel2g : téléchargement fichier CSV venant de  TOPO FTP  en cours..."
./cell_Nortel2g_v10.py Nortel2G.csv 2g
iconv -f ISO-8859-1 -t UTF-8 geo2gNortel.json -o geo2gNortel2.json
echo "fin conversion UTF-8 / debut injection MongoDB"
mongoimport --db cells --collection topo --file geo2gNortel2.json --upsert --upsertFields LAC,CI

