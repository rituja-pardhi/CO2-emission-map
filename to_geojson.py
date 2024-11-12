# CSV und JSON Format in Python öffnen.
import csv
import json

# CSV Datei Name: "DATEINAME.CSV"
INPUT_FILE = "output_clustered.csv"

# GeoJSON Datei Name: "DATEINAME.geojson"
OUTPUT_FILE = "output_clustered.geojson"

# Start und Endjahr
start_year = int(2007)
end_year = int(2017)

# Rechteck = 4, Dreieck= 3, Hexagon = 6, Octagon = 8
Ecken = 8 #8 for clustered data file, 1 for non clustered data file


# Lat always equal to 1 = 111 km 
# Long equator 1 = 111 km, 60° 1 = 55 km
a = float(0.02)
# Faktor für Long
b = float(2)
# Faktor für Lat
c = float(1)
# Faktor Hexagon
d = float(0.5)

# Öffnet die CSV Datei.
with open(INPUT_FILE, 'r',encoding="UTF-8-SIG") as file:
    # DictReader ermöglicht auslesen von Spaltennamen wie 
    # FacilityName oder die expliziete Spalte anzugeben
    csv_object = csv.DictReader(file, delimiter=';')
   
    # Erstellt ein Dictonary 
    geojson = {"type": "FeatureCollection"}
    # In der Liste features sind alle Emitenten aufgelistet.
    features = list()

    # Schleife für alle Listen Einträge.
    for row in csv_object:
        if row['Long'] != '':
            
            feature = dict()
            feature["type"] = "Feature"
            # Jahresschleife
            feature["properties"] = {int(str(year)):(int(float(row[str(year)])))for year in range(start_year, end_year+1)}
            # Durch die UTF 8 Formatierung entsteht \ufeff 
            # beim ersten Spalteneintrag
            feature["properties"]["FacilityName"] = (row['FacilityName'])
            feature["properties"]["FacilityID"] = (row['FacilityID'])
            #feature["properties"]["cluster"] = (row['cluster'])           #comment this line when convering non-clustered csv file to geojson
            feature["properties"]["height_07"] = int(float(row['height_07']))   #comment this line when convering non-clustered csv file to geojson
            feature["properties"]["height_08"] = int(float(row['height_08']))
            feature["properties"]["height_09"] = int(float(row['height_09']))
            feature["properties"]["height_10"] = int(float(row['height_10']))
            feature["properties"]["height_11"] = int(float(row['height_11']))
            feature["properties"]["height_12"] = int(float(row['height_12']))
            feature["properties"]["height_13"] = int(float(row['height_13']))
            feature["properties"]["height_14"] = int(float(row['height_14']))
            feature["properties"]["height_15"] = int(float(row['height_15']))
            feature["properties"]["height_16"] = int(float(row['height_16']))
            feature["properties"]["height_17"] = int(float(row['height_17']))
            feature["properties"]["Category"] = (row['Category']) 
            feature["properties"]["Concentration"] = (row['Concentration']) 
                           
                # um die Emissionsdaten extrudieren zu können,
                # werden Flächen anstatt Punkte benötigt.
                # der Type Polygon erstellt eine Fläche aus einer freien Anzahl 
                # von Punkten. Wichtig ist, 
                # dass der erste und letzte Punkt der gleiche ist.

            # Rechteck
            if Ecken == 4:
                
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": [
                    [ 
                        [
                        float(row['Long'].replace(",", "."))+b*a,
                        float(row['Lat'].replace(",", "."))+c*a
                        ],
                        [
                        float(row['Long'].replace(",", "."))+b*a,
                        float(row['Lat'].replace(",", "."))-c*a
                        ],
                        [
                        float(row['Long'].replace(",", "."))-b*a,
                        float(row['Lat'].replace(",", "."))-c*a
                        ],
                        [
                        float(row['Long'].replace(",", "."))-b*a,
                        float(row['Lat'].replace(",", "."))+c*a
                        ],
                        [
                        float(row['Long'].replace(",", "."))+b*a,
                        float(row['Lat'].replace(",", "."))+c*a
                        ]
                    ]
                    ]
                }
            # Dreieck
            elif Ecken == 3:
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": [
                    [ 
                        [
                        float(row['Long']),
                        float(row['Lat'])+c*a
                        ],
                        [
                        float(row['Long'])+b*a,
                        float(row['Lat'])-c*a
                        ],
                        [
                        float(row['Long'])-b*a,
                        float(row['Lat'])-c*a
                        ],
                        [
                        float(row['Long']),
                        float(row['Lat'])+c*a
                        ]
                    ]
                    ]
                }
            # Hexagon
            elif Ecken == 6:
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": [
                    [ 
                        [
                        float(row['Long']),
                        float(row['Lat'])+c*a
                        ],
                        [
                        float(row['Long'])+b*a,
                        float(row['Lat'])+(c-d)*a
                        ],
                        [
                        float(row['Long'])+b*a,
                        float(row['Lat'])-(c-d)*a
                        ],
                        [
                        float(row['Long']),
                        float(row['Lat'])-c*a
                        ],
                        [
                        float(row['Long'])-b*a,
                        float(row['Lat'])-(c-d)*a
                        ],
                        [
                        float(row['Long'])-b*a,
                        float(row['Lat'])+(c-d)*a
                        ],
                        [
                        float(row['Long']),
                        float(row['Lat'])+c*a
                        ]
                    ]
                    ]
                }
                # Octagon
            elif Ecken == 8:
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": [
                    [ 
                        [
                        float(row['Long'])+(c-d)*a,
                        float(row['Lat'])+c*a
                        ],
                        [
                        float(row['Long'])+b*a,
                        float(row['Lat'])+(c-d)*a
                        ],
                        [
                        float(row['Long'])+b*a,
                        float(row['Lat'])-(c-d)*a
                        ],
                        [
                        float(row['Long'])+(c-d)*a,
                        float(row['Lat'])-c*a
                        ],
                        [
                        float(row['Long'])-(c-d)*a,
                        float(row['Lat'])-c*a
                        ],
                        [
                        float(row['Long'])-b*a,
                        float(row['Lat'])-(c-d)*a
                        ],
                        [
                        float(row['Long'])-b*a,
                        float(row['Lat'])+(c-d)*a
                        ],
                        [
                        float(row['Long'])-(c-d)*a,
                        float(row['Lat'])+c*a
                        ],
                        [
                        float(row['Long'])+(c-d)*a,
                        float(row['Lat'])+c*a
                        ]
                    ]
                    ]
                }
            elif Ecken == 1:
            
                feature["geometry"] = {
                    "type": "Point",
                    "coordinates": [
                    
                        
                        float(row['Long']),
                        float(row['Lat'])
                        
                    
                    ]
                }
            features.append(feature)

    geojson['features'] = features

with open(OUTPUT_FILE, 'w',encoding="UTF-8-SIG") as of:
    # Schreibt die GeoJSON Datei. 
    # Mit indent kann der Abstand von Tabs verändert werden.
    json.dump(geojson, of, indent=4, ensure_ascii=False)