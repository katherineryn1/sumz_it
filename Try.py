import urllib.request
import os

URL = "https://cdn.discordapp.com/attachments/781424540383313932/781578293199110174/volcano.txt"

# Download file from URL - Failed HTTP 403 Forbidden
# with urllib.request.urlopen(URL) as f:
#     html = f.read().decode('utf-8')
#     print(html)

# Download file from URL - Success
# opener = urllib.request.URLopener()
# opener.addheader('User-Agent', 'Mozilla/5.0')
# filename, headers = opener.retrieve(URL, 'downloads/volcano.txt')
# print(filename)
# print(headers)

# Read the file and split it - Success
# split_text = []
# with open("downloads/volcano.txt") as f:
#     for line in f:
#         split_text.extend( line.replace('  ', ' ').split(' ') )
# print(split_text)

# Remove file - Success
os.remove('downloads/volcano.txt')