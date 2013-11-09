import struct
            
def Fetch_Block(filename, lefthigh, righthigh, leftlow, rightlow):
    # get the axes in .hgt file
    lefthigh_n = 3601 - int(lefthigh[0]+1)
    lefthigh_w = int(lefthigh[1]+1)
    ##print ("LH: x %d, y %d\n" % (lefthigh_x, lefthigh_y))
    righthigh_n = 3601 - int(righthigh[0]+1)
    righthigh_w = int(righthigh[1]+1)
    ##print ("RH: x %d, y %d\n" % (righthigh_x, righthigh_y))
    leftlow_n = 3601 - int(leftlow[0]+1)
    leftlow_w = int(leftlow[1]+1)
    ##print ("LL: x %d, y %d\n" % (leftlow_x, leftlow_y))
    rightlow_n = 3601 - int(rightlow[0]+1)
    rightlow_w = int(rightlow[1]+1)
    ##print ("RL: x %d, y %d\n" % (rightlow_x, rightlow_y))
    
    # chunk size for each altitude
    chunk_size = righthigh_w - lefthigh_w + 1
    #print "chunk size : ", chunk_size
    # get number of rows of the block
    row_num =  leftlow_n - lefthigh_n + 1
    #print "row size : ", row_num
    
    # read and parse elevation data in the block
    hightest = 0;
    with open(filename, "rb") as f:
        for index in range(row_num):
            f.seek(((leftlow_n + index)*3601 + leftlow_w)*2)
            buf = f.read(chunk_size*2)
            step = 2
            buf_slice = [buf[i:i+step] for i in range(0, len(buf), step)]
            hgtline = []
            for sbuf in buf_slice:
                val = struct.unpack('>h', sbuf) 
                hgtline.append(val)
            hgt.append(hgtline)
    f.close
    
    with open("block.txt", "w") as fout:
        for item in hgt:
            for phgt in item:
                fout.write("%s " % phgt)
            fout.write("\n")
            
            
def Height_Block(filename, NW, NE, SW, SE):
    # get the axes in .hgt file
    NW_alt = 3601 - int(NW[0]+1)
    NW_long = 3601 - int(NW[1]+1)

    NE_alt = 3601 - int(NE[0]+1)
    NE_long = 3601 - int(NE[1]+1)

    SW_alt = 3601 - int(SW[0]+1)
    SW_long = 3601 - int(SW[1]+1)

    SE_alt = 3601 - int(SE[0]+1)
    SE_long = 3601 - int(SE[1]+1)
    ##print ("RL: x %d, y %d\n" % (rightlow_x, rightlow_y))
    
    # chunk size for each altitude
    chunk_size = NE_long - NW_long + 1
    #print "chunk size : ", chunk_size
    # get number of rows of the block
    row_num =  SW_alt - NW_alt + 1
    #print "row size : ", row_num
    
    # read and parse elevation data in the block
    hightest = 0;
    with open(filename, "rb") as f:
        for index in range(row_num):
            f.seek(((NW_alt + index)*3601 + NW_long)*2)
            buf = f.read(chunk_size*2)
            step = 2
            buf_slice = [buf[i:i+step] for i in range(0, len(buf), step)]
            for sbuf in buf_slice:
                val = struct.unpack('>h', sbuf) 
                if hightest < val[0]:
                    hightest = val[0]
    f.close
    return hightest
        
        
        
def Hash_Filename(Dir):
    import os
    import re
    text_files = [f for f in os.listdir(Dir) if f.endswith('.hgt')];
    ##print text_files
    Dic = {}
    for str in text_files:
        AL = re.split('\D+', str)
        Alt = int(AL[1])
        Lot = int(AL[2])
        t = Alt, Lot
        Dic[t] = str;
    return Dic
    
def Get_SRTMIndex(GridCord):
    import re
    SRTMIndex = [];
    for cord in GridCord:
        Index = []
        ind = 0
        for degree in cord:
            ind = ind + 1
            deg = re.split('\D+', degree)
            if(ind == 2):
                Index.append(int(deg[0])+1)
            else:
                Index.append(int(deg[0]))      
        SRTMIndex.append(Index)
    return SRTMIndex
    
def Get_SRTMGridIndex(GridCord):
    import re
    SRTMGridIndex = [];
    for cord in GridCord:
        Index = []
        for degree in cord:
            deg = re.split('\D+', degree)
            n = int(deg[1])*60 + int(deg[2])
            Index.append(n)
        SRTMGridIndex.append(Index)
    return SRTMGridIndex
 
def Max(a,b): 
    if a > b:
        return a
    else:
        return b

def Fetch_Filename(DHash, SRTMIndex):
    t = SRTMIndex[0], SRTMIndex[1]
    if t in DHash.keys():
        return DHash[t]
    else:
        return 0
    
def Height_Grid(DHash, SRTMIndex, SRTMGridIndex):
    
    from itertools import groupby
    Uniq_SRTMIndex =  [k for k,v in groupby(sorted(SRTMIndex))]
    #print "unique:"
    #print Uniq_SRTMIndex
    
    #4 situation to get the elevation
    #1: all 4 conern are in the same .hgt file
    if len(Uniq_SRTMIndex) == 1:
        filename = Fetch_Filename(DHash, SRTMIndex[0])
        if filename != 0:
            h = Height_Block(filename, SRTMGridIndex[0], SRTMGridIndex[1], SRTMGridIndex[2], SRTMGridIndex[3])
            ##print h
        else:
            h = 0
        #print "#1"    
        #print h
        return h
    
    #2: NW and SW in the same .hgt file; NE and SE in the same .hgt file; NW and NE in different files
    if SRTMIndex[0] == SRTMIndex[2] and SRTMIndex[1] == SRTMIndex[3] and SRTMIndex[0] != SRTMIndex[1]:
        filename1 = Fetch_Filename(DHash, SRTMIndex[0])
        if filename1 != 0:
            h1 = Height_Block(filename1, SRTMGridIndex[0], [SRTMGridIndex[0][0], 0], SRTMGridIndex[2], [SRTMGridIndex[2][0], 0])
        else:
            h1 = 0
        #print h1
        
        filename2 = Fetch_Filename(DHash, SRTMIndex[1])
        if filename2 != 0:
            h2 = Height_Block(filename2, [SRTMGridIndex[1][0], 3600], SRTMGridIndex[1], [SRTMGridIndex[3][0], 3600], SRTMGridIndex[3])
        else:
            h2 = 0    
        #print h2
        
        h = Max(h1, h2)
        #print "#2"  
        #print h
        return h
        
    #3: NW and NE in the same .hgt file; SW and SE in the same .hgt file; NW and SW in different files
    if SRTMIndex[0] == SRTMIndex[1] and SRTMIndex[2] == SRTMIndex[3] and SRTMIndex[0] != SRTMIndex[2]:
        #t1 = SRTMIndex[0][0], SRTMIndex[0][1]
        #filename1 = DHash[t1]
        filename1 = Fetch_Filename(DHash, SRTMIndex[0])
        if filename1 != 0:
            h1 = Height_Block(filename1, SRTMGridIndex[0], SRTMGridIndex[1], [0 ,SRTMGridIndex[0][1]], [0, SRTMGridIndex[1][1]])
        else:
            h1 = 0
        #print h1
        
        #t2 = SRTMIndex[2][0], SRTMIndex[2][1]
        #filename2 = DHash[t2]
        filename2 = Fetch_Filename(DHash, SRTMIndex[2])
        if filename2 != 0:
            h2 = Height_Block(filename2, [3600, SRTMGridIndex[2][1]], [3600, SRTMGridIndex[3][1]], SRTMGridIndex[2], SRTMGridIndex[3])
        else:
            h2 = 0
        #print h2
        
        h = Max(h1, h2)
        #print "#3" 
        #print h
        return h
    
    #4: NW, NE, SW, SE are all in different files
    if len(Uniq_SRTMIndex) == 4:
        #t1 = SRTMIndex[0][0], SRTMIndex[0][1]
        #filename1 = DHash[t1]
        filename1 = Fetch_Filename(DHash, SRTMIndex[0])
        if filename1 != 0:
            h1 = Height_Block(filename1, SRTMGridIndex[0], [SRTMGridIndex[0][0], 0], [0, SRTMGridIndex[0][1]], [0, 0])
        else:
            h1 = 0
        #print h1
        
        #t2 = SRTMIndex[1][0], SRTMIndex[1][1]
        #filename2 = DHash[t2]
        filename2 = Fetch_Filename(DHash, SRTMIndex[1])
        if filename2 != 0:
            h2 = Height_Block(filename2, [SRTMGridIndex[1][0], 3600], SRTMGridIndex[1], [0, 3600], [0, SRTMGridIndex[1][1]])
        else:
            h2 = 0
        #print h2
        
        #t3 = SRTMIndex[2][0], SRTMIndex[2][1]
        #filename3 = DHash[t3]
        filename3 = Fetch_Filename(DHash, SRTMIndex[2])
        if filename3 != 0:
            h3 = Height_Block(filename3, [3600, SRTMGridIndex[2][1]], [3600, 0], SRTMGridIndex[2], [SRTMGridIndex[2][0], 0])
        else:
            h3 = 0
        #print h3
        
        #t4 = SRTMIndex[3][0], SRTMIndex[3][1]
        #filename4 = DHash[t4]
        filename4 = Fetch_Filename(DHash, SRTMIndex[3])
        if filename4 != 0:
            h4 = Height_Block(filename4, [3600, 3600], [3600, SRTMGridIndex[3][1]], [SRTMGridIndex[3][0], 3600], SRTMGridIndex[3])
        else:
            h4 = 0
        #print h4
        
        h = Max(Max(h1, h2), Max(h3, h4))
        #print "#4" 
        #print h
        return h
        
import math

equator_radius = 40075.36 * 1000 #meters

def dis_in_latitude():
    return 30.8

def dis_in_longitude(latitude):
    r = math.sin(math.radians(90-latitude))
    return (equator_radius*r) / (360*60*60)
    
import math

equator_radius = 40075.36 * 1000 #meters

def dis_in_latitude():
    return 30.8

def dis_in_longitude(latitude):
    r = math.sin(math.radians(90-latitude))
    return (equator_radius*r) / (360*60*60)
    
def Degree_Add(s1, s2):
    import re
    #parse s1
    deg1 = re.split('\D+', s1)
    deg1_d = int(deg1[0])
    deg1_m = int(deg1[1])
    deg1_s = int(deg1[2])
    ##print deg1_d, deg1_m, deg1_s
    
    #parse s2
    deg2 = re.split('\D+', s2)
    deg2_d = int(deg2[0])
    deg2_m = int(deg2[1])
    deg2_s = int(deg2[2])
    ##print deg2_d, deg2_m, deg2_s
    
    s_add = deg1_s +deg2_s
    gs = 0
    if s_add >= 60:
        s_add = s_add - 60
        gs = 1
    
    m_add = deg1_m + deg2_m + gs
    gm = 0
    if m_add >= 60:
        m_add = m_add - 60
        gm = 1
        
    d_add = deg1_d + deg2_d + gm
    
    return str(d_add)+'d'+str(m_add)+'m'+str(s_add)+'s'

    
def LatLong_Spacing(spacing, dis_sec):
    total_s = spacing / dis_sec
    
    degree = int(total_s / 3600)
    rd = total_s
    if degree > 0:
        rd = total_s - degree*3600
        
    min = int(rd / 60)
    rm = rd
    if min > 0:
        rm = rd - min*60
        
    sec = int(rm);
    
    return str(degree)+'d'+str(min)+'m'+str(sec)+'s'
    
def Degree_Divide(s1, s2):
    import re
    #parse s1
    deg1 = re.split('\D+', s1)
    deg1_d = int(deg1[0])
    deg1_m = int(deg1[1])
    deg1_s = int(deg1[2])
    total_s1 = deg1_d*3600 + deg1_m*60 + deg1_s
    ##print deg1_d, deg1_m, deg1_s
    
    #parse s2
    deg2 = re.split('\D+', s2)
    deg2_d = int(deg2[0])
    deg2_m = int(deg2[1])
    deg2_s = int(deg2[2])
    total_s2 = deg2_d*3600 + deg2_m*60 + deg2_s
    ##print deg2_d, deg2_m, deg2_s
    
    return int(total_s1 / total_s2) + 1
    
    
def Create_Grid(filename, DHash, NW, NE, SW, SE, Spacing):
    SRTMGrid = [NW, NE, SW, SE]
    SRTMIndex = Get_SRTMIndex(SRTMGrid);
    Lat_Range = str(SRTMIndex[0][0] - SRTMIndex[2][0]) + 'd0m0s'
    Long_Range = str(SRTMIndex[0][1] - SRTMIndex[1][1]+1) + 'd0m0s'
    #print Long_Range, Lat_Range
    
    # latitude and longitude spacing
    Dis_Long_Sec = dis_in_longitude(int(SRTMIndex[0][0]))
    Dis_Lat_Sec = dis_in_latitude()
    LatSpacing = LatLong_Spacing(Spacing, Dis_Lat_Sec)
    LongSpacing = LatLong_Spacing(Spacing, Dis_Long_Sec)
    
    X_size = Degree_Divide(Long_Range, LongSpacing) + 1
    Y_size = Degree_Divide(Lat_Range, LatSpacing) + 1
    #print X_size, Y_size
    
    with open(filename, "w") as f:
        f.write("X\tY\tNorthWest\t\tNorthEast\t\tSouthWest\t\tSouthEast\t\tElevation\n")
        threshold_change_longspace = (Y_size / (int(SRTMIndex[0][0]) - int(SRTMIndex[2][0])+1)) + 1
        ind = 1
        Yt1 = SE[0]
        #print Yt1, LatSpacing
        Yt2 = Degree_Add(Yt1, LatSpacing)
        for y in range(Y_size):
            # change longitude spacing
            #if (y % threshold_change_longspace == 0):
            #   Dis_Long_Sec = dis_in_longitude(int(SRTMIndex[0][0])+ind)
            #    print Dis_Long_Sec
            #    ind = ind + 1
            #    LongSpacing = LatLong_Spacing(Spacing, Dis_Long_Sec)
            
            #keep track with Lat and Long    
            Xt1 = SE[1]
            Xt2 = Degree_Add(Xt1, LongSpacing)
            for x in range(X_size):
                nw = [Yt2, Xt2]
                ne = [Yt2, Xt1]
                sw = [Yt1, Xt2]
                se = [Yt1, Xt1]
                grid = [nw, ne, sw, se]
                #print grid
                SRTMIndex = Get_SRTMIndex(grid);
                #print SRTMIndex
                SRTMGridIndex = Get_SRTMGridIndex(grid)
                #print SRTMGridIndex
                height = Height_Grid(DHash, SRTMIndex, SRTMGridIndex)
                ##print "output:"
                ###print height
                f.write("%d %d %s %s %s %s %d\n" % (x, y, str(nw), str(ne), str(sw), str(se), height))
                #f.write("%d %d %d\n" % (x, y, height))
                Xt1 = Degree_Add(Xt1, LongSpacing)
                Xt2 = Degree_Add(Xt2, LongSpacing)
        
            Yt1 = Degree_Add(Yt1, LatSpacing)
            Yt2 = Degree_Add(Yt2, LatSpacing)
        f.close()
        

if __name__ == "__main__":

    #input parameters:
    Dir = "/Users/student/Documents/Intern/SRTM"; # directory contains all *.hgt files
    OutputFile = "GridSpace10km.txt" # output file name
    Spacing = 10000 # meters
    Area_NW_Conern = ['40d0m0s', '124d0m0s']  #latitude N*** longitude W***
    Area_NE_Conern = ['40d0m0s', '111d0m0s']   #latitude N*** longitude W***
    Area_SW_Conern = ['38d0m0s', '124d0m0s']  #latitude N*** longitude W***
    Area_SE_Conern = ['38d0m0s', '111d0m0s']   #latitude N*** longitude W***
    
    DHash = Hash_Filename(Dir)
    Create_Grid(OutputFile, DHash, Area_NW_Conern, Area_NE_Conern, Area_SW_Conern, Area_SE_Conern, Spacing)
    
    
    
    
    
    
    
    
    