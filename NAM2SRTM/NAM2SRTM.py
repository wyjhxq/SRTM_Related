import struct

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
    
def Fetch_Filename(DHash, SRTMIndex):
    t = SRTMIndex[0], SRTMIndex[1]
    if t in DHash.keys():
        return DHash[t]
    else:
        return "n"
    
def Get_SRTMIndex(PointCord):
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
    
def get_sample(filename, n, w):
    i = 3601 - int(n+1)  
    j = int(w+1) 
    with open(filename, "rb") as f:
        f.seek((i * 3601 + j) * 2)  # go to the right spot,
        buf = f.read(2)  # read two bytes and convert them:
        val = struct.unpack('>h', buf)  # ">h" is a signed two byte integer
        f.close()
        return val

def Nam2SRTM(NamFile, OutFile, DHash):
    f = open(NamFile, "r")
    line = f.readline()
    with open(OutFile, "w") as outf:
        while line:
            line = f.readline()
            content = line.split()
            if len(content) < 2:
                break
            for i in range(4):
                content[i] = float(content[i])
            latitude = content[2]
            longitude = -content[3]
            SRTMIndex = [0, 0];
            SRTMIndex[0] = int(latitude)
            SRTMIndex[1] = int(longitude) + 1
            filename = Fetch_Filename(DHash, SRTMIndex)
            if len(filename) < 2:
                hgt = (0, 1)
            else:
                n = 3600*(latitude - int(latitude))
                w = 3600*(longitude - int(longitude))
                hgt = get_sample(filename, n, w)
            hgtv = list(hgt)
            #print hgtv[0]
            outf.write("%d %d %d %d %d\n" % ((content[0]), (content[1]), (content[2]), (content[3]), hgt[0]))
        f.close()
    outf.close

if __name__ == "__main__":
    Dir = "/Users/student/Documents/Intern/NAM2SRTM"#"/Users/student/Documents/Intern/Region1"; # directory contains all *.hgt files
    NamFile = "SRTM Elevation for NAM CONUS 218 Grid.txt"
    OutFile = "NAM2SRTM_Mapping.txt"
    DHash = Hash_Filename(Dir)
    Nam2SRTM(NamFile, OutFile, DHash)