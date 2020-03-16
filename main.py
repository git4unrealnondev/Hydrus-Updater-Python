import requests
import sqlite3
import os
import time
import zipfile
import io
import shutil
import subprocess

##
#  start This contains the code to start a properly installed version of hydrus
def startHydrus():
	subprocess.call("python3 hydrusnetwork/client.py", shell=True)
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
		print ('Download Complete Moving Files...')
	z.extractall()
	
	root_src_dir = str(fn[0]) + '-' + str(fn[1]) + '-' + str(format(str(fn[4]))[1:]).split('.')[0]
	
	root_dst_dir = 'hydrusnetwork'
	
	
	for src_dir, dirs, files in os.walk(root_src_dir):
		dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
		if not os.path.exists(dst_dir):
			os.makedirs(dst_dir)
		for file_ in files:
			src_file = os.path.join(src_dir, file_)
			dst_file = os.path.join(dst_dir, file_)
			if os.path.exists(dst_file):
				# in case of the src and dst are the same file
				if os.path.samefile(src_file, dst_file):
					continue
				os.remove(dst_file)
			shutil.move(src_file, dst_dir)
	shutil.rmtree(root_src_dir)
	
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
		
		startHydrus()
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
			
			startHydrus()
		else:
			print ('Nothing To Do Starting Hydrus')
			
			startHydrus()

main()


