import pydicom # Changing import statement from dicom to pydicom
from pydicom.errors import InvalidDicomError

import numpy as np
from PIL import Image, ImageDraw
import os
from glob import glob
import argparse
import pickle
import parsing

############# Argument Parser ###################
parser = argparse.ArgumentParser(description='Take user input Files names')
parser.add_argument('-b', '--BASE_PATH', type = str ,default = "./",help = 'Base Path where the dicom and contour folders are placed')
parser.add_argument('-d', '--DICOM_FOLDER', type = str ,default = "dicoms",help = 'Name of dicom folder')
parser.add_argument('-c', '--CONTOUR_FOLDER', type = str ,default = "contourfiles",help = 'Name of contour folder')
parser.add_argument('-l', '--LINK', type = str ,default = "Link.csv",help = 'File containing Patient_id and original_id')
parser.add_argument('-o', '--OUTPUT_FOLDER', type = str ,default = "output",help = 'Output folder containing result of data preprocessing')
args = parser.parse_args()

BASE_PATH = args.BASE_PATH
DICOM_BASE_PATH = os.path.join(BASE_PATH ,args.DICOM_FOLDER)
CONTOUR_BASE_PATH = os.path.join(BASE_PATH ,args.CONTOUR_FOLDER)
LINK_FILE = os.path.join(BASE_PATH,args.LINK)
OUTPUT_FOLDER = os.path.join(BASE_PATH,args.OUTPUT_FOLDER)
if os.path.exists(OUTPUT_FOLDER):
    pass
else:
    os.mkdir(OUTPUT_FOLDER)
print(BASE_PATH,
      DICOM_BASE_PATH,
      CONTOUR_BASE_PATH,
      LINK_FILE,
      OUTPUT_FOLDER )

##################################################

class FileParse(object):
    """FileParse class to parse dicom and contour files from given paths. It wraps existing functions and builds method on top of it.
    
       param parse_contour_file : func for parsing contour file, default : parse_contour_file
       param parse_dicom_file : func for parsing dicom file , default : parse_dicom_file 
       param poly_to_mask : func for creating mask from polygon, default : poly_to_mask
       param BASE_PATH,DICOM_BASE_PATH,CONTOUR_BASE_PATH,LINK_FILE : Paths for folder and files, refer argparse
       param link_file_header: Flag for header if its present in LINK_FILE
    
    """
    def __init__(self,parse_contour_file = parsing.parse_contour_file ,
                  parse_dicom_file =parsing.parse_dicom_file ,
                  poly_to_mask= parsing.poly_to_mask,
                  BASE_PATH = BASE_PATH,
                  DICOM_BASE_PATH = DICOM_BASE_PATH,
                  CONTOUR_BASE_PATH = CONTOUR_BASE_PATH,
                  LINK_FILE = LINK_FILE,
                  OUTPUT_FOLDER = OUTPUT_FOLDER,
                  link_file_header = True):
        
        self.parse_contour_file = parse_contour_file
        self.parse_dicom_file = parse_dicom_file
        self.poly_to_mask = poly_to_mask
        self.BASE_PATH = BASE_PATH
        self.DICOM_BASE_PATH = DICOM_BASE_PATH
        self.CONTOUR_BASE_PATH  = CONTOUR_BASE_PATH 
        self.LINK_FILE  = LINK_FILE 
        self.OUTPUT_FOLDER = OUTPUT_FOLDER
        self._link_file_header = link_file_header
        
    def _link_patient_file(self):
        """
        param filename: Name of csv file assuming two columns containing patient_id and original_id.
        param header: If first item is header/column name ( default True) or not.
        :return: list containing tuples of patient_id and corresponding original_id
        """
        self.patient_id = []
        self.original_id = []
        with open(self.LINK_FILE, 'r') as infile:
            for line in infile:
                if self._link_file_header:
                    self._link_file_header = False
                else:
                    rec = line.strip().split(",")
                    self.patient_id.append(rec[0])
                    self.original_id.append( rec[1])

        return zip(self.patient_id,self.original_id)
    
    def link_dicom_contour(self):
        
        """Method to link contour and dicom file.
           param return: list containing tuples of dicom image array and contour image array
        """
        self.patient_file_link = self._link_patient_file()
        self._link_file_header = True
        self.patient_dict = {}
        self.dic_cont_arr = []
        self.unknown_idx = []
        for link in self.patient_file_link:
            dicom_file_path = glob(os.path.join(self.DICOM_BASE_PATH,link[0])+"/*.dcm")
            icountour_file_path = glob(os.path.join(self.CONTOUR_BASE_PATH,link[1])+"/i-contours"+"/*.txt")
            #ocountour_file_path = glob(os.path.join(CONTOUR_BASE_PATH,link[1])+"/o-contours"+"/*.txt")
            assert dicom_file_path !=[]
            assert icountour_file_path !=[]
            try:
                dicom_id_dict = dict(list(map(lambda x: (int(x.split("/")[-1].strip(".dcm")),x),dicom_file_path)))
                contour_id_dict = dict(list(map(lambda x: (int(x.split("/")[-1].split("-icontour-manual")[0].split("-")[-1]),x),icountour_file_path)))
            except:
                print("Please check the file format")
            dic_cont = [] 
            for idx in contour_id_dict.keys():
                try:
                    dic_cont.append((dicom_id_dict[idx],contour_id_dict[idx]))
                    dicom_arr = self.parse_dicom_file(dicom_id_dict[idx])
                    contour_arr =  self.poly_to_mask(self.parse_contour_file(contour_id_dict[idx]),256,256)
                    self.dic_cont_arr.append((dicom_arr,contour_arr ))
                except:
                    self.unknown_idx.append((idx,contour_id_dict[idx]))

            self.patient_dict[link[0]] = dic_cont
        print("{} contour files unlinked".format(len(self.unknown_idx)) )


    
    def save_pkl(self):
        with open(os.path.join(self.OUTPUT_FOLDER,"dic_cont_arr.pkl"), 'wb') as handle:
            pickle.dump(self.dic_cont_arr, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
            
            
            
###############################################

Parsed_object = FileParse()
Parsed_object.link_dicom_contour()
Parsed_object.save_pkl()
        
        

        
        
        
    
    

