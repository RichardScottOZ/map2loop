#ROI

step_out=0.1   #padding around dtm to ensure reprojected dtm covers target area (in degrees)
inset=0      #unused??

#
minx=576473  #region of interest coordinates in metre-based system (or non-degree system)
maxx=626311
miny=5598018
maxy=5650849
model_top=4000
model_base=-3200

#PATHS

local_paths=False       #flag to use local or WFS source for data inputs (True = local)


data_path=''
clut_path=''
base_url='https://gs-seamless.geoscience.nsw.gov.au/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeName='

structure_file='D:/Loop_Data/GSC/3D_Rockies/extra/For_Mark/Bedding_Map_all.shp'
fault_file='D:/Loop_Data/GSC/3D_Rockies/of_8576_2D_finaldata/of_8576_faults_26911.shp'
fold_file='D:/Loop_Data/GSC/3D_Rockies/of_8576_2D_finaldata/of_8576_folds_26911.shp'
geology_file='D:/Loop_Data/GSC/3D_Rockies/Kana_geo/Kana_geo_flat.shp'
mindep_file='../source_data//null_mindeps.shp'

#CRS

src_crs = 'epsg:4326'  # coordinate reference system for imported dtms (geodetic lat/long WGS84)
dst_crs = 'epsg:26911' # coordinate system for data

#CODES AND LABELS 
# these refer to specific fields (codes) in GIS layer or database that contain the info needed for these calcs and text substrings (labels) in the contents of these fields
c_l={'d': 'DIP',
 'dd': 'STRIKE',
 'sf': 'SUBFEATURE',
 'bedding': 'bed',
 'otype': 'strike',
 'bo': 'ATTITUDE',
 'btype': 'over',
 'g': 'MAX_AGE',
 'g2': 'MIN_AGE',
 'c': 'LABEL',
 'ds': 'LITH_LIST',
 'u': 'MAP_THEME',
 'r1': 'LITH_LIST',
 'r2': 'GENESIS',
 'sill': 'sill',
 'intrusive': 'intrusive',
 'volcanic': 'volc',
 'msc': 'SITE_CODE',
 'msn': 'SHORT_NAME',
 'mst': 'SITE_TYPE_',
 'mtc': 'TARGET_COM',
 'mscm': 'SITE_COMMO',
 'mcom': 'COMMODITY_',
 'minf': 'Cons',
 'min': 'RM_AGE',
 'max': 'RM_AGE',
 'f': 'FEATURE',
 'fault': 'fault',
 'ff': 'FEATURE',
 'fold': 'Fold',
    
 'fdip_flag': 'fixed', # alpha, num, fixed, random
 'fdip': '90',
 'fdipnull': '0',
    
 'fdipdir_flag': 'random', # alpha, num, random
 'fdipdirnull': '0',
 'fdipdir': '0',
    
 'n': 'NAME',
 't': 'SUBFEATURE',
 'syn': 'syn',
 'o': 'OBJECTID',
 'gi': 'STATION_ID'}

#DECIMATION

orientation_decimate=0  #store every nth orientation (in object order) 0 = save all
contact_decimate=10     #store every nth contact point (in object order) 0 = save all
fault_decimate=5        #store every nth fault point (in object order) 0 = save all
fold_decimate=5         #store every nth fold axial trace point (in object order) 0 = save all

#INTERPOLATION

gridx=50                #x grid dimensions (no of points, not distance) for interpolations
gridy=50                #x grid dimensions (no of points, not distance) for interpolations
scheme='scipy_rbf'      #interpolation scheme
dist_buffer=5           #buffer distance for clipping points by faults (in metres or same units as dst_crs)
intrusion_mode=0        # 1 all intrusions exluded from basal contacts, 0 only sills
use_interpolations=False    # flag to use interpolated orientations or not.

#ASSUMPTIONS

pluton_dip=45           #surface dip of pluton contacts
pluton_form='domes'     #saucers: \__+_+__/  batholith: +/       \+   domes: /  +  + \  pendant: +\_____/+
fault_dip=90            #surface dip of faults

#DERIVED AND FIXED PATHS

m2m_cpp_path='../m2m_cpp/'

graph_path=test_data_path+'graph/'
tmp_path=test_data_path+'tmp/'
#data_path=test_data_path+'data/'
dtm_path=test_data_path+'dtm/'
output_path=test_data_path+'output/'
vtk_path=test_data_path+'vtk/'

fault_file_csv=tmp_path+'fault_file.csv'
structure_file_csv=tmp_path+'structure_file.csv'
geology_file_csv=tmp_path+'geology_file.csv'
mindep_file_csv=tmp_path+'mindep_file.csv'

fault_file=data_path+fault_file
fold_file=data_path+fold_file
structure_file=data_path+structure_file
geology_file=data_path+geology_file
mindep_file=data_path+mindep_file

strat_graph_file=test_data_path+'graph/graph_strat_NONE.gml'

dtm_file=dtm_path+'dtm.tif'
dtm_reproj_file=dtm_path+'dtm_rp.tif'

if(not os.path.isdir(test_data_path)):
   os.mkdir(test_data_path)
if(not os.path.isdir(tmp_path)):
   os.mkdir(tmp_path)
if(not os.path.isdir(output_path)):
   os.mkdir(output_path)
if(not os.path.isdir(dtm_path)):
   os.mkdir(dtm_path)
if(not os.path.isdir(vtk_path)):
   os.mkdir(vtk_path)
if(not os.path.isdir(graph_path)):
   os.mkdir(graph_path)

print('Default parameters loaded from '+test_data_path+'m2l_config.py:')
with open('../Rockies/m2l_config.py', 'r') as myfile:
  data = myfile.read()
  print(data)
  myfile.close()

print('Modify these parameters in the cell below')
