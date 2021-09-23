import os, re

def delete_space(target_string):
    result_string=''
    for index in range(len(target_string)):
        if target_string[index]!=' ':
            result_string+=target_string[index]
    return result_string

def mm2pdb(input_file,output_file, water_flag):
########################定义,defination
    chain_id_list=['A','B','C','D']
    chain_id_list_hoh={'E':0,'F':0,'G':0,'H':0,'I':0, 'J':0,'K':0,'L':0,'M':0,'N':0,'O':0,'P':0,'Q':0,'R':0,'S':0,'T':0,'U':0,'V':0,'W':0,'X':0,'Y':0,'Z':0}
    last_res_number=1
    chain_id_index=0
    cutoff=8000
    flag_A=0
    flag_B=0
########################Read gromac files
    with open(output_file,mode='w',encoding='utf-8') as out_file:
        with open(input_file,mode='r',encoding='utf-8') as in_file:
##################delete first, second and last two lines
            all_line = in_file.readlines()[2:-2]
            #print(len(all_line))
            old_res_number=all_line[0][22:26]
            old_res_chain=all_line[0][20:22]
            for index, a_line in enumerate(all_line):  
##################delete 'CONECT' and 'TER' lines
                if a_line[0:6]=='CONECT' or a_line[0:3]=='TER' or a_line[0:6]=='ENDMDL' or a_line[0:5]=='MODEL':
                    continue
             
##################Read strings 
                res_chain_ini=a_line[20:22]
                res_number_ini=a_line[22:26]
                res_name_ini=a_line[16:20]
                atom_name_ini=a_line[11:16]
                atom_number_ini=a_line[6:11]
                x_coordinate_ini=a_line[26:38]
                y_coordinate_ini=a_line[38:46]
                z_coordinate_ini=a_line[46:54]
#################transfer data            
                res_number=int(res_number_ini)
                res_name=delete_space(res_name_ini)
                res_chain=delete_space(res_chain_ini)
                atom_number=int(atom_number_ini)
                atom_name=delete_space(atom_name_ini)
                x_coordinate=float(x_coordinate_ini)
                y_coordinate=float(y_coordinate_ini)
                z_coordinate=float(z_coordinate_ini)
                flag=' '            
########################去掉氢 delete H atom/OT
                if atom_name=='OT1' or atom_name=='OT2' or atom_name[0]=='H':
                    continue
########################cofactor重命名及简单处理 rename and simple dealt with cofactor  
# """   
#                 if atom_name[-1]=='0':
#                         atom_name=atom_name[0:-1]
#                         flag='b'
#                     elif atom_name[-1]=='1':
#                         atom_name=atom_name[0:-1]
#                         flag='c'
#                     elif atom_name[-1]=='4':
#                         atom_name=atom_name[0:-1]
#                         flag='a' 
#                     if atom_name=='OH2':
#                         atom_name='O'
#                 elif res_name=='CU2':
#                     res_name='CUA'
#                     atom_name='CU' 
                
# """      

######################## edit chain id and residue number for hoh

#if res_name=='POT' or res_name=='CLA' or res_name=='POPC' or res_name=='POP':
                #    continue
                if res_name=='POT' or res_name=='CLA' or res_name=='POPC':
                    continue
                current_res_number=all_line[index][22:26]
                current_res_chain=all_line[index][20:22]
                #print(res_name)
                #print(current_res_number, current_res_chain)
                #print(old_res_number, old_res_chain)
                #print("\n")
                if res_name=='HOH':
                    #if water_flag ==1, don't output water molecules, if 0, output water
                    if water_flag == 1:
                        continue
                    
                    if res_chain=='A':
                        res_chain='E'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['E']
                    elif res_chain=='B':
                        res_chain='F'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['F']
                    elif res_chain=='C':
                        res_chain='G'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['G']
                    elif res_chain=='D':
                        res_chain='H'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['H']
                    else:
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh[res_chain]
                    
                    
 

                
                if res_name=='POP':
                    if atom_name[0] !='C': continue
                    res_name='LIP'
                    if 0 < int(atom_name[1:]) < 21: continue  ## delete the head of pop
                    if int(atom_name[1:]) > 99 and int(atom_name[1:]) < 300 :
                        #print(atom_name)
                        atom_name = atom_name[0]+'4'+atom_name[3:] 
                        #print(atom_name)
                    if int(atom_name[1:]) > 299 and int(atom_name[1:]) < 400 :
                        #print(atom_name)
                        atom_name = atom_name[0]+'5'+atom_name[3:]

                    #avoid overlap resid
                    if res_chain=='A':
                        res_chain='E'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['E']
                    elif res_chain=='B':
                        res_chain='F'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['F']
                    elif res_chain=='C':
                        res_chain='G'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['G']
                    elif res_chain=='D':
                        res_chain='H'
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh['H']
                    else:
                        if current_res_number != old_res_number or current_res_chain != old_res_chain:
                            #print("move")
                            chain_id_list_hoh[res_chain]=chain_id_list_hoh[res_chain]+1
                        res_number=chain_id_list_hoh[res_chain]
                    

#######################modify resid to fit with crystal structure sequence
                if res_chain=='A':
                    res_number=res_number+6
                elif res_chain=='B':
                    res_number=res_number+2
                elif res_chain=='C':
                    res_number=res_number+3
                old_res_chain=current_res_chain
                old_res_number=current_res_number
########################输出, output
                outputstr='ATOM  {0:5} {1}{2:3}{3:>4}{4:>2}{5:4}    {6:8.3f}{7:8.3f}{8:8.3f}\n'.format(atom_number,flag,atom_name,res_name,res_chain,res_number,x_coordinate,y_coordinate,z_coordinate)
                out_file.write(outputstr)

def crd2pdb(input_file,output_file):
########################定义,defination
    chain_id_list=['A','B','C','D']
    chain_id_list_hoh={'E':0,'F':0,'G':0,'H':0,'I':0, 'J':0,'K':0,'L':0,'M':0,'N':0,'O':0,'P':0,'Q':0,'R':0,'S':0,'T':0,'U':0,'V':0,'W':0,'X':0,'Y':0,'Z':0}
    last_res_number=1
    chain_id_index=0
    cutoff=8000
    flag_A=0
    flag_B=0
########################Read gromac files
    with open(output_file,mode='w',encoding='utf-8') as out_file:
        with open(input_file,mode='r',encoding='utf-8') as in_file:
##################delete first, second and last two lines
            all_line = in_file.readlines()[4:-1]
            for a_line in all_line:  
##################delete 'CONECT' and 'TER' lines
                if a_line[0:6]=='CONECT' or a_line[0:3]=='TER' or a_line[0:6]=='ENDMDL' or a_line[0:5]=='MODEL':
                    continue
             
##################Read strings
                res_chain_type_ini=a_line[102:105] 
                res_chain_ini=a_line[105:112]
                res_number_ini=a_line[112:128]
                res_name_ini=a_line[22:32]
                atom_name_ini=a_line[32:46]
                atom_number_ini=a_line[4:10]
                x_coordinate_ini=a_line[46:60]
                y_coordinate_ini=a_line[66:80]
                z_coordinate_ini=a_line[86:100]
#################transfer data           
                res_number=int(res_number_ini)
                res_chain_type=delete_space(res_chain_type_ini)
                res_name=delete_space(res_name_ini)
                res_chain=delete_space(res_chain_ini)
                atom_number=int(atom_number_ini)
                atom_name=delete_space(atom_name_ini)
                x_coordinate=float(x_coordinate_ini)
                y_coordinate=float(y_coordinate_ini)
                z_coordinate=float(z_coordinate_ini)
                flag=' '            
########################去掉氢 delete H atom/OT
                if atom_name=='OT1' or atom_name=='OT2' or atom_name[0]=='H':
                    continue
                 #for btype membrane
                if res_name=='DOPC':
                    if atom_name[0] !='C': continue
                    res_chain='M'
                    res_name='LIP'
                    if int(atom_name[1:]) > 99 and int(atom_name[1:]) < 300 :
                        #print(atom_name)
                        atom_name = atom_name[0]+'4'+atom_name[3:] 
                        #print(atom_name)
                    if int(atom_name[1:]) > 299 and int(atom_name[1:]) < 400 :
                        #print(atom_name)
                        atom_name = atom_name[0]+'5'+atom_name[3:] 
                #delete D12 and SOD
                if res_name=='D12' or res_name=='SOD' or res_name=='CLA':
                    continue
########################cofactor重命名及简单处理 rename and simple dealt with cofactor  
# """   
#                 if atom_name[-1]=='0':
#                         atom_name=atom_name[0:-1]
#                         flag='b'
#                     elif atom_name[-1]=='1':
#                         atom_name=atom_name[0:-1]
#                         flag='c'
#                     elif atom_name[-1]=='4':
#                         atom_name=atom_name[0:-1]
#                         flag='a' 
#                     if atom_name=='OH2':
#                         atom_name='O'
#                 elif res_name=='CU2':
#                     res_name='CUA'
#                     atom_name='CU' 
                
# """      

######################## edit chain id and residue number for hoh
                if res_name=='TIP3':
                    res_name='HOH'
                    if res_number <= 9999: 
                        res_chain ='E'
                        res_number = res_number
                    elif res_number <=19998:
                        res_chain = 'F'
                        res_number = res_number - 9999
                    elif res_number <= 29998:
                        res_chain = 'G'
                        res_number = res_number - 19998
                if res_name=='HSD':
                    res_name=='HIS'
#check
#                if res_name=='POT' or res_name=='CLA' or res_name=='POPC' or res_name=='POP' or res_name=='DOPC':
#                    continue

#######################modify resid to fit with crystal structure sequence
#                if res_chain=='A':
#                    res_number=res_number+6
#                elif res_chain=='B':
#                    res_number=res_number+2
#                elif res_chain=='C':
#                    res_number=res_number+3
########################输出, output
                outputstr='ATOM  {0:5} {1}{2:3}{3:>4}{4:>2}{5:4}    {6:8.3f}{7:8.3f}{8:8.3f}\n'.format(atom_number,flag,atom_name,res_name,res_chain,res_number,x_coordinate,y_coordinate,z_coordinate)
                out_file.write(outputstr)


                

inputpathway=r'/Users/caixiuhong/Dropbox_CityCollege/cai/btype_cco/snapshot/clustering_PLS-20-01-14/SnapshotsFromTrajs'
outputpathway=r'/Users/caixiuhong/Dropbox_CityCollege/cai/btype_cco/snapshot/clustering_PLS-20-01-14/SnapshotsForMCCE/no_water_lip'

for root,dirs,files in os.walk(inputpathway):
    for subdir in dirs:
        subdirpath=os.path.join(root,subdir)
        outputsubdir=re.sub(inputpathway,outputpathway,subdirpath)
        if not os.path.exists(outputsubdir):
            os.mkdir(outputsubdir)
    for name in files:
        #print(name)
        if name[-4:] !='.pdb' and name[-4:] != '.gro': continue
        inputfilepath=os.path.join(root,name)
        outputfilepath=re.sub(inputpathway,outputpathway,inputfilepath)
#       outputfilepath=re.sub('gro$','pdb',outputfilepath_1)
        print("creating %s." % (str(outputfilepath)))
        mm2pdb(inputfilepath,outputfilepath, 1)