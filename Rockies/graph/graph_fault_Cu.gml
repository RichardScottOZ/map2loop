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
    LabelGraphics [ text "LOWER CAMBRIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -25
    LabelGraphics [ text "LOWER ORDOVICIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -3
    LabelGraphics [ text "MIDDLE CAMBRIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -24
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
    id -27
    LabelGraphics [ text "NEOPROTEROZOIC" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -8
    LabelGraphics [ text "UPPER CAMBRIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -18
    LabelGraphics [ text "UPPER DEVONIAN" anchor "n" fontStyle "bold" fontSize 14 ]
    isGroup 1
    graphics [ fill "#FAFAFA" ]
  ]
  node [
    id -26
    LabelGraphics [ text "UPPER ORDOVICIAN" anchor "n" fontStyle "bold" fontSize 14 ]
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
    id 26
    LabelGraphics [ text "Cm-Ar-l" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 25
    LabelGraphics [ text "Cm-Ar-lw" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 27
    LabelGraphics [ text "Cm-Ar-uWf" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 32
    LabelGraphics [ text "Cm-Ca" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 34
    LabelGraphics [ text "Cm-G" fontSize 14 ]
    gid -7
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 20
    LabelGraphics [ text "Cm-L" fontSize 14 ]
    gid -8
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 28
    LabelGraphics [ text "Cm-La" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 18
    LabelGraphics [ text "Cm-M" fontSize 14 ]
    gid -8
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 29
    LabelGraphics [ text "Cm-MD" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 33
    LabelGraphics [ text "Cm-Na" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 31
    LabelGraphics [ text "Cm-Pk" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 23
    LabelGraphics [ text "Cm-Su-l" fontSize 14 ]
    gid -8
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 30
    LabelGraphics [ text "Cm-T" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 24
    LabelGraphics [ text "Cm-rim" fontSize 14 ]
    gid -3
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 17
    LabelGraphics [ text "CmOd-SP" fontSize 14 ]
    gid -8
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 7
    LabelGraphics [ text "Dv-A" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 6
    LabelGraphics [ text "Dv-MH" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 5
    LabelGraphics [ text "Dv-PMH" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 3
    LabelGraphics [ text "Dv-Pa" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 4
    LabelGraphics [ text "Dv-Ss" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 2
    LabelGraphics [ text "DvCb-EBf-l-lm" fontSize 14 ]
    gid -18
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 10
    LabelGraphics [ text "Od-Sk" fontSize 14 ]
    gid -24
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 13
    LabelGraphics [ text "Od-Tp" fontSize 14 ]
    gid -25
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 8
    LabelGraphics [ text "OdSl-B" fontSize 14 ]
    gid -26
    graphics [ fill "#ffffff" w 150 ]
  ]
  node [
    id 35
    LabelGraphics [ text "Pt-M" fontSize 14 ]
    gid -27
    graphics [ fill "#ffffff" w 150 ]
  ]
  edge [
    source 0
    target 3
    graphics [ style "line" arrow "last" width 3 fill "#0014ea" ]
  ]
  edge [
    source 2
    target 3
    graphics [ style "line" arrow "last" width 3 fill "#0003fb" ]
  ]
  edge [
    source 3
    target 10
    graphics [ style "line" arrow "last" width 1 fill "#0008f6" ]
  ]
  edge [
    source 3
    target 17
    graphics [ style "line" arrow "last" width 3 fill "#0031cd" ]
  ]
  edge [
    source 4
    target 17
    graphics [ style "line" arrow "last" width 1 fill "#004db1" ]
  ]
  edge [
    source 6
    target 17
    graphics [ style "line" arrow "last" width 1 fill "#006b93" ]
  ]
  edge [
    source 7
    target 8
    graphics [ style "line" arrow "last" width 3 fill "#0001fd" ]
  ]
  edge [
    source 7
    target 17
    graphics [ style "line" arrow "last" width 3 fill "#0006f8" ]
  ]
  edge [
    source 10
    target 17
    graphics [ style "line" arrow "last" width 3 fill "#005aa4" ]
  ]
  edge [
    source 23
    target 28
    graphics [ style "line" arrow "last" width 1 fill "#ff0000" ]
  ]
  edge [
    source 24
    target 28
    graphics [ style "line" arrow "last" width 3 fill "#ff0000" ]
  ]
  edge [
    source 24
    target 31
    graphics [ style "line" arrow "last" width 3 fill "#00c935" ]
  ]
  edge [
    source 25
    target 28
    graphics [ style "line" arrow "last" width 1 fill "#ff0000" ]
  ]
  edge [
    source 27
    target 31
    graphics [ style "line" arrow "last" width 5 fill "#0001fd" ]
  ]
  edge [
    source 29
    target 31
    graphics [ style "line" arrow "last" width 3 fill "#0016e8" ]
  ]
  edge [
    source 30
    target 31
    graphics [ style "line" arrow "last" width 3 fill "#0030ce" ]
  ]
  edge [
    source 31
    target 32
    graphics [ style "line" arrow "last" width 5 fill "#000ef0" ]
  ]
  edge [
    source 32
    target 34
    graphics [ style "line" arrow "last" width 3 fill "#0002fc" ]
  ]
  edge [
    source 34
    target 35
    graphics [ style "line" arrow "last" width 5 fill "#0001fd" ]
  ]
  edge [
    source 0
    target 10
    graphics [ style "line" arrow "last" width 1 fill "#25d900" ]
  ]
  edge [
    source 0
    target 13
    graphics [ style "line" arrow "last" width 1 fill "#00fe00" ]
  ]
  edge [
    source 0
    target 17
    graphics [ style "line" arrow "last" width 1 fill "#008f6f" ]
  ]
  edge [
    source 1
    target 13
    graphics [ style "line" arrow "last" width 1 fill "#00fe00" ]
  ]
  edge [
    source 1
    target 17
    graphics [ style "line" arrow "last" width 1 fill "#00926c" ]
  ]
  edge [
    source 2
    target 17
    graphics [ style "line" arrow "last" width 3 fill "#007886" ]
  ]
  edge [
    source 3
    target 34
    graphics [ style "line" arrow "last" width 1 fill "#00cc32" ]
  ]
  edge [
    source 3
    target 35
    graphics [ style "line" arrow "last" width 3 fill "#009f5f" ]
  ]
  edge [
    source 4
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#00ab53" ]
  ]
  edge [
    source 5
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#008a74" ]
  ]
  edge [
    source 7
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#00b648" ]
  ]
  edge [
    source 10
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#00f10d" ]
  ]
  edge [
    source 17
    target 32
    graphics [ style "line" arrow "last" width 1 fill "#009668" ]
  ]
  edge [
    source 17
    target 34
    graphics [ style "line" arrow "last" width 3 fill "#009866" ]
  ]
  edge [
    source 17
    target 35
    graphics [ style "line" arrow "last" width 3 fill "#008f6f" ]
  ]
  edge [
    source 18
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#00c33b" ]
  ]
  edge [
    source 20
    target 32
    graphics [ style "line" arrow "last" width 3 fill "#00906e" ]
  ]
  edge [
    source 20
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#008a74" ]
  ]
  edge [
    source 23
    target 32
    graphics [ style "line" arrow "last" width 1 fill "#00a25c" ]
  ]
  edge [
    source 23
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#33cb00" ]
  ]
  edge [
    source 26
    target 32
    graphics [ style "line" arrow "last" width 1 fill "#00b945" ]
  ]
  edge [
    source 27
    target 32
    graphics [ style "line" arrow "last" width 1 fill "#00916d" ]
  ]
  edge [
    source 27
    target 35
    graphics [ style "line" arrow "last" width 1 fill "#2fcf00" ]
  ]
  edge [
    source 30
    target 32
    graphics [ style "line" arrow "last" width 3 fill "#0046b8" ]
  ]
  edge [
    source 30
    target 33
    graphics [ style "line" arrow "last" width 1 fill "#00639b" ]
  ]
  edge [
    source 30
    target 34
    graphics [ style "line" arrow "last" width 3 fill "#0039c5" ]
  ]
  edge [
    source 31
    target 35
    graphics [ style "line" arrow "last" width 3 fill "#00a955" ]
  ]
  edge [
    source 32
    target 35
    graphics [ style "line" arrow "last" width 3 fill "#006b93" ]
  ]
]