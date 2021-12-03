#!/usr/bin/env python


import sys
import os, argparse

#Umesh

"""
CONVERT_OLD_NEW has old mcce hydrogen name format(PDB v2) as KEY 
and stable  mcce hydrogen name format (PDB v3) as value.

If you have extra residues and ligands then you need to add name in the dictionary.
Key as pdb V2 and Value pdb V3
"""

CONVERT_OLD_NEW = {"1H   HOH": " H1  HOH",
                   "2H   HOH": " H2  HOH",
                   "1H   NTR": " H   NTR",
                   "2H   NTR": " H2  NTR",
                   "3H   NTR": " H3  NTR",
                   "1HG1 VAL": "HG11 VAL",
                   "2HG1 VAL": "HG12 VAL",
                   "3HG1 VAL": "HG13 VAL",
                   "1HG2 VAL": "HG21 VAL",
                   "2HG2 VAL": "HG22 VAL",
                   "3HG2 VAL": "HG23 VAL",
                   "1HA  GLY": " HA2 GLY",
                   "2HA  GLY": " HA3 GLY",
                   "1HB  ALA": " HB1 ALA",
                   "2HB  ALA": " HB2 ALA",
                   "3HB  ALA": " HB3 ALA",
                   "1HB  LEU": " HB2 LEU",
                   "2HB  LEU": " HB3 LEU",
                   "1HD1 LEU": "HD11 LEU",
                   "2HD1 LEU": "HD12 LEU",
                   "3HD1 LEU": "HD13 LEU",
                   "1HD2 LEU": "HD21 LEU",
                   "2HD2 LEU": "HD22 LEU",
                   "3HD2 LEU": "HD23 LEU",
                   "1HB  TRP": " HB2 TRP",
                   "2HB  TRP": " HB3 TRP",
                   "1HB  ARG": " HB2 ARG",
                   "2HB  ARG": " HB3 ARG",
                   "1HG  ARG": " HG2 ARG",
                   "2HG  ARG": " HG3 ARG",
                   "1HD  ARG": " HD2 ARG",
                   "2HD  ARG": " HD3 ARG",
                   "1HH1 ARG": "HH11 ARG",
                   "2HH1 ARG": "HH12 ARG",
                   "1HH2 ARG": "HH21 ARG",
                   "2HH2 ARG": "HH22 ARG",
                   "1HB  LYS": " HB2 LYS",
                   "2HB  LYS": " HB3 LYS",
                   "1HG  LYS": " HG2 LYS",
                   "2HG  LYS": " HG3 LYS",
                   "1HD  LYS": " HD2 LYS",
                   "2HD  LYS": " HD3 LYS",
                   "1HE  LYS": " HE2 LYS",
                   "2HE  LYS": " HE3 LYS",
                   "1HZ  LYS": " HZ1 LYS",
                   "2HZ  LYS": " HZ2 LYS",
                   "3HZ  LYS": " HZ3 LYS",
                   "1HB  ASN": " HB2 ASN",
                   "2HB  ASN": " HB3 ASN",
                   "1HD2 ASN": "HD21 ASN",
                   "2HD2 ASN": "HD22 ASN",
                   "1HB  GLN": " HB2 GLN",
                   "2HB  GLN": " HB3 GLN",
                   "1HG  GLN": " HG2 GLN",
                   "2HG  GLN": " HG3 GLN",
                   "1HE2 GLN": "HE21 GLN",
                   "2HE2 GLN": "HE22 GLN",
                   "1HG1 ILE": "HG12 ILE",
                   "2HG1 ILE": "HG13 ILE",
                   "1HG2 ILE": "HG21 ILE",
                   "2HG2 ILE": "HG22 ILE",
                   "3HG2 ILE": "HG23 ILE",
                   "1HD1 ILE": "HD11 ILE",
                   "2HD1 ILE": "HD12 ILE",
                   "3HD1 ILE": "HD13 ILE",
                   "1HG1 ILE": "HG12 ILE",
                   "1HB  PRO": " HB2 PRO",
                   "2HB  PRO": " HB3 PRO",
                   "1HG  PRO": " HG2 PRO",
                   "2HG  PRO": " HG3 PRO",
                   "1HD  PRO": " HD2 PRO",
                   "2HD  PRO": " HD3 PRO",
                   "1HB  PHE": " HB2 PHE",
                   "2HB  PHE": " HB3 PHE",
                   "1HB  HIS": " HB2 HIS",
                   "2HB  HIS": " HB3 HIS",
                   "1HB  SER": " HB2 SER",
                   "2HB  SER": " HB3 SER",
                   "1HG2 THR": "HG21 THR",
                   "2HG2 THR": "HG22 THR",
                   "3HG2 THR": "HG23 THR",
                   "1HB  CYS": " HB2 CYS",
                   "2HB  CYS": " HB3 CYS",
                   "1HB  MET": " HB2 MET",
                   "2HB  MET": " HB3 MET",
                   "1HG  MET": " HG2 MET",
                   "2HG  MET": " HG3 MET",
                   "1HE  MET": " HE1 MET",
                   "2HE  MET": " HE2 MET",
                   "3HE  MET": " HE3 MET",
                   "1HB  ASP": " HB2 ASP",
                   "2HB  ASP": " HB3 ASP",
                   "1HB  GLU": " HB2 GLU",
                   "2HB  GLU": " HB3 GLU",
                   "1HG  GLU": " HG2 GLU",
                   "2HG  GLU": " HG3 GLU",
                   "1HB  TYR": " HB2 TYR",
                   "2HB  TYR": " HB3 TYR",
                   "1HB ATYR": " HB2 TYR",
                   "2HB ATYR": " HB3 TYR",
                   "1HB BTYR": " HB2 TYR",
                   "2HB BTYR": " HB3 TYR",
                   "1HB AARG": " HB2AARG",
                   "2HB AARG": " HB3 ARG",
                   "1HG AARG": " HG2 ARG",
                   "2HG AARG": " HG3 ARG",
                   "1HD AARG": " HD2 ARG",
                   "2HD AARG": " HD3 ARG",
                   "1HH1AARG": "HH11 ARG",
                   "2HH1AARG": "HH12 ARG",
                   "1HH2AARG": "HH21 ARG",
                   "2HH2AARG": "HH22 ARG",
                   "1HB BARG": " HB2AARG",
                   "2HB BARG": " HB3 ARG",
                   "1HG BARG": " HG2 ARG",
                   "2HG BARG": " HG3 ARG",
                   "1HD BARG": " HD2 ARG",
                   "2HD BARG": " HD3 ARG",
                   "1HH1BARG": "HH11 ARG",
                   "2HH1BARG": "HH12 ARG",
                   "1HH2BARG": "HH21 ARG",
                   "2HH2BARG": "HH22 ARG",
                   "1HG1AVAL": "HG11 VAL",
                   "2HG1AVAL": "HG12 VAL",
                   "3HG1AVAL": "HG13 VAL",
                   "1HG2AVAL": "HG21 VAL",
                   "2HG2AVAL": "HG22 VAL",
                   "3HG2AVAL": "HG23 VAL",
                   "1HG1BVAL": "HG11 VAL",
                   "2HG1BVAL": "HG12 VAL",
                   "3HG1BVAL": "HG13 VAL",
                   "1HG2BVAL": "HG21 VAL",
                   "2HG2BVAL": "HG22 VAL",
                   "3HG2BVAL": "HG23 VAL",
                   "1HA AGLY": " HA2 GLY",
                   "2HA AGLY": " HA3 GLY",
                   "1HB AALA": " HB1 ALA",
                   "2HB AALA": " HB2 ALA",
                   "3HB AALA": " HB3 ALA",
                   "1HB ALEU": " HB2 LEU",
                   "2HB ALEU": " HB3 LEU",
                   "1HD1ALEU": "HD11 LEU",
                   "2HD1ALEU": "HD12 LEU",
                   "3HD1ALEU": "HD13 LEU",
                   "1HD2ALEU": "HD21 LEU",
                   "2HD2ALEU": "HD22 LEU",
                   "3HD2ALEU": "HD23 LEU",
                   "1HA BGLY": " HA2 GLY",
                   "2HA BGLY": " HA3 GLY",
                   "1HB BALA": " HB1 ALA",
                   "2HB BALA": " HB2 ALA",
                   "3HB BALA": " HB3 ALA",
                   "1HB BLEU": " HB2 LEU",
                   "2HB BLEU": " HB3 LEU",
                   "1HD1BLEU": "HD11 LEU",
                   "2HD1BLEU": "HD12 LEU",
                   "3HD1BLEU": "HD13 LEU",
                   "1HD2BLEU": "HD21 LEU",
                   "2HD2BLEU": "HD22 LEU",
                   "3HD2BLEU": "HD23 LEU",
                   "1HB ALYS": " HB2 LYS",
                   "2HB ALYS": " HB3 LYS",
                   "1HG ALYS": " HG2 LYS",
                   "2HG ALYS": " HG3 LYS",
                   "1HD ALYS": " HD2 LYS",
                   "2HD ALYS": " HD3 LYS",
                   "1HE ALYS": " HE2 LYS",
                   "2HE ALYS": " HE3 LYS",
                   "1HZ ALYS": " HZ1 LYS",
                   "2HZ ALYS": " HZ2 LYS",
                   "3HZ ALYS": " HZ3 LYS",
                   "1HB AASN": " HB2 ASN",
                   "2HB AASN": " HB3 ASN",
                   "1HD2AASN": "HD21 ASN",
                   "2HD2AASN": "HD22 ASN",
                   "1HB AGLN": " HB2 GLN",
                   "2HB AGLN": " HB3 GLN",
                   "1HG AGLN": " HG2 GLN",
                   "2HG AGLN": " HG3 GLN",
                   "1HE2AGLN": "HE21 GLN",
                   "2HE2AGLN": "HE22 GLN",
                   "1HG1AILE": "HG12 ILE",
                   "2HG1AILE": "HG13 ILE",
                   "1HG2AILE": "HG21 ILE",
                   "2HG2AILE": "HG22 ILE",
                   "3HG2AILE": "HG23 ILE",
                   "1HD1AILE": "HD11 ILE",
                   "2HD1AILE": "HD12 ILE",
                   "3HD1AILE": "HD13 ILE",
                   "1HG1AILE": "HG12 ILE",
                   "1HB APRO": " HB2 PRO",
                   "2HB APRO": " HB3 PRO",
                   "1HG APRO": " HG2 PRO",
                   "2HG APRO": " HG3 PRO",
                   "1HD APRO": " HD2 PRO",
                   "2HD APRO": " HD3 PRO",
                   "1HB APHE": " HB2 PHE",
                   "2HB APHE": " HB3 PHE",
                   "1HB AHIS": " HB2 HIS",
                   "2HB AHIS": " HB3 HIS",
                   "1HB ASER": " HB2 SER",
                   "2HB ASER": " HB3 SER",
                   "1HG2ATHR": "HG21 THR",
                   "2HG2ATHR": "HG22 THR",
                   "3HG2ATHR": "HG23 THR",
                   "1HB ACYS": " HB2 CYS",
                   "2HB ACYS": " HB3 CYS",
                   "1HB AMET": " HB2 MET",
                   "2HB AMET": " HB3 MET",
                   "1HG AMET": " HG2 MET",
                   "2HG AMET": " HG3 MET",
                   "1HE AMET": " HE1 MET",
                   "2HE AMET": " HE2 MET",
                   "3HE AMET": " HE3 MET",
                   "1HB AASP": " HB2 ASP",
                   "2HB AASP": " HB3 ASP",
                   "1HB AGLU": " HB2 GLU",
                   "2HB AGLU": " HB3 GLU",
                   "1HG AGLU": " HG2 GLU",
                   "2HG AGLU": " HG3 GLU",
                   "1HB BLYS": " HB2 LYS",
                   "2HB BLYS": " HB3 LYS",
                   "1HG BLYS": " HG2 LYS",
                   "2HG BLYS": " HG3 LYS",
                   "1HD BLYS": " HD2 LYS",
                   "2HD BLYS": " HD3 LYS",
                   "1HE BLYS": " HE2 LYS",
                   "2HE BLYS": " HE3 LYS",
                   "1HZ BLYS": " HZ1 LYS",
                   "2HZ BLYS": " HZ2 LYS",
                   "3HZ BLYS": " HZ3 LYS",
                   "1HB BASN": " HB2 ASN",
                   "2HB BASN": " HB3 ASN",
                   "1HD2BASN": "HD21 ASN",
                   "2HD2BASN": "HD22 ASN",
                   "1HB BGLN": " HB2 GLN",
                   "2HB BGLN": " HB3 GLN",
                   "1HG BGLN": " HG2 GLN",
                   "2HG BGLN": " HG3 GLN",
                   "1HE2BGLN": "HE21 GLN",
                   "2HE2BGLN": "HE22 GLN",
                   "1HG1BILE": "HG12 ILE",
                   "2HG1BILE": "HG13 ILE",
                   "1HG2BILE": "HG21 ILE",
                   "2HG2BILE": "HG22 ILE",
                   "3HG2BILE": "HG23 ILE",
                   "1HD1BILE": "HD11 ILE",
                   "2HD1BILE": "HD12 ILE",
                   "3HD1BILE": "HD13 ILE",
                   "1HG1BILE": "HG12 ILE",
                   "1HB BPRO": " HB2 PRO",
                   "2HB BPRO": " HB3 PRO",
                   "1HG BPRO": " HG2 PRO",
                   "2HG BPRO": " HG3 PRO",
                   "1HD BPRO": " HD2 PRO",
                   "2HD BPRO": " HD3 PRO",
                   "1HB BPHE": " HB2 PHE",
                   "2HB BPHE": " HB3 PHE",
                   "1HB BHIS": " HB2 HIS",
                   "2HB BHIS": " HB3 HIS",
                   "1HB BSER": " HB2 SER",
                   "2HB BSER": " HB3 SER",
                   "1HG2BTHR": "HG21 THR",
                   "2HG2BTHR": "HG22 THR",
                   "3HG2BTHR": "HG23 THR",
                   "1HB BCYS": " HB2 CYS",
                   "2HB BCYS": " HB3 CYS",
                   "1HB BMET": " HB2 MET",
                   "2HB BMET": " HB3 MET",
                   "1HG BMET": " HG2 MET",
                   "2HG BMET": " HG3 MET",
                   "1HE BMET": " HE1 MET",
                   "2HE BMET": " HE2 MET",
                   "3HE BMET": " HE3 MET",
                   "1HB BASP": " HB2 ASP",
                   "2HB BASP": " HB3 ASP",
                   "1HB BGLU": " HB2 GLU",
                   "2HB BGLU": " HB3 GLU",
                   "1HG BGLU": " HG2 GLU",
                   "2HG BGLU": " HG3 GLU",
                   "1HB  CYD": " HB2 CYD",
                   "2HB  CYD": " HB3 CYD",
                   }


# CONVERT_NEW_OLD has  stable  mcce hydrogen name format (PDB v3) as KEY 
# and old mcce hydrogen name format(PDB v2) as value.

CONVERT_NEW_OLD= {}
for x, y  in CONVERT_NEW_OLD.items():
    CONVERT_NEW_OLD[y] = x


def readStep2(read_step2_file, convert_variable):
    lines = open(read_step2_file).readlines()
    for line in lines:
        if line[:6] == "ATOM  " or line[:6] == "HETATM":
            if line[12:20] in convert_variable:
                print(line[:12]+ convert_variable[line[12:20]]+ line[20:].rstrip())
            else:
                print(line, end="")
        else:
            print(line, end="")


if __name__ == "__main__":

    helpmsg = "Translate the mcce hydrogen name format in step2_out.pdb. \
                 Usuage: translate_step2.py -t old/new > output_file_name"
    parser = argparse.ArgumentParser(description=helpmsg)
    parser.add_argument("-t", help=" Give OLD to translate to  old  \
     (v2) and NEW to translate to new hydrogen format (v3).")
    args = parser.parse_args()

    # what format you want to change
    what_to_change = args.t
    if what_to_change:
        if what_to_change.lower() == 'old' or what_to_change.lower() == "new":
            if what_to_change.lower() == "old":
                convert_variable =  CONVERT_NEW_OLD
                readStep2("step2_out.pdb", convert_variable)
            else:
                convert_variable =  CONVERT_OLD_NEW
                readStep2("step2_out.pdb", convert_variable)

        else:
            print("Run code like this: translate_step2.py -t old/new > output_file_name")
    else:
        print("Run code like this: translate_step2.py -t old/new > output_file_name")
  

        



        
        


