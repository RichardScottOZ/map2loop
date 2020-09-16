# --- COLUMN NAMES IN CSV DATA FILES: -------------------------------------------------------------
# OBJECT COORDINATES              =WKT
# FAULT: ID                       =OBJECTID
# FAULT: FEATURE                  =FEATURE
# POLYGON: ID                     =OBJECTID
# POLYGON: LEVEL1 NAME            =MAP_THEME
# POLYGON: LEVEL2 NAME            =MAX_AGE
# POLYGON: MIN AGE                =RM_AGE
# POLYGON: MAX AGE                =RM_AGE
# POLYGON: CODE                   =LABEL
# POLYGON: DESCRIPTION            =LITH_LIST
# POLYGON: ROCKTYPE1              =LITH_LIST
# POLYGON: ROCKTYPE2              =GENESIS
# DEPOSIT: SITE CODE              =SITE_CODE
# DEPOSIT: SITE TYPE              =SITE_TYPE_
# DEPOSIT: SITE COMMODITY         =SITE_COMMO
# --- SOME CONSTANTS: ----------------------------------------------------------------------------
# FAULT AXIAL FEATURE NAME        =Fold
# SILL UNIT DESCRIPTION CONTAINS  =sill
# IGNEOUS ROCKTYPE CONTAINS                           =intrusive
# VOLCANIC ROCKTYPE CONTAINS                          =volc
# IGNORE DEPOSITS WITH SITE TYPE                      =Infrastructure
# Intersect Contact With Fault: angle epsilon (deg)   =1.0
# Intersect Contact With Fault: distance epsilon (m)  =15.0
# Distance buffer (fault stops on another fault) (m)  =20.0
# Distance buffer (point on contact) (m)              =500.0
# Intersect polygons distance buffer (for bad maps)   =3.
# ------------------------------------------------------------------------------------------------
# Path to the output data folder                      =../Rockies/graph/
# Path to geology data file                           =../Rockies/tmp/geology_file.csv
# Path to faults data file                            =../Rockies/tmp/fault_file.csv
# Path to mineral deposits data file                  =../Rockies/tmp/mindep_file.csv
# ------------------------------------------------------------------------------------------------
# Clipping window X1 Y1 X2 Y2 (zeros for infinite)    =576473 5598018 626311 5650849
# Min length fraction for strat/fault graphs          =0.0
# Graph edge width categories (three doubles)         =2000. 20000. 200000.
# Graph edge direction (0-min age, 1-max age, 2-avg)  =2
# Deposit names for adding info on the graph          =Fe,Cu,Au,NONE
# Partial graph polygon ID                            =32
# Partial graph depth                                 =4
# Map subregion size dx, dy [m] (zeros for full map)  =0. 0.
# ------------------------------------------------------------------------------------------------
Creator "map2model-cpp"
graph [
  hierarchic 1
  directed 1
]