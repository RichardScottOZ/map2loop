import geopandas as gpd
from shapely.geometry import  LineString, Polygon,MultiLineString
import os.path
from map2loop import m2l_utils      
import warnings
import numpy as np
import pandas as pd
   
#explodes polylines and modifies objectid for exploded parts
def explode_polylines(indf,c_l,dst_crs):                                        
    #indf = gpd.GeoDataFrame.from_file(indata)                  
    outdf = gpd.GeoDataFrame(columns=indf.columns, crs=dst_crs)              
    for idx, row in indf.iterrows():                            
        if type(row.geometry) == LineString:                    
            outdf = outdf.append(row,ignore_index=True)         
        if type(row.geometry) == MultiLineString:               
            multdf = gpd.GeoDataFrame(columns=indf.columns, crs=dst_crs)     
            recs = len(row.geometry)                            
            multdf = multdf.append([row]*recs,ignore_index=True)
            i=0
            for geom in range(recs):                            
                multdf.loc[geom,'geometry'] = row.geometry[geom]
                multdf.loc[geom,c_l['o']]=str(multdf.loc[geom,c_l['o']])+'_'+str(i)
                print('map2loop warning: Fault_'+multdf.loc[geom,c_l['o']],'is one of a set of duplicates, so renumbering')
                i=i+1
            outdf = outdf.append(multdf,ignore_index=True)      
    return outdf                                                

def check_map_old(structure_file,geology_file,fault_file,mindep_file,tmp_path,bbox,c_l,dst_crs,local_paths):

    y_point_list = [bbox[1], bbox[1], bbox[3], bbox[3], bbox[1]]
    x_point_list = [bbox[0], bbox[2], bbox[2], bbox[0], bbox[0]]
    bbox_geom = Polygon(zip(x_point_list, y_point_list))
    polygo = gpd.GeoDataFrame(index=[0], crs=dst_crs, geometry=[bbox_geom]) 

    m2l_errors=[]
    m2l_warnings=[]
    if(local_paths):
        for file_name in (structure_file,geology_file,fault_file,mindep_file):
            if not os.path.isfile(file_name):
                m2l_errors.append('file '+file_name+' not found')
    
    if (os.path.isfile(structure_file) or not local_paths):
        orientations = gpd.read_file(structure_file,bbox=bbox)
        if(len(orientations)<2):
            m2l_errors.append('not enough orientations to complete calculations (need at least 2)')

        orientations = orientations.replace(r'^\s+$', np.nan, regex=True)        

        for code in ('sf','d','dd','gi'):
            if not c_l[code] in orientations.columns:
                if(code=='sf'):
                    orientations[c_l[code]]='Bed'
                    m2l_warnings.append('field named "'+str(c_l[code])+'" added with default value "Bed"')
                elif(not code=='gi'):
                    m2l_errors.append('"'+c_l[code]+'" field needed')
                else:
                    m2l_warnings.append('field named "'+str(c_l[code])+'" added with default value')
                    orientations[c_l[code]] = np.arange(len(orientations))
            else:
                nans=orientations[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of orientations file, replacing with 0')
                    orientations[c_l[code]].fillna("0", inplace = True)


        unique_o=set(orientations[c_l['gi']])

        if(not len(unique_o) == len(orientations)):
            m2l_warnings.append('duplicate orientation point unique IDs')
        show_metadata(orientations,"orientations layer")    
            
    if (os.path.isfile(geology_file) or not local_paths):
        geology = gpd.read_file(geology_file,bbox=bbox)
        if not c_l['o'] in geology.columns:
            geology = geology.reset_index()
            geology[c_l['o']]=geology.index
        unique_g=set(geology[c_l['o']])

        if(not len(unique_g) == len(geology)):
            m2l_warnings.append('duplicate geology polygon unique IDs')
        
        geology = geology.replace(r'^\s+$', np.nan, regex=True)
        geology[c_l['g']].fillna(geology[c_l['g2']], inplace=True)
        geology[c_l['g']].fillna(geology[c_l['c']], inplace=True)
        
        for code in ('c','g','g2','ds','u','r1'):
            if(c_l[code] in geology.columns):
                geology[c_l[code]].str.replace(","," ")        
                if(code == 'c' or code =='g' or code=='g2'):
                    geology[c_l[code]].str.replace(" ","_")        
                    geology[c_l[code]].str.replace("-","_")        

                nans=geology[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of geology file, replacing with 0')
                    geology[c_l[code]].fillna("0", inplace = True)
            
        show_metadata(geology,"geology layer")    
        
    if (os.path.isfile(fault_file) or not local_paths):
        fault_folds = gpd.read_file(fault_file,bbox=bbox)    
        fault_folds = fault_folds.replace(r'^\s+$', np.nan, regex=True)        
        
        

        for code in ('f','o','fdip','fdipdir','fdipest'):
            if not c_l['f'] in fault_folds.columns:
                m2l_errors.append('field named "'+str(c_l[code])+'" not found in fault/fold file')
            elif not c_l['o'] in fault_folds.columns:
                m2l_warnings.append('field named "'+str(c_l[code])+'" added with default value')
                fault_folds[c_l[code]] = np.arange(len(fault_folds))
            elif not c_l[code] in fault_folds.columns:
                m2l_errors.append('field named "'+str(c_l[code])+'" not found in fault/fold file')
                
            if(c_l[code] in fault_folds.columns):
                nans=fault_folds[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of fault file, replacing with -999')
                    fault_folds[c_l[code]].fillna("-999", inplace = True)

        unique_f=set(fault_folds[c_l['o']])

        if(not len(unique_f) == len(fault_folds)):
            m2l_errors.append('duplicate fault/fold polyline unique IDs')

        fault_folds = fault_folds.replace(r'^\s+$', np.nan, regex=True)        

        faults_clip=m2l_utils.clip_shp(fault_folds,polygo)

        if(len(faults_clip)>0):
            faults_explode=explode_polylines(faults_clip,c_l,dst_crs)     
            if(len(faults_explode)>len(faults_clip)):
               m2l_warnings.append('some faults are MultiPolyLines, and have been split')
            faults_explode.crs = dst_crs
            
            show_metadata(faults_explode,"fault layer")    
        else: 

            #fault_file='None'
            print('No faults in area')
            
    if (os.path.isfile(mindep_file) or not local_paths):
        mindeps = gpd.read_file(mindep_file,bbox=bbox) 
        if(len(mindeps)==0):
            m2l_warnings.append('no mindeps for analysis')
        else:
            mindeps = mindeps.replace(r'^\s+$', np.nan, regex=True)        
        
            for code in ('msc','msn','mst','mtc','mscm','mcom'):
                if not c_l[code] in mindeps.columns:
                    m2l_errors.append('field named "'+str(c_l[code])+'" not found in mineral deposits file')
                else:
                    nans=mindeps[c_l[code]].isnull().sum() 
                    if(nans>0):
                        m2l_warnings.append(str(nans)+' NaN/blank found in column '+str(c_l[code])+' of mindep file, replacing with 0')
                        mindeps[c_l[code]].fillna("0", inplace = True)
        show_metadata(mindeps,"mindeps layer")    

        # explode fault/fold multipolylines
        # sometimes faults go off map and come back in again which after clipping creates multipolylines

    if(len(m2l_warnings)>0):
        print("\nWarnings:")
        warnings.warn('The warnings listed above were issued') 
        for w in m2l_warnings:
            print("    ",w)
    if(len(m2l_errors)>0):
        print("\nErrors:")
        warnings.warn('The errors listed above must be fixed prior to rerunning map2loop')                            
        for e in m2l_errors:
            print("    ",e)
        raise NameError('map2loop error: Fix errors before running again')
    
    if(len(m2l_errors)==0):
        print('\nNo errors found, clipped and updated files saved to tmp')
        
        if(len(faults_clip)>0):
            fault_file=tmp_path+'faults_clip.shp'
            faults_explode.crs=dst_crs
            faults_explode.to_file(fault_file)         
        else:
            fault_file=tmp_path+'faults_clip.shp'
            print("\nFault layer metadata\n--------------------")             
            print("No faults found")
            
        geol_clip=gpd.overlay(geology, polygo, how='intersection')
        if(len(geol_clip)>0):
            geol_clip.crs=dst_crs
            geol_file=tmp_path+'geol_clip.shp'
            geol_clip.to_file(geol_file)         
        
        if(len(orientations)>0):
            structure_file=tmp_path+'structure_clip.shp'
            orientations.crs=dst_crs
            orientations.to_file(structure_file)         
        
        if(len(mindeps)>0):
            mindep_file=tmp_path+'mindeps_clip.shp'
            mindeps.crs=dst_crs
            mindeps.to_file(mindep_file)
        return(structure_file,geol_file,fault_file,mindep_file)

def show_metadata(gdf,name):
    if(len(gdf)>0):
        print("\n",name," metadata\n--------------------")
        print("    bbox",gdf.total_bounds)
        print("    CRS",gdf.crs)
        print("    # items",len(gdf))
        types=[]
        for i,g in gdf.iterrows():
            if(not g.geometry.type in types):
                types.append(g.geometry.type)
        
        print("    Data types",types)
    else:
        print("\n",name," metadata\n--------------------")
        print("    empty file, check contents") 


def check_map(structure_file,geology_file,fault_file,mindep_file,fold_file,tmp_path,bbox,c_l,dst_crs,local_paths):

    y_point_list = [bbox[1], bbox[1], bbox[3], bbox[3], bbox[1]]
    x_point_list = [bbox[0], bbox[2], bbox[2], bbox[0], bbox[0]]
    bbox_geom = Polygon(zip(x_point_list, y_point_list))
    polygo = gpd.GeoDataFrame(index=[0], crs=dst_crs, geometry=[bbox_geom]) 

    m2l_errors=[]
    m2l_warnings=[]
    if(local_paths):
        for file_name in (structure_file,geology_file,fault_file,mindep_file,fold_file):
            if not os.path.isfile(file_name):
                m2l_errors.append('file '+file_name+' not found')
    
    # Process orientation points
    
    if (os.path.isfile(structure_file) or not local_paths):
        orientations = gpd.read_file(structure_file,bbox=bbox)
        if(len(orientations)<2):
            m2l_errors.append('not enough orientations to complete calculations (need at least 2)')

        orientations = orientations.replace(r'^\s+$', np.nan, regex=True)        

        for code in ('sf','d','dd','gi'):
            if not c_l[code] in orientations.columns:
                if(code=='sf'):
                    orientations[c_l[code]]='Bed'
                    m2l_warnings.append('field named "'+str(c_l[code])+'" added with default value "Bed"')
                elif(not code=='gi'):
                    m2l_errors.append('"'+c_l[code]+'" field needed')
                else:
                    m2l_warnings.append('field named "'+str(c_l[code])+'" added with default value')
                    orientations[c_l[code]] = np.arange(len(orientations))
            else:
                nans=orientations[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of orientations file, replacing with 0')
                    orientations[c_l[code]].fillna("0", inplace = True)


        unique_o=set(orientations[c_l['gi']])

        if(not len(unique_o) == len(orientations)):
            m2l_warnings.append('duplicate orientation point unique IDs')
        show_metadata(orientations,"orientations layer")    
            
    # Process geology polygons
    
    if (os.path.isfile(geology_file) or not local_paths):
        geology = gpd.read_file(geology_file,bbox=bbox)
        
        if not c_l['o'] in geology.columns:
            geology = geology.reset_index()
            geology[c_l['o']]=geology.index
        unique_g=set(geology[c_l['o']])

        if(not len(unique_g) == len(geology)):
            m2l_warnings.append('duplicate geology polygon unique IDs')
    
        
        geology = geology.replace(r'^\s+$', np.nan, regex=True)
        geology[c_l['g']].fillna(geology[c_l['g2']], inplace=True)
        geology[c_l['g']].fillna(geology[c_l['c']], inplace=True)
        
        
        
        for code in ('c','g','g2','ds','u','r1'):
            if(c_l[code] in geology.columns):
                geology[c_l[code]].str.replace(","," ")        
                if(code == 'c' or code =='g' or code=='g2'):
                    geology[c_l[code]].str.replace(" ","_")        
                    geology[c_l[code]].str.replace("-","_")        

                nans=geology[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of geology file, replacing with 0')
                    geology[c_l[code]].fillna("0", inplace = True)
            
        show_metadata(geology,"geology layer")   
        
    # Process fold polylines
    
    if (os.path.isfile(fold_file) or not local_paths):
        folds = gpd.read_file(fold_file,bbox=bbox)
        if(len(folds)>0):
            if not c_l['o'] in folds.columns:
                folds = folds.reset_index()
                folds[c_l['o']]=folds.index
            unique_g=set(folds[c_l['o']])

            if(not len(unique_g) == len(folds)):
                m2l_warnings.append('duplicate fold polyline unique IDs')

            folds = folds.replace(r'^\s+$', np.nan, regex=True)

            for code in ('ff','t'):
                if(c_l[code] in folds.columns):
                    folds[c_l[code]].str.replace(","," ")        

                    nans=folds[c_l[code]].isnull().sum() 
                    if(nans>0):
                        m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of folds file, replacing with 0')
                        folds[c_l[code]].fillna("0", inplace = True)

            folds_clip=m2l_utils.clip_shp(folds,polygo)

            show_metadata(folds_clip,"fold layer")    
        else: 
            print('No folds in area')
        
    # Process fault polylines
    
    if (os.path.isfile(fault_file) or not local_paths):
        faults_folds = gpd.read_file(fault_file,bbox=bbox) 
        
        
        faults = faults_folds[faults_folds[c_l['f']].str.contains(c_l['fault'])]        
        faults = faults.replace(r'^\s+$', np.nan, regex=True)        

        if not c_l['o'] in faults.columns:
            m2l_warnings.append('field named "'+str(c_l['o'])+'" added with default value')
            faults[c_l['o']] = np.arange(len(faults))

        for code in ('f','o','fdip','fdipdir','fdipest'):
        
            if not c_l[code] in faults.columns:
                m2l_errors.append('field named "'+str(c_l[code])+'" not found in fault/fold file')
                
            if(c_l[code] in faults.columns):
                nans=faults[c_l[code]].isnull().sum() 
                if(nans>0):
                    m2l_warnings.append(''+str(nans)+' NaN/blank found in column "'+str(c_l[code])+'" of fault file, replacing with -999')
                    faults[c_l[code]].fillna("-999", inplace = True)

        unique_f=set(faults[c_l['o']])
        
        

        if(not len(unique_f) == len(faults)):
            m2l_errors.append('duplicate fault/fold polyline unique IDs')

        faults = faults.replace(r'^\s+$', np.nan, regex=True)        

        faults_clip=m2l_utils.clip_shp(faults,polygo)

        if(len(faults_clip)>0):
            faults_explode=explode_polylines(faults_clip,c_l,dst_crs)     
            if(len(faults_explode)>len(faults_clip)):
                m2l_warnings.append('some faults are MultiPolyLines, and have been split')
            faults_explode.crs = dst_crs
            
            show_metadata(faults_explode,"fault layer")    
        else: 

            #fault_file='None'
            print('No faults in area')
            
    # Process mindep points
    
    if (os.path.isfile(mindep_file) or not local_paths):
        mindeps = gpd.read_file(mindep_file,bbox=bbox) 
        if(len(mindeps)==0):
            m2l_warnings.append('no mindeps for analysis')
        else:
            mindeps = mindeps.replace(r'^\s+$', np.nan, regex=True)        
        
            for code in ('msc','msn','mst','mtc','mscm','mcom'):
                if not c_l[code] in mindeps.columns:
                    m2l_errors.append('field named "'+str(c_l[code])+'" not found in mineral deposits file')
                else:
                    nans=mindeps[c_l[code]].isnull().sum() 
                    if(nans>0):
                        m2l_warnings.append(str(nans)+' NaN/blank found in column '+str(c_l[code])+' of mindep file, replacing with 0')
                        mindeps[c_l[code]].fillna("0", inplace = True)
        show_metadata(mindeps,"mindeps layer")    

        # explode fault/fold multipolylines
        # sometimes faults go off map and come back in again which after clipping creates multipolylines

    if(len(m2l_warnings)>0):
        print("\nWarnings:")
        warnings.warn('The warnings listed above were issued') 
        for w in m2l_warnings:
            print("    ",w)
    if(len(m2l_errors)>0):
        print("\nErrors:")
        warnings.warn('The errors listed above must be fixed prior to rerunning map2loop')                            
        for e in m2l_errors:
            print("    ",e)
        raise NameError('map2loop error: Fix errors before running again')
    
    if(len(m2l_errors)==0):
        print('\nNo errors found, clipped and updated files saved to tmp')
        
        if(len(folds)>0):
            fold_file=tmp_path+'folds_clip.shp'
            folds_clip.to_file(fold_file)         
        else:
            fold_file=tmp_path+'fold_clip.shp'
            print("\nFold layer metadata\n--------------------")             
            print("No folds found")
        
        if(len(faults_clip)>0):
            fault_file=tmp_path+'faults_clip.shp'
            faults_explode.crs=dst_crs
            faults_explode.to_file(fault_file)         
        else:
            fault_file=tmp_path+'faults_clip.shp'
            print("\nFault layer metadata\n--------------------")             
            print("No faults found")
            
            
        geol_clip=gpd.overlay(geology, polygo, how='intersection')
        if(len(geol_clip)>0):
            geol_clip.crs=dst_crs
            geol_file=tmp_path+'geol_clip.shp'
            geol_clip.to_file(geol_file)         
        
        if(len(orientations)>0):
            structure_file=tmp_path+'structure_clip.shp'
            orientations.crs=dst_crs
            orientations[c_l['dd']] = pd.to_numeric(orientations[c_l['dd']])
            orientations[c_l['d']] = pd.to_numeric(orientations[c_l['d']])

            orientations.to_file(structure_file)         
        
        if(len(mindeps)>0):
            mindep_file=tmp_path+'mindeps_clip.shp'
            mindeps.crs=dst_crs
            mindeps.to_file(mindep_file)
        return(structure_file,geol_file,fault_file,mindep_file,fold_file) 