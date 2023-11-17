import os
import utils.tools as tools
if not os.path.exists('Temp/Videos'):
    os.makedirs('Temp/Videos')
if not os.path.exists('Temp/Images'):
    os.makedirs('Temp/Images')
    
try:
    tools.updateImages()
except Exception as e:
    print(e)
# make videos
tools.makeVideos()