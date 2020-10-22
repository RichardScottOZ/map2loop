# from map2loop import m2l_topology
import networkx as nx
import random
import numpy as np
import pandas as pd
import os
import geopandas as gpd
import rasterio
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from rasterio.transform import from_origin
from rasterio.io import MemoryFile
import matplotlib
from map2loop import m2l_utils

##########################################################################
# Save out and compile taskfile needed to generate geomodeller model using the geomodellerbatch engine
#
# loop2geomodeller(test_data_path,tmp_path,output_path,save_faults,compute_etc)
# Args:
# test_data_path root directory of test data
# tmp_path directory of temporary outputs
# output_path directory of outputs
# ave_faults flag for saving faults or not
# compute_etc flag for actual calculations or just project output
#
# Creates geomodeller taskfile files from varous map2loop outputs
##########################################################################
def loop2geomodeller(model_name,test_data_path,tmp_path,output_path,dtm_file,bbox,
                     model_top,model_base,save_faults,compute_etc,workflow):

    f=open(test_data_path+'/'+model_name+'/m2l.taskfile','w')
    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Project Header-----------------------\n')
    f.write('#---------------------------------------------------------------\n')
    f.write('name: "UWA_Intrepid"\n')
    f.write('description: "Automate_batch_Model"\n')
    f.write('    GeomodellerTask {\n')
    f.write('    CreateProject {\n')
    f.write('        name: "Hamersley"\n')
    f.write('        author: "Mark"\n')
    f.write('        date: "23/10/2019  0: 0: 0"\n')
    f.write('        projection { map_projection: "GDA94 / MGA50"}\n')
    f.write('        version: "2.0"\n')
    f.write('        units: meters\n')
    f.write('        precision: 1.0\n')
    f.write('        Extents {\n')
    f.write('            xmin: '+str(bbox[0])+'\n')
    f.write('            ymin: '+str(bbox[1])+'\n')
    f.write('            zmin: '+str(model_base)+'\n')
    f.write('            xmax: '+str(bbox[2])+'\n')
    f.write('            ymax: '+str(bbox[3])+'\n')
    f.write('            zmax: '+str(model_top)+'\n')
    f.write('        }\n')
    f.write('        deflection2d: 0.001\n')
    f.write('        deflection3d: 0.001\n')
    f.write('        discretisation: 10.0\n')
    f.write('        referenceTop: false\n')
    f.write('        CustomDTM {\n')
    f.write('            Extents {\n')
    f.write('            xmin: '+str(bbox[0])+'\n')
    f.write('            ymin: '+str(bbox[1])+'\n')
    f.write('            xmax: '+str(bbox[2])+'\n')
    f.write('            ymax: '+str(bbox[3])+'\n')
    f.write('            }\n')
    f.write('            name: "Topography"\n')
    f.write('            filename {\n')
    f.write('                Grid_Name: "'+dtm_file+'"\n')
    f.write('            }\n')
    f.write('            nx: 10\n')
    f.write('            ny: 10\n')
    f.write('        }\n')
    f.write('    }\n')
    f.write('}\n')


    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')

    empty_fm=[]

    for indx,afm in all_sorts.iterrows():
        foundcontact=False
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] in afm['code']):
                foundcontact=True
                break
        foundorientation=False
        for indx3,ano in orientations.iterrows():
            if(ano['formation'] in afm['code']):
                foundorientation=True
                break
        if(not foundcontact or not foundorientation):
            empty_fm.append(afm['code'])

    #print(empty_fm)
    asc=pd.read_csv(tmp_path+'all_sorts_clean.csv',",")

    all_sorts=np.genfromtxt(tmp_path+'all_sorts_clean.csv',delimiter=',',dtype='U100')
    nformations=len(all_sorts)

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Create Formations-----------------------\n')
    f.write('#---------------------------------------------------------------\n')
       
    for ind,row in asc.iterrows():
        if( not row['code'] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('CreateFormation {\n')
    
            ostr='    name: "'+row['code'].replace("\n","")+'"\n'  
            f.write(ostr)            
            r,g,b=m2l_utils.hextoints(row['colour'])
            ostr='    red: '+str(int(r))+'\n'
            f.write(ostr)
    
            ostr='    green: '+str(int(g))+'\n'
            f.write(ostr)

            ostr='    blue: '+str(int(b))+'\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Set Stratigraphic Pile------------------\n')
    f.write('#---------------------------------------------------------------\n')
      
             
    for i in range (1,nformations):
    #for i in range (nformations-1,0,-1):
        if(all_sorts[i,2]==str(1)):
            f.write('GeomodellerTask {\n')
            f.write('SetSeries {\n')

            ostr='    name: "'+all_sorts[i][5].replace("\n","")+'"\n'
            f.write(ostr)

            ostr='    position: 1\n'
            f.write(ostr)

            ostr='    relation: "erode"\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')

            for j in range(nformations-1,0,-1):
    #        for j in range(1,nformations):
                if(all_sorts[j,1]==all_sorts[i,1]):
                    if( not all_sorts[j][4] in empty_fm):
                        f.write('GeomodellerTask {\n')
                        f.write('AddFormationToSeries {\n')

                        ostr='    series: "'+all_sorts[j][5]+'"\n'
                        f.write(ostr)

                        ostr='    formation: "'+all_sorts[j][4]+'"\n'
                        f.write(ostr)

                        f.write('    }\n')
                        f.write('}\n')    

    if(save_faults):
        output_path=test_data_path+'output/'

        faults_len=pd.read_csv(output_path+'fault_dimensions.csv')

        n_allfaults=len(faults_len)

        fcount=0
        for i in range(0,n_allfaults):
            f.write('GeomodellerTask {\n')
            f.write('CreateFault {\n')
            r,g,b=m2l_utils.hextoints(str(faults_len.iloc[i]["colour"]))
            ostr='    name: "'+faults_len.iloc[i]["Fault"]+'"\n'
            f.write(ostr)

            ostr='    red: '+str(r)+'\n'
            f.write(ostr)

            ostr='    green: '+str(g)+'\n'
            f.write(ostr)

            ostr='    blue: '+str(b)+'\n'
            f.write(ostr)

            f.write('    }\n')
            f.write('}\n')
            fcount=fcount+1
            
            f.write('GeomodellerTask {\n')
            f.write('    Set3dFaultLimits {\n')
            f.write('        Fault_name: "'+faults_len.iloc[i]["Fault"]+ '"\n')
            f.write('        Horizontal: '+str(faults_len.iloc[i]["HorizontalRadius"])+ '\n')
            f.write('        Vertical: '+str(faults_len.iloc[i]["VerticalRadius"])+ '\n')
            f.write('        InfluenceDistance: '+str(faults_len.iloc[i]["InfluenceDistance"])+ '\n')
            f.write('    }\n')
            f.write('}\n')
            

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Import 3D contact data ---Base Model----\n')
    f.write('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(afm[0])
        if( not afm['code'] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('    Add3DInterfacesToFormation {\n')
            f.write('          formation: "'+str(afm['code'])+'"\n')

            for indx2,acontact in contacts.iterrows():
                if(acontact['formation'] in afm['code'] ):
                    ostr='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                    f.write(ostr)
            f.write('    }\n')
            f.write('}\n')
    f.write('#---------------------------------------------------------------\n')
    f.write('#------------------Import 3D orientation data ---Base Model-----\n')
    f.write('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(groups[agp])
        if( not afm['code'] in empty_fm):
            f.write('GeomodellerTask {\n')
            f.write('    Add3DFoliationToFormation {\n')
            f.write('          formation: "'+str(afm['code'])+'"\n')
            for indx2,ano in orientations.iterrows():
                if(ano['formation'] in afm['code']):
                    f.write('           foliation {\n')
                    ostr='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                    f.write(ostr)
                    ostr='                  direction: '+str(ano['azimuth'])+'\n'
                    f.write(ostr)
                    ostr='                  dip: '+str(ano['dip'])+'\n'
                    f.write(ostr)
                    if(ano['polarity']==1):
                        ostr='                  polarity: Normal_Polarity\n'
                    else:
                        ostr='                  polarity: Reverse_Polarity\n'
                    f.write(ostr)            
                    ostr='           }\n'
                    f.write(ostr)
            f.write('    }\n')
            f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#-----------------------Import 3D fault data ---Base Model------\n')
    f.write('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'faults.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        f.write('GeomodellerTask {\n')
        f.write('    Add3DInterfacesToFormation {\n')
        f.write('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] == afault['Fault']):
                ostr='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                f.write(ostr)
        f.write('    }\n')
        f.write('}\n')

    f.write('#---------------------------------------------------------------\n')
    f.write('#------------------Import 3D fault orientation data ------------\n')
    f.write('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'fault_orientations.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        f.write('GeomodellerTask {\n')
        f.write('    Add3DFoliationToFormation {\n')
        f.write('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,ano in orientations.iterrows():
            if(ano['formation'] == afault['Fault']):
                f.write('           foliation {\n')
                ostr='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                f.write(ostr)
                ostr='                  direction: '+str(ano['DipDirection'])+'\n'
                f.write(ostr)
                if(ano['dip'] == -999):
                    ostr='                  dip: '+str(random.randint(60,90))+'\n'
                else:    
                    ostr='                  dip: '+str(ano['dip'])+'\n'
                f.write(ostr)
                if(ano['DipPolarity']==1):
                    ostr='                  polarity: Normal_Polarity\n'
                else:
                    ostr='                  polarity: Reverse_Polarity\n'
                f.write(ostr)            
                ostr='           }\n'
                f.write(ostr)
        f.write('    }\n')
        f.write('}\n')

    if(save_faults):
        G=nx.read_gml(tmp_path+"fault_network.gml",label='label')
        #nx.draw(G, with_labels=True, font_weight='bold')
        edges=list(G.edges)
        #for i in range(0,len(edges)):
            #print(edges[i][0],edges[i][1])
        cycles=list(nx.simple_cycles(G))
        #display(cycles)
        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Link faults with faults ----------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    LinkFaultsWithFaults {\n')

        for i in range(0,len(edges)):
                found=False
                for j in range(0,len(cycles)):
                    if(edges[i][0]== cycles[j][0] and edges[i][1]== cycles[j][1]):
                        found=True # fault pair is first two elements in a cycle list so don't save to taskfile
                if(not found):
                    ostr='        FaultStopsOnFaults{ fault: "'+edges[i][1]+'"; stopson: "'+edges[i][0]+'"}\n'
                    f.write(ostr)

        f.write('    }\n')
        f.write('}\n')

    if(save_faults):
        all_fault_group=np.genfromtxt(output_path+'group-fault-relationships.csv',delimiter=',',dtype='U100')
        ngroups=len(all_fault_group)
        all_fault_group=np.transpose(all_fault_group)
        nfaults=len(all_fault_group)

        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Link series with faults ----------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    LinkFaultsWithSeries {\n')

        for i in range(1,nfaults):
            first=True
            for j in range(1,ngroups):
                if(all_fault_group[i,j]==str(1)):
                    if(first):
                        ostr='    FaultSeriesLinks{ fault: "'+all_fault_group[i,0]+'"; series: ['
                        f.write(ostr)
                        ostr='"'+all_fault_group[0,j]+'"'
                        f.write(ostr)
                        first=False
                    else:
                        ostr=', "'+all_fault_group[0,j]+'"'
                        f.write(ostr)
            if(not first):
                ostr=']}\n'
                f.write(ostr)

        f.write('    }\n')
        f.write('}\n')
    

    f.write('GeomodellerTask {\n')
    f.write('    SaveProjectAs {\n')
    f.write('        filename: "./'+model_name+'.xml"\n')
    f.write('    }\n')
    f.write('}\n')
    f.close()
    

    if(compute_etc):
        f=open(test_data_path+model_name+'/'+'m2l_compute.taskfile','w')
        f.write('#---------------------------------------------------------------\n')
        f.write('#----------------------------Load Model----------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    OpenProjectNoGUI {\n')
        f.write('        filename: "./'+model_name+'.xml"\n')
        f.write('    }\n')
        f.write('}\n')
     
        f.write('#---------------------------------------------------------------\n')
        f.write('#----------------------------Compute Model----------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
        f.write('GeomodellerTask {\n')
        f.write('    ComputeModel {\n')
        f.write('        SeriesList {\n')
        f.write('            node: "All" \n')
        f.write('        }\n')
        f.write('        SectionList {\n')
        f.write('            node: "All"\n')
        f.write('        }\n')
        f.write('        FaultList {\n')
        f.write('            node: "All"\n')
        f.write('        }\n')
        f.write('        radius: 10.0\n')
        f.write('    }\n')
        f.write('}\n')

        f.write('#---------------------------------------------------------------\n')
        f.write('#-----------------------Add geophysical Properties--------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('#--------------------------Export Lithology Voxet---------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('GeomodellerTask {\n')
        f.write('    SaveLithologyVoxet {\n')
        f.write('        nx: 25\n')
        f.write('        ny: 25\n')
        f.write('        nz: 40\n')
        f.write('        LithologyVoxetFileStub: "./Litho_Voxet/LithoVoxet.vo"\n')
        f.write('    }\n')
        f.write('}\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('#--------------------------Save As Model------------------------\n')
        f.write('#---------------------------------------------------------------\n')
        f.write('\n')
    
        f.write('GeomodellerTask {\n')
        f.write('    SaveProjectAs {\n')
        f.write('        filename: "/'+model_name+'.xml"\n')
        f.write('    }\n')
        f.write('}\n')   
        f.write('GeomodellerTask {\n')
        f.write('    CloseProjectNoGUI {\n')
        f.write('    }\n')
        f.write('}\n')

        f.close()
        
# same same expect it builds a list that then gets written all at once (this version is slower!)        
def loop2geomodeller2(model_name,test_data_path,tmp_path,output_path,dtm_file,bbox,save_faults,compute_etc,workflow):

    f=open(test_data_path+'/'+model_name+'/m2l.taskfile','w')
    ostr=[]
    
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Project Header-----------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('name: "UWA_Intrepid"\n')
    ostr.append('description: "Automate_batch_Model"\n')
    ostr.append('    GeomodellerTask {\n')
    ostr.append('    CreateProject {\n')
    ostr.append('        name: "Hamersley"\n')
    ostr.append('        author: "Mark"\n')
    ostr.append('        date: "23/10/2019  0: 0: 0"\n')
    ostr.append('        projection { map_projection: "GDA94 / MGA50"}\n')
    ostr.append('        version: "2.0"\n')
    ostr.append('        units: meters\n')
    ostr.append('        precision: 1.0\n')
    ostr.append('        Extents {\n')
    ostr.append('            xmin: '+str(bbox[0])+'\n')
    ostr.append('            ymin: '+str(bbox[1])+'\n')
    ostr.append('            zmin: -7000\n')
    ostr.append('            xmax: '+str(bbox[2])+'\n')
    ostr.append('            ymax: '+str(bbox[3])+'\n')
    ostr.append('            zmax: 1200\n')
    ostr.append('        }\n')
    ostr.append('        deflection2d: 0.001\n')
    ostr.append('        deflection3d: 0.001\n')
    ostr.append('        discretisation: 10.0\n')
    ostr.append('        referenceTop: false\n')
    ostr.append('        CustomDTM {\n')
    ostr.append('            Extents {\n')
    ostr.append('            xmin: '+str(bbox[0])+'\n')
    ostr.append('            ymin: '+str(bbox[1])+'\n')
    ostr.append('            xmax: '+str(bbox[2])+'\n')
    ostr.append('            ymax: '+str(bbox[3])+'\n')
    ostr.append('            }\n')
    ostr.append('            name: "Topography"\n')
    ostr.append('            filename {\n')
    ostr.append('                Grid_Name: "'+dtm_file+'"\n')
    ostr.append('            }\n')
    ostr.append('            nx: 10\n')
    ostr.append('            ny: 10\n')
    ostr.append('        }\n')
    ostr.append('    }\n')
    ostr.append('}\n')


    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')

    empty_fm=[]

    for indx,afm in all_sorts.iterrows():
        foundcontact=False
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] in afm['code']):
                foundcontact=True
                break
        foundorientation=False
        for indx3,ano in orientations.iterrows():
            if(ano['formation'] in afm['code']):
                foundorientation=True
                break
        if(not foundcontact or not foundorientation):
            empty_fm.append(afm['code'])

    #print(empty_fm)

    all_sorts=np.genfromtxt(tmp_path+'all_sorts_clean.csv',delimiter=',',dtype='U100')
    nformations=len(all_sorts)

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Create Formations-----------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
       
    for i in range (1,nformations):
        if( not all_sorts[i,4] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('CreateFormation {\n')

            ostr2='    name: "'+all_sorts[i,4].replace("\n","")+'"\n'
            ostr.append(ostr2)

            ostr2='    red: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    green: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    blue: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Set Stratigraphic Pile------------------\n')
    ostr.append('#---------------------------------------------------------------\n')
      
             
    for i in range (1,nformations):
    #for i in range (nformations-1,0,-1):
        if(all_sorts[i,2]==str(1)):
            ostr.append('GeomodellerTask {\n')
            ostr.append('SetSeries {\n')

            ostr2='    name: "'+all_sorts[i][5].replace("\n","")+'"\n'
            ostr.append(ostr2)

            ostr2='    position: 1\n'
            ostr.append(ostr2)

            ostr2='    relation: "erode"\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')

            for j in range(nformations-1,0,-1):
    #        for j in range(1,nformations):
                if(all_sorts[j,1]==all_sorts[i,1]):
                    if( not all_sorts[j][4] in empty_fm):
                        ostr.append('GeomodellerTask {\n')
                        ostr.append('AddFormationToSeries {\n')

                        ostr2='    series: "'+all_sorts[j][5]+'"\n'
                        ostr.append(ostr2)

                        ostr2='    formation: "'+all_sorts[j][4]+'"\n'
                        ostr.append(ostr2)

                        ostr.append('    }\n')
                        ostr.append('}\n')    

    if(save_faults):
        output_path=test_data_path+'output/'

        faults_len=pd.read_csv(output_path+'fault_dimensions.csv')

        n_allfaults=len(faults_len)

        fcount=0
        for i in range(0,n_allfaults):
            ostr.append('GeomodellerTask {\n')
            ostr.append('CreateFault {\n')
            ostr2='    name: "'+faults_len.iloc[i]["Fault"]+'"\n'
            ostr.append(ostr2)

            ostr2='    red: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    green: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr2='    blue: '+str(random.randint(1,256)-1)+'\n'
            ostr.append(ostr2)

            ostr.append('    }\n')
            ostr.append('}\n')
            fcount=fcount+1
            
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Set3dFaultLimits {\n')
            ostr.append('        Fault_name: "'+faults_len.iloc[i]["Fault"]+ '"\n')
            ostr.append('        Horizontal: '+str(faults_len.iloc[i]["HorizontalRadius"])+ '\n')
            ostr.append('        Vertical: '+str(faults_len.iloc[i]["VerticalRadius"])+ '\n')
            ostr.append('        InfluenceDistance: '+str(faults_len.iloc[i]["InfluenceDistance"])+ '\n')
            ostr.append('    }\n')
            ostr.append('}\n')
            

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Import 3D contact data ---Base Model----\n')
    ostr.append('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'contacts_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(afm[0])
        if( not afm['code'] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Add3DInterfacesToFormation {\n')
            ostr.append('          formation: "'+str(afm['code'])+'"\n')

            for indx2,acontact in contacts.iterrows():
                if(acontact['formation'] in afm['code'] ):
                    ostr2='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                    ostr.append(ostr2)
            ostr.append('    }\n')
            ostr.append('}\n')
    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#------------------Import 3D orientation data ---Base Model-----\n')
    ostr.append('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'orientations_clean.csv',',')
    all_sorts=pd.read_csv(tmp_path+'all_sorts_clean.csv',',')
    #all_sorts.set_index('code',  inplace = True)
    #display(all_sorts)

    for inx,afm in all_sorts.iterrows():
        #print(groups[agp])
        if( not afm['code'] in empty_fm):
            ostr.append('GeomodellerTask {\n')
            ostr.append('    Add3DFoliationToFormation {\n')
            ostr.append('          formation: "'+str(afm['code'])+'"\n')
            for indx2,ano in orientations.iterrows():
                if(ano['formation'] in afm['code']):
                    ostr.append('           foliation {\n')
                    ostr2='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                    ostr.append(ostr2)
                    ostr2='                  direction: '+str(ano['azimuth'])+'\n'
                    ostr.append(ostr2)
                    ostr2='                  dip: '+str(ano['dip'])+'\n'
                    ostr.append(ostr2)
                    if(ano['polarity']==1):
                        ostr2='                  polarity: Normal_Polarity\n'
                    else:
                        ostr2='                  polarity: Reverse_Polarity\n'
                    ostr.append(ostr2)            
                    ostr2='           }\n'
                    ostr.append(ostr2)
            ostr.append('    }\n')
            ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#-----------------------Import 3D fault data ---Base Model------\n')
    ostr.append('#---------------------------------------------------------------\n')

    contacts=pd.read_csv(output_path+'faults.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        ostr.append('GeomodellerTask {\n')
        ostr.append('    Add3DInterfacesToFormation {\n')
        ostr.append('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,acontact in contacts.iterrows():
            if(acontact['formation'] == afault['Fault']):
                ostr2='              point {x:'+str(acontact['X'])+'; y:'+str(acontact['Y'])+'; z:'+str(acontact['Z'])+'}\n'
                ostr.append(ostr2)
        ostr.append('    }\n')
        ostr.append('}\n')

    ostr.append('#---------------------------------------------------------------\n')
    ostr.append('#------------------Import 3D fault orientation data ------------\n')
    ostr.append('#---------------------------------------------------------------\n')

    orientations=pd.read_csv(output_path+'fault_orientations.csv',',')
    faults=pd.read_csv(output_path+'fault_dimensions.csv',',')

    for indx,afault in faults.iterrows():
        ostr.append('GeomodellerTask {\n')
        ostr.append('    Add3DFoliationToFormation {\n')
        ostr.append('          formation: "'+str(afault['Fault'])+'"\n')
        for indx2,ano in orientations.iterrows():
            if(ano['formation'] == afault['Fault']):
                ostr.append('           foliation {\n')
                ostr2='                  Point3D {x:'+str(ano['X'])+'; y:'+str(ano['Y'])+'; z:'+str(ano['Z'])+'}\n'
                ostr.append(ostr2)
                ostr2='                  direction: '+str(ano['DipDirection'])+'\n'
                ostr.append(ostr2)
                if(ano['dip'] == -999):
                    ostr2='                  dip: '+str(random.randint(60,90))+'\n'
                else:    
                    ostr2='                  dip: '+str(ano['dip'])+'\n'
                ostr.append(ostr2)
                if(ano['DipPolarity']==1):
                    ostr2='                  polarity: Normal_Polarity\n'
                else:
                    ostr2='                  polarity: Reverse_Polarity\n'
                ostr.append(ostr2)            
                ostr2='           }\n'
                ostr.append(ostr2)
        ostr.append('    }\n')
        ostr.append('}\n')

    if(save_faults):
        G=nx.read_gml(tmp_path+"fault_network.gml",label='label')
        #nx.draw(G, with_labels=True, font_weight='bold')
        edges=list(G.edges)
        #for i in range(0,len(edges)):
            #print(edges[i][0],edges[i][1])
        cycles=list(nx.simple_cycles(G))
        #display(cycles)
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Link faults with faults ----------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    LinkFaultsWithFaults {\n')

        for i in range(0,len(edges)):
                found=False
                for j in range(0,len(cycles)):
                    if(edges[i][0]== cycles[j][0] and edges[i][1]== cycles[j][1]):
                        found=True # fault pair is first two elements in a cycle list so don't save to taskfile
                if(not found):
                    ostr2='        FaultStopsOnFaults{ fault: "'+edges[i][1]+'"; stopson: "'+edges[i][0]+'"}\n'
                    ostr.append(ostr2)

        ostr.append('    }\n')
        ostr.append('}\n')

    if(save_faults):
        all_fault_group=np.genfromtxt(output_path+'group-fault-relationships.csv',delimiter=',',dtype='U100')
        ngroups=len(all_fault_group)
        all_fault_group=np.transpose(all_fault_group)
        nfaults=len(all_fault_group)

        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Link series with faults ----------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    LinkFaultsWithSeries {\n')

        for i in range(1,nfaults):
            first=True
            for j in range(1,ngroups):
                if(all_fault_group[i,j]==str(1)):
                    if(first):
                        ostr2='    FaultSeriesLinks{ fault: "'+all_fault_group[i,0]+'"; series: ['
                        ostr.append(ostr2)
                        ostr2='"'+all_fault_group[0,j]+'"'
                        ostr.append(ostr2)
                        first=False
                    else:
                        ostr2=', "'+all_fault_group[0,j]+'"'
                        ostr.append(ostr2)
            if(not first):
                ostr2=']}\n'
                ostr.append(ostr2)

        ostr.append('    }\n')
        ostr.append('}\n')
    

    ostr.append('GeomodellerTask {\n')
    ostr.append('    SaveProjectAs {\n')
    ostr.append('        filename: "./'+model_name+'.xml"\n')
    ostr.append('    }\n')
    ostr.append('}\n')
    f.close()
    

    if(compute_etc):
        f=open(test_data_path+model_name+'/'+'m2l_compute.taskfile','w')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#----------------------------Load Model----------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    OpenProjectNoGUI {\n')
        ostr.append('        filename: "./'+model_name+'.xml"\n')
        ostr.append('    }\n')
        ostr.append('}\n')
     
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#----------------------------Compute Model----------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    ComputeModel {\n')
        ostr.append('        SeriesList {\n')
        ostr.append('            node: "All" \n')
        ostr.append('        }\n')
        ostr.append('        SectionList {\n')
        ostr.append('            node: "All"\n')
        ostr.append('        }\n')
        ostr.append('        FaultList {\n')
        ostr.append('            node: "All"\n')
        ostr.append('        }\n')
        ostr.append('        radius: 10.0\n')
        ostr.append('    }\n')
        ostr.append('}\n')

        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#-----------------------Add geophysical Properties--------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
        ostr.append('\n')
        ostr.append('\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#--------------------------Export Lithology Voxet---------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('GeomodellerTask {\n')
        ostr.append('    SaveLithologyVoxet {\n')
        ostr.append('        nx: 25\n')
        ostr.append('        ny: 25\n')
        ostr.append('        nz: 40\n')
        ostr.append('        LithologyVoxetFileStub: "./Litho_Voxet/LithoVoxet.vo"\n')
        ostr.append('    }\n')
        ostr.append('}\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('#--------------------------Save As Model------------------------\n')
        ostr.append('#---------------------------------------------------------------\n')
        ostr.append('\n')
    
        ostr.append('GeomodellerTask {\n')
        ostr.append('    SaveProjectAs {\n')
        ostr.append('        filename: "/'+model_name+'.xml"\n')
        ostr.append('    }\n')
        ostr.append('}\n')   
        ostr.append('GeomodellerTask {\n')
        ostr.append('    CloseProjectNoGUI {\n')
        ostr.append('    }\n')
        ostr.append('}\n')
        f.writelines(ostr)
        f.close()

##########################################################################
# Import outputs from map2loop to LoopStructural and view with Lavavu
#
# loop2LoopStructural(thickness_file,orientation_file,contacts_file,bbox)
# Args:
# bbox model bounding box
#
# Calculates model and displays in LavaVu wthin notebook
##########################################################################
def loop2LoopStructural(m2l_directory):
    """ create a model from a map2loop directory

    [extended_summary]

    Parameters
    ----------
    m2l_directory : string
        path to the map2loop directory
    """
    visualise = False
    ## make sure everything is installed and can be imported
    try:
        from LoopStructural import GeologicalModel
        from LoopStructural.utils import process_map2loop
    except ImportError:
        print('Loop Structural not installed')
        return
    try:
        from LoopStructural.visualisation import LavaVuModelViewer
        visualise = True
    except ImportError:
        print("Lavavu is not installed, try installing it with pip \n"
              "Model will be built but cannot be visualised")

    m2l_data = process_map2loop(m2l_directory)
    boundary_points = np.zeros((2, 3))
    boundary_points[0, 0] = m2l_data['bounding_box']['minx']
    boundary_points[0, 1] = m2l_data['bounding_box']['miny']
    boundary_points[0, 2] = m2l_data['bounding_box']['lower']
    boundary_points[1, 0] = m2l_data['bounding_box']['maxx']
    boundary_points[1, 1] = m2l_data['bounding_box']['maxy']
    boundary_points[1, 2] = m2l_data['bounding_box']['upper']

    model = GeologicalModel(boundary_points[0, :], boundary_points[1, :])
    model.set_model_data(m2l_data['data'])

    faults = []
    for f in m2l_data['max_displacement'].keys():
        if model.data[model.data['type'] == f].shape[0] == 0:
            continue
        fault_id = f[6:]
        overprints = []
        try:
            overprint_id = m2l_data['fault_fault'][m2l_data['fault_fault'][fault_id] == 1]['fault_id'].to_numpy()
            for i in overprint_id:
                overprints.append(['Fault_%i' % i])
        except:
            print('No entry for %s in fault_fault_relations' % f)
        #     continue
        faults.append(model.create_and_add_fault(f,
                                                 -m2l_data['max_displacement'][f],
                                                 faultfunction='BaseFault',
                                                 interpolatortype='FDI',
                                                 nelements=1e4,
                                                 data_region=.1,
                                                 #                                                  regularisation=[1,1,1],
                                                 solver='pyamg',
                                                 #                                                  damp=True,
                                                 #                                                  buffer=0.1,
                                                 #                                                  steps=1,
                                                 overprints=overprints,
                                                 cpw=10,
                                                 npw=10
                                                 )
                      )

    ## loop through all of the groups and add them to the model in youngest to oldest.
    group_features = []
    for i in m2l_data['groups']['group number'].unique():
        g = m2l_data['groups'].loc[m2l_data['groups']['group number'] == i, 'group'].unique()[0]
        group_features.append(model.create_and_add_foliation(g,
                                                             interpolatortype="PLI",  # which interpolator to use
                                                             nelements=1e5,  # how many tetras/voxels
                                                             buffer=0.5,  # how much to extend nterpolation around box
                                                             solver='pyamg',
                                                             damp=True))
        # if the group was successfully added (not null) then lets add the base (0 to be unconformity)
        if group_features[-1]:
            model.add_unconformity(group_features[-1]['feature'], 0)
    model.set_stratigraphic_column(m2l_data['stratigraphic_column'])
    if visualise:
        viewer = LavaVuModelViewer(model)
        viewer.add_model(cmap='tab20')
        viewer.interactive()

    
    
##########################################################################
# Import outputs from map2loop to gempy and view with pyvtk
# loop2gempy(test_data_name,tmp_path,vtk_pth,orientations_file,contacts_file,groups_file,dtm_reproj_file,bbox,model_base, model_top,vtk)
# Args:
# test_data_name root name of project
# tmp_path path of temp files directory
# vtk_pth path of vtk output directory
# orientations_file path of orientations file
# contacts_file path of contacts file
# groups_file path of groups file
# dtm_reproj_file path of dtm file
# bbox model bounding box
# model_base z value ofbase of model 
# model_top z value of top of model
# vtk flag as to wether to save out model to vtk
#
# Calculates model and displays in external vtk viewer
##########################################################################
def loop2gempy(*args, **kwargs):
    """ Calculate the model using gempy as backend.

    At the moment there is not support for finite faults since gempy does not
     accept passing the ellipsoid parameters directly.

    :param contacts_file (str): path of contacts file
    :param orientations_file: path of orientations file
    :param bbox: model bounding box
    :param groups_file: path of groups file
    :param model_base: z value ofbase of model
    :param model_top: z value of top of model
    :param dtm_reproj_file: path of dtm file
    :param faults_contact: path of contacts file with fault data
    :param faults_orientations: path of orientations file with fault data
    :param faults_rel_matrix: bool matrix describing the interaction between groups. Rows offset columns
    :param faults_groups_rel: bool matrix describing the interaction between faults and features
    :param faults_faults_rel: bool matrix describing the interaction between faults and faults
    :param model_name: name of the model
    :param compute (bool): Default True. Whether or not compute the model
    :param vtk (bool): Default False. Whether or not visualize the model
    :param vtk_path (str): Default None. Path of vtk output directory
    :param plot_3d_kwargs (dict): kwargs for `gempy.plot_3d`
    :return: gempy.Project
    """
    from gempy.addons.map2gempy import loop2gempy
    geo_model = loop2gempy(*args, **kwargs)
    return geo_model

# Courtesy of https://gist.github.com/delestro/54d5a34676a8cef7477e

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np


    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap
    
def display_LS_map(model,dtm,geol_clip,faults_clip,dst_crs,use_cmap,cmap,use_topo,use_faults):
    
    if(not use_cmap):
        cmap = rand_cmap(100, type='soft', first_color_black=False, last_color_black=False, verbose=False)

    dtm_val = dtm.read(1)

    grid=np.array((dtm_val.shape[0]*dtm_val.shape[1],3))
    scale=(dtm.bounds[2]-dtm.bounds[0])/dtm_val.shape[1]
    x=np.linspace(dtm.bounds[0],dtm.bounds[2],dtm_val.shape[1])
    y=np.linspace(dtm.bounds[3],dtm.bounds[1],dtm_val.shape[0])
    xx, yy = np.meshgrid(x,y,indexing='ij')

    if(use_topo):
        zz = dtm_val.flatten()
    else:
        zz = np.zeros_like(xx)

    points = np.array([xx.flatten(order='F'),yy.flatten(order='F'),zz.flatten(order='F')]).T
    v = model.evaluate_model(model.scale(points),scale=False)
    transform = from_origin(dtm.bounds[0], dtm.bounds[3],scale,scale)

    
    memfile = MemoryFile()
    new_dataset = memfile.open( driver='GTiff',
                            height = dtm.shape[0], width = dtm.shape[1],
                            count=1, dtype='float64',
                            crs=dst_crs,
                            transform=transform)
    new_dataset.write(v.astype('float64').reshape(dtm_val.shape[0],dtm_val.shape[1]), 1)
    
    fig, ax = matplotlib.pyplot.subplots(figsize=(15, 15))
    rasterio.plot.show(new_dataset.read(1),transform=new_dataset.transform, cmap=cmap, ax=ax)
    geol_clip.plot(ax=ax, facecolor='none', edgecolor='black',linewidth=0.4)
    if(use_faults):
        faults_clip.plot(ax=ax, facecolor='none', edgecolor='red',linewidth=0.7)