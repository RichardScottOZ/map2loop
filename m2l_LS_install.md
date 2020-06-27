### 1) Start up an Anaconda console window  If you created an environment called loop last time, delete it to start again, otherwise ignore this step
   
conda env remove --name loop
   
### 2) Either way do the next two steps to create and enter a new environment called loop. 
   
conda create --name loop python=3.7
   
conda activate loop   
   
Each time you open an anaconda console   you will need to ensure you are in the loop environment by typing conda activate loop

### 3)  Install a bunch of libraries needed by LoopStructural or map2loop (you can copy/paste all of these at once into the console, once you are in the loop environment). This only has to be done the first time. This may take 15-20 minutes depending on internet/computer speed. You may get prompted to install some of the packages, if so, type y then hit return.
    
conda install -c conda-forge rasterio   -y   
conda install -c conda-forge geopandas -y   
conda install -c anaconda networkx -y   
conda install -c anaconda git -y   
conda install -c anaconda cython -y   
conda install -c anaconda pytz -y    
conda install -c anaconda pyamg -y   
conda install -c anaconda python-dateutil -y   
conda install -c conda-forge descartes -y   
conda install -c conda-forge owslib -y   
pip install jupyter    
conda install -c anaconda ipywidgets    -y   
conda install -c conda-forge ipyleaflet -y   
pip install lavavu    
conda install -c conda-forge folium -y   
pip install mplsteronet    
conda install -c anaconda scikit-learn -y   
conda install -c anaconda scikit-image -y   
    
### 4)  Navigate to where you want to store your files 
   
cd dirname
   
to change directory 
   
cd .. 
   
to go up one directory 
   
Create a new directory somewhere using
   
mkdir dirname
   
Now, download and install map2loop
   
git clone http://github.com/Loop3D/map2loop
   
Use your browser to go to download LoopStructural to the same level as the map2loop directory
https://github.com/Loop3D/LoopStructural/releases/download/latest/LoopStructural-1.0.1-cp37-cp37m-win_amd64.whl 
   
In the console type
   
pip install LoopStructural-1.0.1-cp37-cp37m-win_amd64.whl
cd map2loop
python setup.py install --user
    
### 5) Finally start up the jupyter server:
   
cd ..
jupyter-notebook
   
go into map2loop/notebooks using browser links to 1. Hamersley map processing.ipynb
   
To kill the jupyter server, click in the console where you started the server and type ctrl-C a couple of times.
   
### 6) To restart the server in the future, open up an anaconda console
   
cd to the directory that has map2loop in it
conda activate loop
jupyter-notebook

