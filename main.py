#IMPORTS
import requests
from urllib.request import urlopen
import json
import ctypes
from shutil import copy2,copyfile
import schedule
import time
from datetime import datetime
import os
from PIL import Image
import msvcrt as m

#VARIABLES
API_KEY=""
DEFAULT_API_KEY="PLEASE REGISTER YOUR API KEY AT: https://api.nasa.gov/"
USER_KEY=input("enter your api key(pass empty string for default one):")
user = os.path.expanduser('~').split('\\')[2]
directory=f"C:\\Users\\{user}\\Documents\\APOD_Data"
assets=directory+"\\Fetched"
assets_img=assets+"\\img"
assets_txt=assets+"\\txt"
default_choice="y"
#FUNCTIONS
def wait():
    print("press any key to exit")
    m.getch()
#make some necesery folders to store fetched data
if not os.path.isdir(directory):
      os.mkdir(directory)
if not os.path.isdir(assets):
    os.mkdir(assets)
if not os.path.isdir(assets_img):
      os.mkdir(assets_img)
if not os.path.isdir(assets_txt):
      os.mkdir(assets_txt)

if USER_KEY=="":
    API_KEY=DEFAULT_API_KEY
else:
    API_KEY=USER_KEY
print(f"Using default api key.\nAPI KEY IS: {API_KEY}")
print("do you want data for today?<y/n>(default is y)")
choice= input()
if choice=="y":
    date=datetime.today().strftime('%Y-%m-%d')
else:
    print("enter date you want")
    year = input("Enter Year: ")  #choose date from whitch to fetch data
    month = input("Enter Month: ")
    day = input("Enter Day: ")
    date = f"{year}-{month}-{day}"
print(f"retrieving data for {date}")
url=f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}&hd=True"

response= requests.get(url)
if response:
    print('Request is successful')
    decoded_string = urlopen(url).read().decode('utf-8')
    decoded_json=json.loads(decoded_string)
    for key in decoded_json:
        value=decoded_json[key]
        print(f"{key}: {value}")
   
    assets_img=assets_img+f"\\PIC_FOR_{decoded_json['date']}.png"
    if decoded_json['url'].split("/")[2]=="www.youtube.com":
        print("\n\n\nSorry That is youtube video \nIf you typed in the custom date try different one \nor wait for tomorrow if you chose today")
        wait()
    else:
        img=Image.open(urlopen(decoded_json['url']))
        img.save(assets_img,"PNG")
        ctypes.windll.user32.SystemParametersInfoW(20, 0, assets_img , 0)
        print(f"Image has been saved to: {assets_img}\nand background has been set to that image")
        assets_txt=assets_txt+f"\\DESCRIPTION_FOR_{decoded_json['date']}.txt"
        with open(assets_txt, 'a', encoding='utf-8') as f:
            json.dump(decoded_json, f, ensure_ascii=False, indent=4)
        print(f"Description has been saved to: {assets_txt}\nIt contains copyright data, Author and urls for hd version beside date and desc.")
        print("Dates are in YYYY-MM-DD Format.")
        wait()   
else:
    time.sleep(5)
    print("something's wrong.../n...I can feel it")
    wait()
    