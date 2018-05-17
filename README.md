# Challenge 1

*Python version* : 3.5

Usage :
      python FileParser.py [-h] [-b BASE_PATH] [-d DICOM_FOLDER]
                           [-c CONTOUR_FOLDER] [-l LINK] [-o OUTPUT_FOLDER]

output :
       saves a pickle file in ./output folder. The pickle file contains list of tuples of (input,target)
Usage:
     batch_processor.py , class DataPreProc can be imported and API over (input, target) data can be used to generate shuffled batches of data.

a) Manually inspecting the images generated from array
b) created a method link_dicom_contour in FileParse class to match the id of contour file and respective dicom file


a) Kept the template functions  same and wrapped it in FileParse class.
b) defined three more methods :
    link_patient_file : links patient_id and original_id from csv
    link_dicom_contour : Maps dicom image array to corresponding contour array
    save_pkl : Helper function to save the output from ink_dicom_contour


Improvements
* Multithreaded reading of input files.
* More robust visual inspection , perhaps 3D
* add script for testing 
* .dcm and .txt prefix and suffixes are hardcoded to extract file ids. Need to fix it.
* Adding more assert statements to check for type condition/ array empty or not etc.
* Add function to transform input and target arrays for data augmentation or other transformations.
* add logging info

