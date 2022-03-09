import os, sys
#from ROOT import *
import pprint
import argparse
import uproot
import pandas as pd


### check the x index distance and y index distance. 
def distance(lhs, rhs):
    if (lhs > rhs):
        return (lhs - rhs)
    else:
        return (rhs - lhs)

### if the x index distance and/or y index distance of two pixels are less than or equal to 1, then they are touching. 
def touching(pixels, cls):
    for cluster_pixel in cls:
        pxix = cluster_pixel[0]["cellx"]
        pxiy = cluster_pixel[0]["celly"]
        #### x index distance and y index distance must be less than or equal to 1 for touching pixels
        if(distance(pixels[0]["cellx"], pxix) <= 1 and distance(pixels[0]["celly"], pxiy) <= 1):
            return True;
    return False;

def main():
    
    ### get the input root file name from command line
    parser = argparse.ArgumentParser(description='Code to find seed tracks')
    parser.add_argument('-l', action="store", dest="inFileName", default="dataFile_Signal_e0ppw_3.0_EFieldV10p7p1pyN17Vpercm_Processed_Stave00_Event1.root")
    args = parser.parse_args()
    
    
    
    ### open an empty dictionary
    dict_cell = {}
    
    #############################
    ##### using pyroot ##########
    #############################
    ### load the tree from the root file
    #inFile      = TFile(args.inFileName, "READ")
    #pixels_tree = inFile.Get("pixels")
    
    ##### take all pixels from the pixels tree, for each bunch crossings
    #for event in pixels_tree:
        #bx = event.bx
        
        #dict_cell.setdefault(bx, []).append([{"cellx": event.cellx, "celly": event.celly, "pixId": event.pixId, "pixId": event.pixId, "isSignal": event.isSignal, "charge": event.charge, "tru_p": event.tru_p, "tru_edep": event.tru_edep, "tru_type": event.tru_type, "tru_pdgId": event.tru_pdgId, "tru_trackId": event.tru_trackId, "tru_hit": event.tru_hit, "tru_vertex": event.tru_vertex, "tru_cellx": event.tru_cellx, "tru_celly": event.tru_celly}])

    
    #############################
    ##### using uproot ##########
    #############################
    
    root_file     = uproot.open(args.inFileName)
    tree          = root_file["pixels"].arrays(root_file["pixels"].keys(), library='np') ##useful as np.array
    cellx_list    = tree["cellx"]
    celly_list    = tree["celly"]
    pixId_list    = tree["pixId"]
    isSignal_list = tree["isSignal"]
    
    
    ### for now we are interested only on event 1
    dict_cell[1] = []
    for i in range(len(cellx_list)):
        dict_cell[1].append([{"cellx":cellx_list[i], "celly":celly_list[i]}])
    
    
    pprint.pprint(dict_cell)
    
    
    ### loop over each bx
    for bx in dict_cell:
        ### list of clusters in one bx
        clusters = []
        
        ### dictionary to check if a pixel is already used in a previous cluster
        usedPixel = {}
        
        ### loop over pivot pixel in one bx
        for ipixels, pixels in enumerate(dict_cell[bx]):
            ### for a bx, pixel cellx and celly combination is unique
            pixKey = str(pixels[0]["cellx"])+"_"+str(pixels[0]["celly"])
            ### if the pixel is used in another cluster, ignore (otherwise there will be overcounting)
            if(pixKey in usedPixel and usedPixel[pixKey]):
                continue
            
            cluster = [pixels]
            usedPixel[pixKey] = True
            
            ### loop over all other pixels apart from the pivot pixel
            for other_pixels in dict_cell[bx][ipixels+1:]:
                #other_pixels = dict_cell[bx][ipixels+1+i]
                otherPixKey = str(other_pixels[0]["cellx"])+"_"+str(other_pixels[0]["celly"])
                if ((otherPixKey in usedPixel and usedPixel[otherPixKey]) or not (touching(other_pixels, cluster))):
                    continue
                ### add adjacent pixels to the cluster
                cluster.append(other_pixels)
                usedPixel[otherPixKey] = True
                
                
            ### add the list of cluster in one bx in a list
            clusters.append(cluster)
            
        
        print("for bx: ", bx, " number of clusters: ",len(clusters))
    
    
if __name__=="__main__":
    main()
