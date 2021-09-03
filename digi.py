from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import csv
import json

url = "https://www.digikala.com/incredible-offers/"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

all=[]
products_list = soup.find_all("div", class_="c-product-list__item js-product-list-content")
for i in products_list:
    title = i.find('div', class_ = "js-product-cart").get('title')
    price = re.sub(r"['\n'](\D)+\s","",i.find('div', class_ = "c-price__value-wrapper js-product-card-price").text).replace("تومان","")
    # end = i.find('div', class_ = "c-promotion__badge c-promotion__badge--incredible-over")
    try:
        sale = i.find('div', class_ = "c-price__discount-oval").find('span').text
        all.append(dict({"title": title , "price": price , "sale": sale}))

    except:
        pass    
    # all.append(dict({"title": title , "price": price , "sale": sale}))

print(all)

df = pd.DataFrame(all)
print(df)
df.to_csv('products.csv')



# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
	
	# create a dictionary
	data = {}
	
	# Open a csv reader called DictReader
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		
		# Convert each row into a dictionary
		# and add it to data
		for rows in csvReader:
			
			# Assuming a column named 'No' to
			# be the primary key
			key = rows['id']
			data[key] = rows

	# Open a json writer, and use the json.dumps()
	# function to dump data
	with open(jsonFilePath, 'w') as jsonf:
		jsonf.write(json.dumps(data, indent=4))
		
# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = r'product_detail.csv'
jsonFilePath = r'Names.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)
