#!/usr/bin/python
# -*- coding: utf8 -*-

# Copyright(C) 2021 Dieter Fauth
# This program is free software: you can redistribute it and / or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# You should have received a copy of the GNU General Public License along with this program. If not, see < http: // www.gnu.org/licenses/>.
# Contact: via my github account
# https: // github.com/FauthD/ExportShotwellXMP

# Caution: This is quick and Dirty code, use it on your own risk
# Created for my once in a live action to export from Shotwell to digikam.
# For me it worked just fine.
# Make a full backup before you run it!!!!!

# No Handling of versions inside Shotwell.

# For Python3!

# Rational:
# Shotwell can write the tags and rating into jpg images, but it cannot write such metadata into movies.
# This python code reads the photo.db of shotwell and creates *.xmp files with the same base name as the images and movies.
# Digikam does read these *.xmp files on import and therefore also imports the tags and rating.

# Dieter Fauth, 2022.01.14

import os
import sqlite3
from collections import defaultdict

###############################################################
# adjust these to fit your needs
PrunePath="/home/xxxxx/"
ShotwellDBDir=".shotwell/data/"
###############################################################

def CreateDirs(pathname):
    path = os.path.split(pathname)[0]
    #print (path)
    try:
        os.makedirs(path, mode=0o776)
    except OSError:
        #print ("Exists")
        True

def WriteRating(file, rating):
    RateString='    xmp:Rating="{}">\n'.format(rating)
    file.write(RateString)

def WriteTags(file, tags):
    head =u'  <digiKam:TagsList>\n'\
    '    <rdf:Seq>\n'

    tail=u'    </rdf:Seq>\n'\
    '  </digiKam:TagsList>\n'\

    file.write(head)
    for tag in tags:
        tagstring=u'      <rdf:li>{}</rdf:li>\n'.format(tag)
        file.write(tagstring)
    file.write(tail)

def CreateXMP(file, rating, tags):
    #print(id, rating, pathname )
    
    head = u'<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'\
    '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">\n'\
    ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'\
    '  <rdf:Description rdf:about=""\n'\
    '    xmlns:xmp="http://ns.adobe.com/xap/1.0/"\n'\
    '    xmlns:digiKam="http://www.digikam.org/ns/1.0/">\n'

    tail =u'  </rdf:Description>\n'\
    ' </rdf:RDF>\n'\
    '</x:xmpmeta>\n'\
    '<?xpacket end="w"?>\n'
    
    file.write(head)
    WriteRating(file, rating)
    WriteTags(file, tags)
    file.write(tail)

def WriteXMP(rating, pathname, tags):
    #print(rating, pathname )
    CreateDirs(pathname)
    file = open(pathname + ".xmp", mode='w+', encoding='utf8')
    CreateXMP(file, rating, tags)
    file.close()
    


def ParseTags(tags):
    # if(tags is None):
    #     tags = ''
    return tags.split(',')

def ReadTag(tag, prefix):
    num = -1;
    if (prefix in tag):
        hexstring = tag.replace(prefix, "")
        #print (hexstring)
        num = int(hexstring, 16)
        # print(num)
    # else:
    #     print(tag)
    return num
    
video_tags = defaultdict(list)
photo_tags = defaultdict(list)

def ReadTags(cursor):
    cursor.execute("SELECT * FROM TagTable")
    data = cursor.fetchall()
    for row in data:
        tags = row[2]
        tagname = row[1]
        # print(tagname)
        if(tags is not None):
            taglist = ParseTags(tags)
            # print (taglist)
            for tag in taglist:
                if(len(tag) > 0):
                    num = ReadTag(tag, "video-")
                    if(num >= 0):
                        video_tags[num].append(tagname)
                    num = ReadTag(tag, "thumb")
                    if(num >= 0):
                        photo_tags[num].append(tagname)

video_files = defaultdict(list)

def WorkVideoDetails(cursor):
    cursor.execute("SELECT id,rating,filename FROM VideoTable")
    data = cursor.fetchall()
    #print(data)
    for row in data:
        id = row[0]
        rating = row[1]
        pathname = row[2].replace(PrunePath, "")
        tags = video_tags[id]

        WriteXMP(rating, pathname, tags)

def WorkPhotoDetails(cursor):
    cursor.execute("SELECT id,rating,filename FROM PhotoTable")
    data = cursor.fetchall()
    #print(data)
    for row in data:
        id = row[0]
        rating = row[1]
        pathname = row[2].replace(PrunePath, "")
        tags = photo_tags[id]

        WriteXMP(rating, pathname, tags)

def ReadFromDB():
    con = sqlite3.connect(ShotwellDBDir + "photo.db")
    cursor = con.cursor()

    # cursor.execute("SELECT Count(*) FROM VideoTable")
    # for res in cursor:
    #     print(res[0])

    # cursor.execute("PRAGMA table_info(VideoTable)")
    # for column in cursor:
    #     print(column)

    # cursor.execute("PRAGMA table_info(TagTable)")
    # for column in cursor:
    #     print(column)

    # print(data)
    ReadTags(cursor)
    WorkVideoDetails(cursor)
    WorkPhotoDetails(cursor)
    
    con.close()

ReadFromDB()

# print (video_tags)
# print (photo_tags)
