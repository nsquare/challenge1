# Challenge 1

*Python version* : 3.5

Usage :
      python FileParser.py [-h] [-b BASE_PATH] [-d DICOM_FOLDER]
                           [-c CONTOUR_FOLDER] [-l LINK] [-o OUTPUT_FOLDER]

output :
       saves a pickle file in ./output folder. The pickle file contains list of tuples of (input,target)
Usage:
     batch_processor.py , class DataPreProc can be imported and API over (input, target) data can be used to generate shuffled batches of data.

## Part 1

* How did you verify that you are parsing the contours correctly?

This was done by :
a) Manually inspecting the images generated from array
b) created a method link_dicom_contour in FileParse class to match the id of contour file and respective dicom file

* What changes did you make to the code, if any, in order to integrate it into our production code base? 

a) Kept the template functions  same and wrapped it in FileParse class.
b) defined three more methods :
    link_patient_file : links patient_id and original_id from csv
    link_dicom_contour : Maps dicom image array to corresponding contour array
    save_pkl : Helper function to save the output from ink_dicom_contour

## Part 2

* Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

Saved the output of part 1 and this pickle will be used as input for part 2

* How do you/did you verify that the pipeline was working correctly?

Verified on ipython notebook, by picking the input for part2 from pickle file.

* Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

Improvements Required :

Multithreaded reading of input files.
More robust visual inspection , perhaps 3D




