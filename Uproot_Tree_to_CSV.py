import os, sys
import numpy as np
import uproot
import uproot_methods
import pandas as pd



def Tree_to_CSV(file_full_path, tree_name):

    root_file = uproot.open(file_full_path)
    tree      = root_file[tree_name].arrays(root_file[tree_name].keys(), library='np') ##useful as np.array

    df = pd.DataFrame.from_dict(tree, orient='columns', dtype=None, columns=None)
    df.to_csv(tree_name+".csv", index=True)



#####Implementation example####

def main():
    
    inFile   = sys.argv[1]
    treeName = sys.argv[2]
    #Tree_to_CSV("/Volumes/Study/Weizmann_PostDoc/AllPix2Study/AllPixProceessedOutput/Signal_e0ppw_3.0/dataFile_Signal_e0ppw_3.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave00_Event1.root", "pixels")
    Tree_to_CSV(inFile, treeName)



if __name__=="__main__":
    main()
