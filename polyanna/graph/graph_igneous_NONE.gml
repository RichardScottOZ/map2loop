# --- COLUMN NAMES IN CSV DATA FILES: -------------------------------------------------------------
# OBJECT COORDINATES              =WKT
# FAULT: ID                       =OBJECTID
# FAULT: FEATURE                  =FEATURE
# POLYGON: ID                     =OBJECTID
# POLYGON: LEVEL1 NAME            =PARENTCODE
# POLYGON: LEVEL2 NAME            =GROUP_
# POLYGON: MIN AGE                =MIN_AGE_MA
# POLYGON: MAX AGE                =MAX_AGE_MA
# POLYGON: CODE                   =CODE
# POLYGON: DESCRIPTION            =DESCRIPTN
# POLYGON: ROCKTYPE1              =ROCKTYPE1
# POLYGON: ROCKTYPE2              =ROCKTYPE2
# DEPOSIT: SITE CODE              =site_code
# DEPOSIT: SITE TYPE              =site_type_
# DEPOSIT: SITE COMMODITY         =site_commo
# --- SOME CONSTANTS: ----------------------------------------------------------------------------
# FAULT AXIAL FEATURE NAME        =Fold axial trace
# SILL UNIT DESCRIPTION CONTAINS  =sill
# IGNEOUS ROCKTYPE CONTAINS                           =intrusive
# VOLCANIC ROCKTYPE CONTAINS                          =volcanic
# IGNORE DEPOSITS WITH SITE TYPE                      =Infrastructure
# Intersect Contact With Fault: angle epsilon (deg)   =1.0
# Intersect Contact With Fault: distance epsilon (m)  =15.0
# Distance buffer (fault stops on another fault) (m)  =20.0
# Distance buffer (point on contact) (m)              =500.0
# Intersect polygons distance buffer (for bad maps)   =3.
# ------------------------------------------------------------------------------------------------
# Path to the output data folder                      =../polyanna/graph/
# Path to geology data file                           =../polyanna/tmp/geology_file.csv
# Path to faults data file                            =../polyanna/tmp/fault_file.csv
# Path to mineral deposits data file                  =../polyanna/tmp/mindep_file.csv
# ------------------------------------------------------------------------------------------------
# Clipping window X1 Y1 X2 Y2 (zeros for infinite)    =278190 7419758 576400 7723202
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
    LabelGraphics [ text "Collier Basin" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -1
    LabelGraphics [ text "Fortescue Group" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -3
    LabelGraphics [ text "Gregory Range Suite" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -5
    LabelGraphics [ text "Hamersley Group" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -6
    LabelGraphics [ text "Kalkarindji Suite" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -9
    LabelGraphics [ text "Officer Basin" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -4
    LabelGraphics [ text "Pilbara Craton greenstones" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -10
    LabelGraphics [ text "Talbot and Connaughton Domains Rudall Complex" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id 49
    LabelGraphics [ text "A-FO-xb-s" fontSize 14 ]
    gid -1
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 55
    LabelGraphics [ text "A-FOh-xs-f" fontSize 14 ]
    gid -1
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 50
    LabelGraphics [ text "A-GR-mg" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 57
    LabelGraphics [ text "A-moa-P" fontSize 14 ]
    gid -4
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 22
    LabelGraphics [ text "AP_-_pj-ccx" fontSize 14 ]
    gid -5
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 6
    LabelGraphics [ text "E-_dv-od" fontSize 14 ]
    gid -6
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 15
    LabelGraphics [ text "P_-MN-s" fontSize 14 ]
    gid -7
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 44
    LabelGraphics [ text "P_-MNw-sf" fontSize 14 ]
    gid -7
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 47
    LabelGraphics [ text "P_-TAg-sg" fontSize 14 ]
    gid -9
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 14
    LabelGraphics [ text "P_-_ya-mls" fontSize 14 ]
    gid -10
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 7
    LabelGraphics [ text "P_-md-PTRB" fontSize 14 ]
    gid -10
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 8
    LabelGraphics [ text "P_-mgnu-PTRO" fontSize 14 ]
    gid -10
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 24
    LabelGraphics [ text "P_-xmb-md-PTRC" fontSize 14 ]
    gid -10
    graphics [ fill "#ffffff" w 150 ]
  ]
  edge [
    source 8
    target 7
    graphics [ style "line" arrow "last" width 7 fill "#00aa54" ]
  ]
  edge [
    source 8
    target 14
    graphics [ style "line" arrow "last" width 5 fill "#001de1" ]
  ]
  edge [
    source 6
    target 22
    graphics [ style "line" arrow "last" width 5 fill "#36c800" ]
  ]
  edge [
    source 6
    target 15
    graphics [ style "line" arrow "last" width 5 fill "#000cf2" ]
  ]
  edge [
    source 8
    target 24
    graphics [ style "line" arrow "last" width 7 fill "#00946a" ]
  ]
  edge [
    source 6
    target 47
    graphics [ style "line" arrow "last" width 3 fill "#0000ff" ]
  ]
  edge [
    source 6
    target 44
    graphics [ style "line" arrow "last" width 3 fill "#002ed0" ]
  ]
  edge [
    source 49
    target 50
    graphics [ style "line" arrow "last" width 5 fill "#0000ff" ]
  ]
  edge [
    source 50
    target 57
    graphics [ style "line" arrow "last" width 5 fill "#0000ff" ]
  ]
  edge [
    source 55
    target 50
    graphics [ style "line" arrow "last" width 5 fill "#08f600" ]
  ]
]