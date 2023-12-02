import numpy as np
import sys
import shutil


def extract_coord(word_list):#ang.
    current_coord, elem_list = [], []

    for word in word_list:
        elem_list.append(word[0])
        current_coord.append(list(map(float,word[1:4])))

    return current_coord, elem_list


def extract_energy(word):#hartree
    energy = float(word.split()[2])
    return energy
    
def extract_grad(word_list, elem_list):#hartree/bohr
    gradient_list = []
    for num, word in enumerate([word_list[i:i+3] for i in range(0, len(word_list), 3)]):
        gradient = []
        gradient.extend(list(map(float,word)))
        gradient_list.append(gradient)
    return gradient_list
    
def extract_dipole(word):#au
    dipole_vector = word.split()[2:5]

    return dipole_vector
    
def extract_hess(word_list, elem_list):#hartree/bohr^2
    hessian_matrix = np.zeros((len(elem_list)*3,len(elem_list)*3), dtype="float64").tolist()
    elem_xyz_num = len(elem_list)*3
    row_count = -5
    count = -5
    #----------------
    #form |a    |
    #     |b d  |
    #     |c e f|
    #---------------
    for word in word_list:
        
        if len(word) == 1:
            row_count += 5
            count += 5
            column_count = count

        for j in range(len(word)):
            hessian_matrix[column_count][j+row_count] = float(word[j])
        
        column_count += 1
    #----------------
    #form |a b c|
    #     |b d e|
    #     |c e f|
    #---------------
    for i, row in enumerate(hessian_matrix):#i=column, j=row
        for j in range(len(row)):
            if i != j:
                hessian_matrix[i][j] = hessian_matrix[j][i]


    return hessian_matrix#list
    
def extract_dipole_derivatives(word_list):#probably au
    dipole_derivative_tensor_matrix = []
   

    for num, word in enumerate([word_list[i:i+3] for i in range(0, len(word_list), 3)]):
        
        dipole_derivative_tensor_matrix.append(word)
        

    return dipole_derivative_tensor_matrix



def extract_polarizability(word_list):#au
    #----------------
    #form |a    |
    #     |b d  |
    #     |c e f|
    #---------------
    for i in range(len(word_list)):
        word_list[i] = list(map(float,word_list[i]))
        
    
    pola_tensor_matrix = word_list
    for i, row in enumerate(pola_tensor_matrix):
        if len(row) < 3:
            pola_tensor_matrix[i] += [0]*(3-len(row))
    #----------------
    #form |a b c|
    #     |b d e|
    #     |c e f|
    #---------------     

    for i, row in enumerate(pola_tensor_matrix):#i=column, j=row
        for j in range(len(row)):
            if i != j:
                pola_tensor_matrix[i][j] = float(pola_tensor_matrix[j][i])
    

    return pola_tensor_matrix


def LinkJOB2list(file):
    with open(file,"r") as f:#xxx_LinkJOB.rrm
        words = f.readlines()
    #---------------------------
    INFO_flag = True
    COORD_flag = False
    GRAD_flag = False
    HESS_flag = False
    DIDE_flag = False
    POLA_flag = False
    #---------------------------
    word_list = []
    info_list = []
    for word in words:
        if "COORDINATE" in word:
            INFO_flag = False
        #-----------------------------
        if INFO_flag:
            info_list.append(word)
            
        if "ENERGY" in word:
            energy = extract_energy(word)

            COORD_flag = False
            current_coord, elem_list = extract_coord(word_list)
 
            word_list = []
            
            
        if "DIPOLE" in word and not "DERIVATIVES" in word:
            dipole_vector = extract_dipole(word)

            GRAD_flag = False
            gradient_list = extract_grad(word_list, elem_list)

            word_list = [] 
            
        #-----------------------------
        
        if "DIPOLE DERIVATIVES" in word and HESS_flag:
            HESS_flag = False
            hessian_matrix = extract_hess(word_list, elem_list)
            word_list = []
            
        if "POLARIZABILITY" in word and DIDE_flag:
            DIDE_flag = False
            dipole_derivative_tensor_matrix = extract_dipole_derivatives(word_list)
            
            word_list = []
        
        if "S**2   =" in word:
            spin_multiplicity = word.split()[2]
    
        #----------------------------
        if COORD_flag:
            word_list.append(word.split())
        if GRAD_flag:
            word_list.append(word)
        if HESS_flag:
            word_list.append(word.split())
        if DIDE_flag:
            word_list.append(word.split())
        if POLA_flag:
            word_list.append(word.split())
            
        #----------------------------
        
        if "CURRENT COORDINATE" in word:
            COORD_flag = True         
        if "GRADIENT" in word:
            
            GRAD_flag = True    
        if "HESSIAN" in word:
            HESS_flag = True
        if "DIPOLE DERIVATIVES" in word:
            DIDE_flag = True
        if "POLARIZABILITY" in word:
            POLA_flag = True
        #----------------------------
    pola_tensor_matrix = extract_polarizability(word_list)
    
    #--------------------------    
    
    linkjob_dist = {}
    
    try:
        if current_coord:
            pass
    except:
        current_coord = "None"
    try:
        if dipole_vector:
            pass
    except:    
        dipole_vector = "None"
    try:
        if gradient_list:
            pass
    except:
        gradient_list = "None"
    try:
        if hessian_matrix:
            pass
    except:
        hessian_matrix = "None"
    try:
        if dipole_derivative_tensor_matrix:
            pass
    except:
        dipole_derivative_tensor_matrix = "None"
    
    try:
        if pola_tensor_matrix:
            pass
    except:
        pola_tensor_matrix = "None"
        
    linkjob_dist["information"] = info_list#str, list
    linkjob_dist["energy"] = float(energy)
    linkjob_dist["element_list"] = elem_list#str, list
    linkjob_dist["current_coord"] = np.array(current_coord, dtype="float64")
    linkjob_dist["dipole_vector"] = np.array(dipole_vector, dtype="float64")
    linkjob_dist["gradient_list"] = np.array(gradient_list, dtype="float64")
    linkjob_dist["hessian_matrix"] = np.array(hessian_matrix, dtype="float64")
    linkjob_dist["dipole_derivative_tensor_matrix"] = np.array(dipole_derivative_tensor_matrix, dtype="float64")
    linkjob_dist["pola_tensor_matrix"] = np.array(pola_tensor_matrix, dtype="float64")
    linkjob_dist["spin_multiplicity"] = float(spin_multiplicity)
    

    shutil.copy(file, file+"_old")

        
    return linkjob_dist


def list2LinkJOB(file, linkjob_dist):
    
    with open(file+"_new", "w") as f:
        for word in linkjob_dist["information"]:
            f.write(word)
        f.write("COORDINATE\n")
        for i in range(len(linkjob_dist["element_list"])):

            
            f.write("{:2}".format(linkjob_dist["element_list"][i])+"    {0:>17.12f}    {1:>17.12f}    {2:>17.12f}".format(*linkjob_dist["current_coord"][i].tolist())+"\n")
        
        f.write("\n")
        f.write("RESULTS\n")
        f.write("CURRENT COORDINATE\n")
        for i in range(len(linkjob_dist["element_list"])):

            
            f.write("{:2}".format(linkjob_dist["element_list"][i])+"    {0:>17.12f}    {1:>17.12f}    {2:>17.12f}".format(*linkjob_dist["current_coord"][i].tolist())+"\n")
    
        f.write("ENERGY = {:>17.12f}".format(linkjob_dist["energy"])+"   0.000000000000    0.000000000000\n")
        f.write("       =    0.000000000000    0.000000000000    0.000000000000\n")
        f.write("S**2   =    {:>17.12f}".format(linkjob_dist["spin_multiplicity"])+"\n")
        f.write("GRADIENT\n")
        for word in linkjob_dist["gradient_list"]:
            for w in word:
                f.write(" {:>17.12f}".format(w)+"\n")
        
        f.write("DIPOLE =    {0:>17.12f}    {1:>17.12f}    {2:>17.12f}".format(*linkjob_dist["dipole_vector"].tolist())+"\n")
        
        f.write("HESSIAN\n")
        
        max_column_count = len(linkjob_dist["hessian_matrix"])
        column_count = 0
        row_count = 0
        while max_column_count > column_count:
            
            for i in range(column_count, max_column_count):
                if i == column_count+0:
                    f.write("  {0:>14.9f}  ".format(linkjob_dist["hessian_matrix"].tolist()[i][row_count])+"\n")
                elif i == column_count+1:
                    f.write("  {0:>14.9f}  {1:>14.9f}  ".format(*linkjob_dist["hessian_matrix"].tolist()[i][row_count:row_count+2])+"\n")
                
                elif i == column_count+2:
                    f.write("  {0:>14.9f}  {1:>14.9f}  {2:>14.9f}  ".format(*linkjob_dist["hessian_matrix"].tolist()[i][row_count:row_count+3])+"\n")
                elif i == column_count+3:
                    f.write("  {0:>14.9f}  {1:>14.9f}  {2:>14.9f}  {3:>14.9f}  ".format(*linkjob_dist["hessian_matrix"].tolist()[i][row_count:row_count+4])+"\n")
                elif i >= column_count+4:
                    f.write("  {0:>14.9f}  {1:>14.9f}  {2:>14.9f}  {3:>14.9f}  {4:>14.9f}  ".format(*linkjob_dist["hessian_matrix"].tolist()[i][row_count:row_count+5])+"\n")
            column_count += 5
            row_count += 5
        
        f.write("DIPOLE DERIVATIVES\n")
        for word in linkjob_dist["dipole_derivative_tensor_matrix"]:
            
            for w in word:
               
                f.write("  {0:>17.12f}    {1:>17.12f}    {2:>17.12f}".format(*w.tolist())+"\n")
        
        f.write("POLARIZABILITY\n")
        for num, word in enumerate(linkjob_dist["pola_tensor_matrix"]):
            if num == 0:
                f.write("  {0:>17.12f}   ".format(word.tolist()[0])+"\n")
            elif num == 1:
                f.write("  {0:>17.12f}    {1:>17.12f}  ".format(*word.tolist()[:2])+"\n")
                       
            elif num == 2:
                f.write("  {0:>17.12f}    {1:>17.12f}    {2:>17.12f}".format(*word.tolist())+"\n")
            else:
                raise "error"
        
    
    shutil.copy(file+"_new", file)
    return

if __name__ == "__main__":
    linkjob_dist = LinkJOB2list(sys.argv[1])
    print("gradient_list")
    print(linkjob_dist["gradient_list"])
    #print("hessian_matrix")
    #print(linkjob_dist["hessian_matrix"])
    print("current_coord")
    print(linkjob_dist["current_coord"])
    print("energy")
    print(linkjob_dist["energy"])
    print("pola_tensor_matrix")
    print(linkjob_dist["pola_tensor_matrix"])
    #print("dipole_derivative_tensor_matrix")
    #print(linkjob_dist["dipole_derivative_tensor_matrix"])
    print("dipole_vector")
    print(linkjob_dist["dipole_vector"])
    print("information")
    print(linkjob_dist["information"])
    print("spin_multiplicity")
    print(linkjob_dist["spin_multiplicity"])
    #list2LinkJOB(sys.argv[1], linkjob_dist)
    