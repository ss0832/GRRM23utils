# GRRM23utils
For using utilities to easily implement user-developed tools (GRRM23)

URLs:

https://global.hpc.co.jp/products/grrm23/

https://afir.sci.hokudai.ac.jp/documents/manual/196


## Required modules
- numpy

## Utils
interface.py : For option (**AddSubExPot**) of GRRM23 

**AddSubExPot**=(absolute path of your program file to run between QM calculation and processing by GRRM program)

You can execute your program between processing of QM calculation software and processing of GRRM. 


### functions
**_interface.LinkJOB2list(file_name)_**

Read file_name (expect xxx_LinkJOB.rrm) and extract information of results of calculation (for adding user defined bias potential etc.)

This function saved xxx_LinkJOB.rrm file as xxx_LinkJOB.rrm_old.

file_name: str

expect xxx_LinkJOB.rrm

Returns: dist - results of calculation 

contents of dist

 - energy: electronic energy (float) 

 - element_list: element list of job file (iterable, str)  
 
 - current_coord:  coordination of atoms (3xN, ndarray, float64)  
 
 - dipole_vector: dipole vector(x y z(1x3), ndarray, float64) 
 
 - gradient_list: gradients of atoms (3xN, ndarray, float64)  
 
 - hessian_matrix: hessian matric of atoms (3Nx3N, ndarray, float64)
 
 - dipole_derivative_tensor_matrix: tensor matrix of first derivative dipole moment (Nx3x3, ndarray, float64)
 
 - pola_tensor_matrix: matrix of polarization (3x3, ndarray, float64)
 
 - spin_multiplicity: spin multiplicity (S**2) (float) 


**_interface.list2LinkJOB(file_name, linkjob_dist)_**

Save contents of linkjob_dist (valiable) to xxx_LinkJOB.rrm_new.

This function overwrites xxx_LinkJOB.rrm file as contents of xxx_LinkJOB.rrm_new.

file_name: str

  expect xxx_LinkJOB.rrm

linkjob_dist: dist

  expect linkjob_dist of output of interface.LinkJOB2list function

Returns: None

  

