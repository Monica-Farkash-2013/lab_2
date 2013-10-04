'''
Created on Sep 30, 2013

@author: fedora
'''
import re
import sys

def strcmp(ax,by):
    
    # strip the blank spaces
    a = ax.replace(' ', '').strip('\t')
    b = by.replace(' ', '').strip('\t')
    
    # test the length
    af = len(a)
    bf = len(b)

    if (af!=bf): return 0
    if ((af==0) or (bf==0)): return 0
    if ((a=='nil') and (b=='nil')): return 0    
    
    for k in range (0,af):
        ca = a[k].capitalize()
        cb = b[k].capitalize()
        if (ca!= cb): 
            return 0    
    #print("SAME NAME "+ a +" with "+b)    
    return 1
#*****************************************************************************
#*****************************************************************************
#*****************************************************************************

if __name__ == '__main__':
    print ("\nLooking for potential pairs among the contents of the file you provide")
    if (len(sys.argv)>1):
        ins = open(sys.argv[1],"r")
    else:
        """  
        print ("Please provide the input file: python choose.py <file_name>")
        sys.exit()
        """
        ins = open( "MyTest4.txt", "r" )
    
    print ("....")
    verbose = 0; 
   
    # reads values in an array
    arr = []
    
    nr=0
    for line in ins:
        nr+=1
        #words = itertools.chain(*[i.split(':') for i in line])
        words = re.split(':|\n', line)
        if (words[0]==''):
            nr-=1
        else:
            for i in range (0,4): words.append( 'nil')
            arr.append( words )
    
    ins.close()
    if(verbose): 
        print ("Bears in the file = ",nr)
        print arr
        
    # initializes fields
    m=0 
    while m < nr:
        arr[m][5]='nil'
        arr[m][9]='0'
        m+=1
    
    m=0
    j=0
    
    while m < nr:
        j=0
        while (j < nr-1 ):
            #print (x,y,"COMPARING" + arr[m][2] + "with" + arr[j][0])
            if ( strcmp(arr[m][2],arr[j][0])) : 
                #print (arr[m][2], "FOUND MOTER SIDE")
                arr[m][5] = arr[j][2]
                arr[m][6] = arr[j][3]
            #print ("COMPARING" + arr[m][3] + "with" + arr[j][0])
            if ( strcmp(arr[m][3],arr[j][0] )):
                #print (arr[m][3], "FOUND FATHER SIDE")
                arr[m][7] = arr[j][2]
                arr[m][8] = arr[j][3]
            if ( strcmp(arr[m][0],arr[j][2] ) or strcmp(arr[m][0],arr[j][3])):
                arr[m][9]='1'
                #print (arr[m][0]+ " already is a parent to "+ arr[j][0])
            j+=1       
        m+=1

    if(verbose): 
        print("We identified if a bear has grandparents and/or offsprings")
        print arr

# each record will have names of grandparents or duplicate names of parents 
# <name> <M/F> <mother> <father> <age> <mother's mother> <mother's father> <father's mother> <father's father> <'0'/'1'>
# <name> <M/F> <mother> <father> <age> <''> <'0'> <father's mother> <father's father> <'0'/'1'>
# <name> <M/F> <mother> <father> <age> <mother's mother> <mother's father> <'0'> <'0'>  <'0'/'1'>                
# <name> <M/F> <mother> <father> <age> <''> <'0'> <'0'> <'0'> <'0' or '1'> depending if it has offsprings or not       

    """
    we check for each bear if there is a match
    for each bear until the end of bears
        if has offsprings - no match
        for each bear lower down the list
            if(constraints fulfilled) print it as match
    """
    no_match=0
    m=0
    j=0
    while m < nr:
        # already has at least an offspring
        no_match=0
        if (arr[m][9]=='1'): 
            if(verbose): print(arr[m][0]+"\tALREADY has at least an offspring")
            no_match=1 
            
        if (no_match==0):
            j=0
            # I Can always build my own precision - in this case 2 decimals ( * 100) 
            #age_m = float(arr[m][4].strip(' '''))
            age_m = int(100*float(arr[m][4].strip(' \t')))
            while ((j < nr )):
                if (j>m):
                    #age_j=float(arr[j][4].strip(' '''))
                    age_j=int(100*float(arr[j][4].strip(' \t')))
                    no_match=0
                    if(verbose): print (arr[m][0] +" & " + arr[j][0])
                         
                    # already has an offspring
                    if (arr[j][9]=='1'): 
                        if(verbose): print(arr[m][0]+"\tALREADY has at least an offspring")
                        no_match=1 

                    # if they both have the same sex - no deal
                    if ( strcmp(arr[m][1],arr[j][1])) : 
                        no_match=1 
                        if(verbose): print ("\tSAME SEX PROBLEM"+ arr[m][1] + arr[j][1])
                    
                    # too young or too old
                    if(no_match==0):
                        if (age_m < 200) or (age_j < 200): 
                            no_match=1
                            if(verbose): print ("\tTHERE WAS AGE PROBLEM : one is too young "+arr[m][4] +arr[j][4] )
                    
                    if(no_match==0):
                        if ((age_m > 600) or (age_j> 600)): 
                            no_match=1
                            if(verbose): print ("\tTHERE WAS AGE PROBLEM: one is too old "+arr[m][4] +arr[j][4] )
                
                    # checking if common ancestor 
                    if (no_match==0):
                        for p in {0,2,3,5,6,7,8}:
                            for q in {0,2,3,5,6,7,8}:
                                if (strcmp(arr[m][p],arr[j][q])) : 
                                    if(verbose): print ("\tTHERE WAS A Common Ancestor"+ arr[m][p] + arr[j][q])
                                    no_match=1
                 
                    # more than one year difference
                    if(no_match==0):
                        if(abs(age_m-age_j) >100): 
                            no_match=1
                            if(verbose): print ("\tTHE AGE DIFFERENCE is a problem"+arr[m][4] +arr[j][4])
                    
                    # found a match
                    if (no_match ==0): print (arr[m][0] + " + " + arr[j][0])  
                j+=1    
        m+=1
    
    print ("Finished")
    