#ROI

step_out=0.1   #padding around dtm to ensure reprojected dtm covers target area (in degrees)
inset=0      #unused??

#
#minx=500057  #region of interest coordinates in metre-based system (or non-degree system)
#maxx=603028
#miny=7455348
#maxy=7567953
model_top=1200
model_base=-3200

#PATHS

local_paths=False       #flag to use local or WFS source for data inputs (True = local)


data_path=''
clut_path=''
base_url='https://gs-seamless.geoscience.nsw.gov.au/geoserver/ows?service=wfs&version=2.0.0&request=GetFeature&typeName='

structure_file='../NSW/data/lao_struct_pt.shp'
fault_file='../NSW/data/faults_joined_left_contains_drop_dups.shp'
fold_file='../NSW/data/folds_lao.shp'
geology_file='../NSW/data/ge_rockunit_lao2.shp'
mindep_file='../NSW/data/nsw_mindeps.shp'

#CRS

src_crs = 'epsg:4326'  # coordinate reference system for imported dtms (geodetic lat/long WGS84)
dst_crs = 'epsg:28355' # coordinate system for data

#CODES AND LABELS 
# these refer to specific fields (codes) in GIS layer or database that contain the info needed for these calcs and text substrings (labels) in the contents of these fields
c_l= {
#Orientations
  "d": "dip",                  #field that contains dip information
  "dd": "azimuth",             #field that contains dip direction information
  "sf": 'codedescpt',             #field that contains information on type of structure
  "bedding": 'bedding',            #text to search for in field defined by sf code to show that this is a bedding measurement
  "otype": 'dip direction',            #flag to determine measurement convention (currently 'strike' or 'dip direction')
  "bo": "deform",             #field that contains type of foliation
  "btype": 'BEOI',            #text to search for in field defined by bo code to show that this is an overturned bedding measurement
#stratigraphy
  "g": 'sub_provin',               #field that contains coarser stratigraphic coding
  "g2": 'province',              #field that contains alternate coarser stratigraphic coding if 'g' is blank
  "c": 'unit_name',                 #field that contains finer stratigraphic coding
  "ds": 'deposition',           #field that contains information about lithology
  "u": 'nsw_code',             #field that contains alternate stratigraphic coding (not used??)
  "r1": 'class',           #field that contains  extra lithology information
  "r2": 'igneous_ty',           #field that contains even more lithology information
  "sill": 'sill',              #text to search for in field defined by ds code to show that this is a sill
  "intrusive": 'intrusive',    #text to search for in field defined by r1 code to show that this is an intrusion
  "volcanic": 'volcanic',      #text to search for in field defined by ds code to show that this is an volcanic (not intrusion)
#mineral deposits
  "msc": 'occurrence',          #field that contains site code of deposit
  "msn": 'deposit_na',         #field that contains short name of deposit
  "mst": 'comm_type',         #field that contains site type of deposit
  "mtc": 'major_comm',         #field that contains target commodity of deposit
  "mscm": 'ore_min',        #field that contains site commodity of deposit
  "mcom": 'comm_type',        #field that contains commodity group of deposit
  "minf": 'CONSTR',    #text to search for in field defined by mst code that shows site to ignore
#timing
  "min": 'top_end_ag',         #field that contains minimum age of unit defined by ccode
  "max": 'base_start',         #field that contains maximum age of unit defined by ccode
#faults and folds
  "f": 'boundaryty',              #field that contains information on type of structure
  "fault": 'Fault',            #text to search for in field defined by f code to show that this is a fault
  "ff": 'codedescpt',  # field that contains information on type of structure
  "fold": 'cline',  #text to search for in field defined by ff code to show that this is a fold axial trace
  "fdip": 'dip',               # field for numeric fault dip value
  "fdipnull": '0',         # text to search for in field defined by fdip to show that this has no known dip
  "fdipdir": 'faultdipdi',        # field for text fault dip direction value 
  "fdipdir_flag": 'alpha',        # flag for text fault dip direction type num e.g. 045 or alpha e.g. southeast    
  "fdipest": 'faultdipan',        # field for text fault dip estimate value
  "fdipest_vals": 'Moderate,Listric,Steep,Vertical',        # text to search for in field defined by fdipest to give fault dip estimate in increasing steepness
  "n": 'name',                 #field that contains information on name of fault (not used??)
  "t": 'codedescpt',                 #field that contains information on type of fold
  "syn": 'Syncline',           #text to search for in field defined by t to show that this is a syncline
#ids
  "o": 'unique_id',             #field that contains unique id of geometry object
  "gi": 'objectid'            #field that contains unique id of structure point
}

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

print('Default parameters loaded from '+test_data_path+'m2l_config_remote.py:')
with open('../NSW/m2l_config_remote.py', 'r') as myfile:
  data = myfile.read()
  print(data)
  myfile.close()

print('\nModify these parameters in the cell below')