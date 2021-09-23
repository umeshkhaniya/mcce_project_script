#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This will read a pdb file and classify the residue into different groups according the properties of residues
#residues properties considered are acid, base, grotthus polar and Non-grotthuss
import pandas as pd
import numpy as np
import sys


# In[2]:


inputpathway= '/Users/umeshkhaniya/Dropbox/python_script_research/pqrse.pdb'
outputpathway = '/Users/umeshkhaniya/Dropbox/python_script_research/file/'


# In[3]:


acid_list= ["ASP", "GLU"]
base_list= ["LYS","ARG"]
grpo_list=['SER', "THR", "TYR","HIS"] #grotthus polar aminoacid
non_grpo_list=["GLN", "ASN", "TRP"] #non-grotthus


# In[4]:


with open(inputpathway,mode='r',encoding='utf-8') as f1:
    print("processing %s." % (str(f1)))
    lines=[l.split() for l in f1.readlines()]
    #print(lines)
    res_list=[]
    acid_res=[]
    base_res=[]
    grpo_res=[]
    non_grpo_res=[]
    special_res=[]
    res_set=set()
    for l in lines:
        title=l[0]
        #print(title)
        ##test
        #print(l)
        #print(l)
        if (len(l) == 9 and len(l[3]) <= 3 and (title == "ATOM" or title=="HETATM")): #this is for to recognize the required pdb information
            res_full=l[3].rjust(3,'_')+l[4]+l[5].zfill(4)
            if (res_full in res_set):
                continue 
            else:
                res_dict={}
                res_dict['resname']=l[3]
                res_dict['reschain']=l[4]
                res_dict['resid']=l[5]
                res_dict['full_name']=res_full
                
                if ((l[3]) in acid_list or l[3] in base_list or l[3] in grpo_list or l[3] in non_grpo_list):
                    
                    
                        
                    if (l[3] in acid_list):
                        
                        res_dict['role']='acid'
                        acid_res.append(res_dict)
                            
                        
                    elif (l[3] in base_list):
                        res_dict['role']='base'
                        base_res.append(res_dict)
                    elif (l[3] in grpo_list):
                        res_dict['role']='grotthuss polar'
                        grpo_res.append(res_dict)
                    elif (l[3] in non_grpo_list):
                        res_dict['role']='Non grotthuss'
                        non_grpo_res.append(res_dict)
                else:
                    res_dict['role']='special'
                    special_res.append(res_dict)
                    
                    
                    
                      
                res_list.append(res_dict)
                res_set.add(res_full)
            
            
            
            
            
            
            

    


# In[5]:


with open(outputpathway+'acid.dat',mode='w',encoding='utf-8') as f2:
    for residue in acid_res:
        f2.write(residue['full_name'])
        f2.write('\n')

with open(outputpathway+'base.dat',mode='w',encoding='utf-8') as f3:
    for residue in base_res:
        f3.write(residue['full_name'])
        f3.write('\n')

with open(outputpathway+'grotthuss polar.dat',mode='w',encoding='utf-8') as f4:
    for residue in grpo_res:
        f4.write(residue['full_name'])
        f4.write('\n')

with open(outputpathway+'special_res.dat',mode='w',encoding='utf-8') as f5:
    for residue in special_res:
        f5.write(residue['full_name'])
        f5.write('\n')

with open(outputpathway+'nongrotthus.dat',mode='w',encoding='utf-8') as f6:
    for residue in non_grpo_res:
        f6.write(residue['full_name'])
        f6.write('\n')


    


# In[ ]:




