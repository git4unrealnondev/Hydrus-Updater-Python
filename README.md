# Hydrus-Updater-Python
A python program to automatically upgrade hydrus.

To-Install:
Download to your hydrus instillation's parent folder.
pip3 install -r requirements.txt 

Move the main.py file to be in the same folder as your hydrus instillation.
Rename your hydrus instillation to be hydrusnetwork.
It should look like this:

Test-Folder:                                  
.                                                 
├── hydrusnetwork                                       
├── main.py                                    
└── requirements.txt

  
To run:                                                
  Linux: python3 ./main.py
  
  
Tested and works on Ubuntu 19.10

If you're on linux and wxPython Fails to build than try running this command

  sudo apt-get install build-essential libgtk-3-dev

It occurs whenever gtk3 isn't installed in your system

If you get an FFMPEG error than you probably dont have ffMpeg installed so run:

  sudo apt-get install ffmpeg
