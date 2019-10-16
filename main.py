import requests
import sqlite3
import os
import time
import zipfile
import io
import shutil
import subprocess

##
# Function downloads unzips and moves the downloaded files over the existing DB.
# @param url: takes an input URL to download from
def pullUpdate(url):
	r = requests.get(url, stream=True)
	total_length = r.headers.get('content-length')
	print ('Downloading hydrus please wait')
	#print ('header of intrest',str(r.headers['Content-Disposition']).split("=",1)[1] )
	z = zipfile.ZipFile(io.BytesIO(r.content))
	fileName = str(r.headers['Content-Disposition']).split("=",1)[1]
	fn = fileName.split("-")
	try:
		os.rmtree(str(fn[0]) + '-' + str(fn[1]) + '-' + str(format(str(fn[4]))[1:]).split('.')[0])
	except:
		print ('')
	z.extractall()
	
	
	shutil.move(str(fn[0]) + '-' + str(fn[1]) + '-' + str(format(str(fn[4]))[1:]).split('.')[0], 'hydrusnetwork')
	
		
		
		
def main():
	if not os.path.exists('main.db'):
		conn = sqlite3.connect('main.db')
		c = conn.cursor()	
		c.execute('''CREATE TABLE updateList (version text, lastChecked text)''')
		jsonPull = requests.get('https://api.github.com/repos/hydrusnetwork/hydrus/releases/latest').json()
		c.execute("INSERT INTO updateList (version, lastChecked) values (?,?)", (jsonPull.get('tag_name'), time.time()) )
		conn.commit()
		conn.close()
		pullUpdate(jsonPull.get('zipball_url'))
		subprocess.call("python3 hydrusnetwork/client.py", shell=True)
	else:
		jsonPull = requests.get('https://api.github.com/repos/hydrusnetwork/hydrus/releases/latest').json()
		conn = sqlite3.connect('main.db')
		c = conn.cursor()
		data = c.execute('SELECT * FROM updateList').fetchall()
		print (data[0][0])
		if not data[0][0] == jsonPull.get('tag_name') :
			print ('Must Update')
			pullUpdate(jsonPull.get('zipball_url'))
			c.execute("DELETE FROM updateList")
			c.execute("INSERT INTO updateList (version, lastChecked) values (?,?)", (jsonPull.get('tag_name'), time.time()) )
			conn.commit()
			conn.close()
			subprocess.call("python3 hydrusnetwork/client.py", shell=True)
		else:
			print ('Nothing To Do Starting Hydrus')
			subprocess.call("python3 hydrusnetwork/client.py", shell=True)

main()


