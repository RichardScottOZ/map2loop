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
  node [
    id -7
    LabelGraphics [ text "LOWER ORDOVICIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -6
    LabelGraphics [ text "MIDDLE ORDOVICIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -1
    LabelGraphics [ text "MISSISSIPPIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -3
    LabelGraphics [ text "UPPER CAMBRIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -4
    LabelGraphics [ text "UPPER DEVONIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id 1
    LabelGraphics [ text "Cb-Bf-l-u" fontSize 14 ]
    gid -1
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 0
    LabelGraphics [ text "Cb-Bf-u-B" fontSize 14 ]
    gid -1
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 10
    LabelGraphics [ text "CmOd-SP" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 3
    LabelGraphics [ text "Dv-Pa" fontSize 14 ]
    gid -4
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 2
    LabelGraphics [ text "DvCb-EBf-l-lm" fontSize 14 ]
    gid -4
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 8
    LabelGraphics [ text "Od-Sk" fontSize 14 ]
    gid -6
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 9
    LabelGraphics [ text "Od-Tp" fontSize 14 ]
    gid -7
    graphics [ fill "#ffffff" w 150 ]
  ]
  edge [
    source 0
    target 3
    graphics [ style "line" arrow "last" width 1 fill "#00bd41" ]
  ]
  edge [
    source 0
    target 8
    graphics [ style "line" arrow "last" width 1 fill "#25d900" ]
  ]
  edge [
    source 0
    target 9
    graphics [ style "line" arrow "last" width 1 fill "#00fe00" ]
  ]
  edge [
    source 0
    target 10
    graphics [ style "line" arrow "last" width 1 fill "#008f6f" ]
  ]
  edge [
    source 1
    target 9
    graphics [ style "line" arrow "last" width 1 fill "#00fe00" ]
  ]
  edge [
    source 1
    target 10
    graphics [ style "line" arrow "last" width 1 fill "#00926c" ]
  ]
  edge [
    source 2
    target 3
    graphics [ style "line" arrow "last" width 1 fill "#00738b" ]
  ]
  edge [
    source 2
    target 10
    graphics [ style "line" arrow "last" width 3 fill "#007886" ]
  ]
  edge [
    source 3
    target 8
    graphics [ style "line" arrow "last" width 1 fill "#0054aa" ]
  ]
]