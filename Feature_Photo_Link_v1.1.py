'''Program that attaches photos to features in csv file based on time stamp
This version of the script runs on the shapefile data created from the final template, after the template is applied in SAGA
Please install all the libraries. What Python does not have by default is: PIL, xlwt
Please export shapefile to csv before you begin
Also write down in a notepad file the complete path to the picture folder and csv file  for when the script will ask it from you
Results should be exported in a csv file and then converted to csv for MS-DOS, with Excel
After you import it to QGIS as a table
v1.1 from 12/08/2016'''

from PIL import Image
from PIL.ExifTags import TAGS
import os
import PIL.Image
import xlwt
from xlwt import Workbook
import sys
import csv
import operator

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1', cell_overwrite_ok=True)

path=raw_input("Give me the photos path: ")       #User inputs a path to find files
dbf_file = raw_input("Give me full file path (full path/'name'.csv) of csv file: ")

f = open(dbf_file, 'rU')
csv_f=csv.reader(f, delimiter=',')

feature_hours = {}

def find_time(csv):
    for row in csv:
        for i in range(len(row)):
            if row[i]=="SVTIME":
                return i

c = find_time(csv_f)
for row in csv_f:
    if row[c]=="SVTIME":
        continue
    if row[c]=='':
        row[c]='00:00:00'
    feature_hours[row[0]] = (row[c][0:2],row[c][3:5],row[c][6:8],row[1]) #dictionary that has as value a tuple of hour:minute # make sure you have the correct column for ID
    
sorted_features = sorted(feature_hours.items(), key=operator.itemgetter(1))
print "Number of feature " + str(len(sorted_features))

a = []          #list a will contain all the files

def list_files(path):
    os.chdir(path)          #os now has path as working directory
    f = []              #list f will contain all the files found at that path
    f = os.listdir(path)
    for item in f:
        a.append(item)      #every path found is added to the list a
        if item=="Thumbs.db":
            a.remove(item)
    
list_files(path)            #lists all the files in that path

b =[]                   #list b will contain all the paths to the files

for item in a:
    b.append(item)

photo_hours = {}                    #starts a dictionary which will contain hours from photo

for item in b:
    i = Image.open(item)                      #opens the image
    info = i._getexif()
    for tag, value in info.items():         #for every couple of tag,value
        decoded = TAGS.get(tag, tag)        #decoded gets the tag - not very clear why "tag,tag"
        if decoded=="DateTimeOriginal":
            photo_hours[item] = (value[11:13],value[14:16],value[17:19])

sorted_photo = sorted(photo_hours.items(), key=operator.itemgetter(1))

j=1

sheet1.write(0,0,"PICTURE1")
sheet1.write(0,1,"PICTURE2")
sheet1.write(0,2,"SVTIME")
#sheet1.write(0,3,"Latitude")
#sheet1.write(0,4,"Longitude")

for feature_time in sorted_features:
    i=0
    for photo_time in sorted_photo:
        if i==2:
            break
        if feature_time[1][0]==photo_time[1][0]:
            if (feature_time[1][1]==photo_time[1][1] and feature_time[1][2]<photo_time[1][2]) or int(feature_time[1][1])+1==int(photo_time[1][1]) or int(feature_time[1][1])+2==int(photo_time[1][1]):
                if i == 0:
                    i=i+1
                    sheet1.write(j,2,feature_time[1][0]+":"+feature_time[1][1]+":"+feature_time[1][2])
                    sheet1.write(j,0,photo_time[0])
                    #sheet1.write(j,3,feature_time[1][3])
                    #sheet1.write(j,4,feature_time[0])
                    j=j+1
                else:
                    i=i+1
                    sheet1.write(j-1,1,photo_time[0])
                
                #j=j+1
        elif int(feature_time[1][0])+1==photo_time[1][0]:
            if feature_time[1][1]>57 and ((photo_time[1][1]==58 and feature_time[1][2]<photo_time[1][2]) or photo_time[1][1]==59 or photo_time[1][1]==0 or photo_time[1][1]==1 or photo_time[1][1]==2):
                if i == 0:
                    i=i+1
                    sheet1.write(j,0,photo_time[0])
                    sheet1.write(j,2,feature_time[1][0]+":"+feature_time[1][1]+":"+feature_time[1][2])
                    #sheet1.write(j,3,feature_time[1][3])
                    #sheet1.write(j,4,feature_time[0])
                    j=j+1
                else:
                    i=i+1
                    sheet1.write(j-1,1,photo_time[0])
                #j=j+1
                    
print "Number of features with photos attached " + str(j-1)
        
x = raw_input("Where would you like to print results? Full path please: ")
wb.save(x)
print "Everything done, Sir!"
reload(sys)  
sys.setdefaultencoding('utf8')
f.close()
