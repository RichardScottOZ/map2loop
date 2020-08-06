#ROI

step_out=0.1   #padding around dtm to ensure reprojected dtm covers target area (in degrees)
inset=0      #unused??

#
#minx=0  #region of interest coordinates in metre-based system (or non-degree system)
#maxx=1
#miny=0
#maxy=1
model_top=1200
model_base=-3200

#PATHS

local_paths=False       #flag to use local or WFS source for data inputs (True = local)


data_path=''
clut_path=''
base_url='https://gs-seamless.geoscience.nsw.gov.au/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeName='

structure_file='../SA/data/sth_flinders_28354.shp'
fault_file='../SA/data/2M Linear Structures_28354.shp'
fold_file='../SA/data/2M Linear Structures_28354.shp'
geology_file='../SA/data/2M_Surface_Geology_28354.shp'
mindep_file='../source_data/null_mindeps.shp'

#CRS

src_crs = 'epsg:4326'  # coordinate reference system for imported dtms (geodetic lat/long WGS84)
dst_crs = 'epsg:28354' # coordinate system for data

#CODES AND LABELS 
# these refer to specific fields (codes) in GIS layer or database that contain the info needed for these calcs and text substrings (labels) in the contents of these fields
c_l={'d': 'INCLINATIO',
 'dd': 'AZIMUTH_TR',
 'sf': 'STRUCTURE_',
 'bedding': 'bedding',
 'otype': 'dip direction',
 'bo': 'YOUNGING',
 'btype': '-',
 'g': 'PARENTNAME',
 'g2': 'PROVINCE',
 'c': 'STRATNAME',
 'ds': 'STRATDESC',
 'u': 'MAINUNIT',
 'r1': 'No_col',
 'r2': 'No_col',
 'sill': 'sill',
 'intrusive': 'intrusive',
 'volcanic': 'volc',
 'msc': 'SITE_CODE',
 'msn': 'SHORT_NAME',
 'mst': 'SITE_TYPE_',
 'mtc': 'TARGET_COM',
 'mscm': 'SITE_COMMO',
 'mcom': 'TARGET_COM',
 'minf': 'Cons',
 'min': 'No_col',
 'max': 'No_col',
 'f': 'DESCRIPTIO',
 'fault': 'Fault',
 'ff': 'DESCRIPTIO',
 'fold': 'Fold',
 'fdip': 'No_col',
 'fdipnull': '0',
 'fdipdir': 'No_col',
 'fdipdir_flag': 'alpha',
 'fdipest': 'No_col',
 'fdipest_vals': 'No_col',
 'n': 'No_col',
 't': 'No_col',
 'syn': 'syn',
 'o': 'ID',
 'gi': 'FIELD_STRU'}

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
with open('../SA/m2l_config.py', 'r') as myfile:
  data = myfile.read()
  print(data)
  myfile.close()

print('Modify these parameters in the cell below')
