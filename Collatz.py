#!/usr/bin/env python3

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2016
# Glenn P. Downing
# ---------------------------



# ------------
# eager cache
# ------------

# Pre-calculated max collatz cycle length, range size = 5000, e.g. [1, 5000], [5001, 10000], ... [999500, 1000000]
collatz_max_cycle = [238,262,276,279,282,308,311,324,288,314,340,322,335,312,325,351,320,333,333,328,341,354,323,349,336,344,331,344,375,357,370,383,370,352,347,347,365,360,347,360,342,373,373,386,355,368,443,350,368,350,363,345,407,345,407,389,358,389,358,371,371,371,384,353,384,353,353,366,353,441,379,379,410,361,392,423,379,436,405,374,387,405,449,387,418,374,387,400,356,369,387,356,444,413,382,382,413,382,426,395,426,382,470,439,364,408,377,377,408,452,421,390,421,359,377,390,434,359,403,372,403,403,354,447,385,509,385,416,416,385,385,429,367,442,367,385,380,398,442,367,504,380,411,380,411,362,380,424,393,393,424,362,380,468,393,437,362,406,437,468,406,406,406,450,450,419,419,525,388,419,419,388,357,388,432,432,370,445,370,370,401,445,476,432,445,476,414,507,383,383,414,352,414,365,458,383,427,427,365,440]

# Corresponding number which has above collatz max cycle within the range it belongs to 
collatz_max_number = [3711,6171,13255,17647,23529,26623,34239,35655,40959,45127,52527,56095,60975,67691,71310,77031,80225,87087,91463,95081,100167,106239,111451,115547,121950,129991,130631,135111,142587,146599,150015,156159,160411,166011,173321,178075,180463,189855,192711,195465,200334,206847,213881,216367,221353,225023,230631,237433,240617,247387,254911,257001,263103,267113,270271,277615,281401,288489,293198,298843,300030,308071,312318,316577,324551,329151,332022,336199,342599,345947,351359,355143,360361,365185,370153,376603,380233,389191,394655,398457,401151,405407,410011,416423,423679,427762,432734,438699,442697,448265,450651,456798,461262,467739,474121,477417,480481,486827,492571,499647,502137,506977,511935,518921,521241,525543,532715,537095,540542,546681,554143,555230,564905,566609,570348,576978,583787,585327,591983,596415,601327,608111,611455,615017,624635,626331,632161,635519,640641,649051,653739,656761,664063,665215,672398,675969,683947,686985,691894,698111,704623,705193,712683,716126,720722,728859,730183,735679,740306,749227,753206,755478,760465,767903,772859,775035,781860,788315,792735,796095,801769,807327,810399,818943,820022,827503,831215,837799,842881,847358,854191,855583,860327,865401,871915,875681,883903,886953,894623,896530,900735,906175,910107,919791,922524,927003,934299,939497,940257,946623,950943,956156,960962,966249,970599,976254,980905,985142,994395,997823]


# ------------
# collatz_read
# ------------
def collatz_read(s):
    """
    read two ints
    s a string
    return a list of two ints, representing the beginning and end of a range, [i, j]
    """
    a = s.split()
    return [int(a[0]), int(a[1])]



# ------------
# collatz_eval
# ------------


def collatz_eval(i, j):
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """
    # <my code>
    assert i > 0 and j > 0

    # change the sequency of the two input integer if necessary
    if i > j:
        temp = i
        i = j
        j = temp

    # calculate the corresponding range index of i, j in the eager cache 
    i_idx = (i - 1) // 5000
    j_idx = (j - 1) // 5000

    if j_idx > (len(collatz_max_number) - 1):
        j_idx = len(collatz_max_number) - 1
    if i_idx > (len(collatz_max_number) - 1):
        i_idx = len(collatz_max_number) - 1

    # initialize lookup value for cache searching 
    lookup = -1

    # initialize the start number and end number array for non-cached values 
    startNum = []
    endNum = []


    # search cache first

    ## The case that i, j in the same cached range 
    if i_idx == j_idx:
        ### if the max-collatz-cycle-number is in range[i,j], use cache
        if i <= collatz_max_number[i_idx] <= j:
            lookup =  collatz_max_cycle[i_idx]
        ### otherwise have to calculate, save start/end number for calculation
        else:
            startNum.append(i)
            endNum.append(j)

    ## The case that i, j are in the neighboring cached range
    elif j_idx - i_idx == 1:
        ### check if both range can use cache directly 
        if i <= collatz_max_number[i_idx] and j >= collatz_max_number[j_idx]:
            #return max(lookup, max(collatz_max_cycle[i_idx: j_idx + 1]))
            lookup =  max(lookup, max(collatz_max_cycle[i_idx: j_idx + 1]))
        ### check if only the first range can use cache directly
        elif  i <= collatz_max_number[i_idx]:
            lookup = max(lookup, collatz_max_cycle[i_idx])
            startNum.append((i_idx + 1) * 5000 + 1)
            endNum.append(j)
        ### check if only the second range can use cache directly 
        elif j >= collatz_max_number[j_idx]:
            lookup = max(lookup, collatz_max_cycle[j_idx])
            startNum.append(i)
            endNum.append(j_idx * 5000)
        ### no luck, just need to calculate, append start/end number for later calcu 
        else:
            startNum.append(i)
            endNum.append(j)

    ## The case that i, j are seperated by multiple (>1) cached ranges 
    else:
        ### First lookup the max cycle length in the cached ranges between i, j
        lookup = max(lookup, max(collatz_max_cycle[i_idx + 1 : j_idx]))
        ### Check if the two ranges at beginning/end can provide  cache directly
        if i <= collatz_max_number[i_idx] and j >= collatz_max_number[j_idx]:
            lookup =  max(lookup, max(collatz_max_cycle[i_idx :  j_idx + 1]))
        ### Check if the range with i can provide cache directly
        elif  i <= collatz_max_number[i_idx]:
            lookup = max(lookup, collatz_max_cycle[i_idx])
            startNum.append(j_idx * 5000 + 1)
            endNum.append(j)
        ### Check if the range with j can provide cache directly
        elif j >= collatz_max_number[j_idx]:
            lookup = max(lookup, collatz_max_cycle[j_idx])
            startNum.append(i)
            endNum.append((i_idx + 1) * 5000)
        ### No luck, have to calculate two seperated ranges 
        else:
            startNum.append(i)
            startNum.append(j_idx * 5000 + 1)
            endNum.append((i_idx + 1) * 5000)
            endNum.append(i)

    # Check if need to calculate collatz cycle

    ## Value directly from cache, no need to calculate
    if startNum == []:
        return lookup
    ## Otherwise need to calculate the max collatz cycle in append range
    else:
        ### Look through each calculation range, can be 1 or 2 ranges 
        for start, end in zip(startNum, endNum):
            #### Calculate max collatz cycle within given range
            for num in range(start, end + 1):
                cnt = 1
                while True:
                    if  num == 1:
                        break
                    elif num % 2 == 0:
                        num = (num >> 1)
                        cnt = cnt + 1
                    else:
                        assert num % 2 == 1
                        num = num + (num >> 1) + 1
                        cnt = cnt + 2
                #### Only assign max value to lookup for final return
                if cnt > lookup:
                    lookup = cnt
    # Done, return
    assert lookup >=1
    return lookup


# -------------
# collatz_print
# -------------
def collatz_print(w, i, j, v):
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# collatz_solve
# -------------



def collatz_solve(r, w):
    """
    r a reader
    w a writer
    """
    for s in r:
        i, j = collatz_read(s)
        v = collatz_eval(i, j)
        collatz_print(w, i, j, v)

