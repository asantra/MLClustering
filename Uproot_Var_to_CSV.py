import numpy as np
import uproot
import uproot_methods



def Var_to_CSV(file_full_path, tree_name, var_name):

    root_file = uproot.open(file_full_path)
    tree      = root_file[tree_name].arrays(root_file[tree_name].keys(), library='np') ##useful as np.array
    var_array = tree[var_name]
    np.savetxt(var_name+".csv", var_array, delimiter=",", header=var_name)



#####Implementation example####

Var_to_CSV("/home/rbrener/Analysis/Zprimebb/ML_stuff/GNN_Real_MC/Datasets/validation/Zpmumu_Sig_500_mc16d_validation.root", "nominal_MuMu_jb", "m_ll")

