#NICHOLAS SUN
#TP062907

import datetime


def startPPEdata():
    genAuthcode()
    print("Welcome to the initial inventory creation")
    print("Please fill the required information with the correct format")
    try:
        with open("Assignment\ppe.txt","w") as ppeFile:
            # Keep asking for input until user wish to discontinue
            while True:
                itemname = input("Please enter the PPE item name : ")
                itemcode = input("Please enter the item code : ")
                suppliercode = input("Register / Enter Supplier Code : ")  
                quantity = int(100)
                YYYY = int(input("Please enter the year item inputted (YYYY) : "))
                MM = int(input("Please enter the month item inputted (MM) : "))
                # to limit month from 1 to 12 only
                MM = monthLimit(MM)
                DD = int(input("Please enter the date item inputted (DD) : "))
                # setting limitation for days in every month
                DD = dayLimit(YYYY, MM, DD)
                ppeData = itemname+"-"+itemcode+"-"+suppliercode+"-"+str(quantity)+"-"+str(YYYY)+"-"+str(MM)+"-"+str(DD)+"\n"
                ppeFile.write(ppeData)
                cont = input("Press Enter key to continue or [q] to stop : ")
                if cont.lower()=="q":
                    print("PPE data has been recorded to ppe.txt file")
                    break
        return 1 # this value will be given to flag on ALL_MENU()
    except:
        print("Error Format Detected, Please try again")

def startSupplydata(mode,supnum):
    try:
        with open("Assignment\ppe.txt","r") as readPPe:
            ppeList = []
            for data in readPPe:
                ppeList.append(data.strip().split("-"))
        # LIST FOR CHECKING WHETHER THE SUPPLY ID HAS ALREADY EXISTED
        with open("Assignment\suppliers.txt",mode) as insupply: 
            for i in range(supnum):
                checklist = []
                supID = input("Please enter registered supplier code / [q] to stop : ")
                if supID.lower()=="q":
                    break

                with open("Assignment\suppliers.txt","r") as readfh:
                    for data in readfh:
                        checklist.append(data.strip().split("-"))
                    
                    checkf=-1
                    for cnt in range(len(checklist)):
                        if supID in checklist[cnt][1]: # IF SUPPLY ID EXISTED
                            print("This supplier code has been inputted")
                            checkf=cnt
                            break
                    if checkf==-1: # IF NOT EXISTED INPUT THE SUPPLY ID INTO suppliers.txt
                        fl = -1
                        for cnt in range(len(ppeList)):
                            if supID in ppeList[cnt][2]:
                                fl=cnt
                                print("Item Supplied : "+ ppeList[cnt][0])
                                supItem = ppeList[cnt][0]
                                supName = input("Enter supplier name : ")
                                supAddress = input("Enter supplier address : ")
                                supQuant = ppeList[cnt][3]
                                suppliers = supName+"-"+supID+"-"+supItem+"-"+supAddress+"-"+str(supQuant)+"\n"
                                insupply.write(suppliers)
                                insupply.flush() # TO REMOVE BUFFER TIME
                        if fl==-1:
                            print("Supplier code not found")
            print("suppliers has been recorded in suppliers.txt")
    except:
        print("Error format / Data not found")

def startHospital(mode,hosnum):
    with open("Assignment\ppe.txt","r") as ppefh:
        list = []
        for data in ppefh:
            list.append(data.strip().split("-"))
        IDlist = []
        for cnt in list:
            IDlist.append(cnt[1])
    try:    
        with open("Assignment\hospital.txt",mode) as fh:
            for x in range(hosnum):
                hosName = input("Enter Hospital name or [q] to stop : ")
                if hosName.lower() == "q":
                    break
                else:
                    u_code(0)
                    hosID = readID(0)
                    hosAdd = input("Enter hospital address : ")
                    hosContact = input("Enter hospital contact number : ")
                    hosData = hosName +"-"+ hosID+"-"+ hosAdd +"-"+ hosContact
                    for i in range(len(IDlist)):
                        # TO LIST OUT ALL THE PPE WITH 0 AS ITS INITIAL QUANTITY OWN BY EACH HOSPITAL
                        hosData = hosData +"-"+ IDlist[i]+"-"+"0"
                    hosData = hosData +"\n"
                    print("Registered Hospital Code is : "+ hosID)
                    fh.write(hosData)
                print("Hospitals has been recorded into hospital.txt")
    except:
        ("Error format / Data not found")

def startDistribution(mode):
    try:
        with open("Assignment\ppe.txt") as ppefh:
            ppeList = []
            for elem in ppefh:
                ppeList.append(elem.strip().split("-"))

        with open("Assignment\hospital.txt") as hospitalfh:
            hospitalList = []
            for elem in hospitalfh:
                hospitalList.append(elem.strip().split("-"))

        with open ("Assignment\distribution.txt",mode) as distFh:
            while True:
                itemID = input("Enter the item code for distribution : ")
                itemflag = 1
                for line in range(len(ppeList)): 
                    if itemID in ppeList[line][1]:
                        itemflag = 2
                        print("This item has quantity of "+ppeList[line][3]+" boxes")
                        send_item = int(input("How many boxes to distribute ? : "))
                        int_itemquantity = int(ppeList[line][3]) 
                        if send_item>int_itemquantity:
                            while True:
                                send_item = int(input("Inssuficcient amount, Enter the correct amount : "))
                                if send_item<=int_itemquantity:
                                    break
                        hospID = input("Enter the destination hospital code : ")
                        hospFlag = 1
                        l2flag = -1
                        for line in range(len(hospitalList)):
                            if hospID in hospitalList[line][1]:
                                for cnt in range(4,len(hospitalList[line])):
                                    # Adding to Hospital File
                                    if itemID in hospitalList[line][cnt] and cnt%2==0:
                                        hosquant = int(hospitalList[line][cnt+1])
                                        receive_quant = hosquant + send_item
                                        hospitalList[line][cnt+1] = str(receive_quant)
                                        hospFlag = 2
                                        print("This item has been distributed")
                                        u_code(1)
                                        distID = readID(1)
                                        print("Distribution Code is : "+distID)
                                        distData = itemID+"-"+str(send_item)+"-"+hospID+"-"+distID+"\n"
                                        distFh.write(distData)
                                        break
                                
                                # Subtracting from PPE File
                                for cnt in range(len(ppeList)):
                                    if itemID in ppeList[cnt][1]:
                                        break
                                current_quantity = int(ppeList[cnt][3])
                                new_quant = current_quantity - send_item
                                ppeList[cnt][3] = str(new_quant)

                                with open("Assignment\ppe.txt","w") as pfh:
                                    for cnt in range(len(ppeList)):
                                        rec = "-".join(ppeList[cnt])+"\n"
                                        pfh.write(rec)

                                with open("Assignment\hospital.txt","w") as hfh:
                                    for cnt in range(len(hospitalList)):
                                        rec = "-".join(hospitalList[cnt])+"\n"
                                        hfh.write(rec)
                                
                                cont = input("Enter [n] to exit this process : ")
                                if cont.lower() == "n":
                                    print("Distribution has been recorded to distribution.txt")
                                    l2flag =1
                                    break # break inner for loop
                        if l2flag == 1: # flag to break outer for loop
                            break
                        if hospFlag == 1:
                            print("Hospital ID not found")
                            break    
                if itemflag == 1:
                    print("Item not found")
                    break 
                if l2flag == 1:
                    break # TO BREAK WHILE LOOP
    except:
        print("Error format/File doesn't exist")

def startTransactions():
    try:
        with open("Assignment\suppliers.txt","r") as supfh:
            suplist = []
            for data in supfh:
                suplist.append(data.strip().split("-"))

        with open("Assignment\ppe.txt") as ppefh:
            ppelist = []
            for data in ppefh:
                ppelist.append(data.strip().split("-"))

        with open("Assignment\Transactions.txt","a") as transfh:
            while True:
                supplierID = input("Enter supplier ID : ")
                supflag = -1
                l1flag = -1
                for cnt in range(len(suplist)):
                    if supplierID in suplist[cnt][1]:
                        supflag = cnt
                        sup_quant = int(suplist[cnt][4])
                        item_name = suplist[cnt][2]
                        for cnt_ppe in range(len(ppelist)):
                            if item_name in ppelist[cnt_ppe][0]:
                                ItemID = ppelist[cnt_ppe][1]
                                break                        
                        print("Item ID is :", ItemID)
                        for cnt in range(len(ppelist)):
                            if ItemID in ppelist[cnt][1]:
                                ppe_quant = int(ppelist[cnt][3])
                                receive_quantity = int(input("Enter quantity of item added : "))
                                new_sup_q = sup_quant + receive_quantity
                                new_ppe_q = ppe_quant + receive_quantity
                                suplist[cnt][4] = str(new_sup_q)
                                ppelist[cnt][3] = str(new_ppe_q)
                                u_code(2)
                                TransID = readID(2)
                                print("Transaction ID :", TransID)
                                Date = datetime.date.today()
                                trans = ItemID + "-"+supplierID+"-"+str(receive_quantity)+"-"+str(Date)+"-"+TransID+"\n"
                                transfh.write(trans)

                                with open("Assignment\ppe.txt","w") as fh:
                                    for cnt in range(len(ppelist)):
                                        rec = "-".join(ppelist[cnt])+"\n"
                                        fh.write(rec)
                                with open("Assignment\suppliers.txt","w") as fh:
                                    for cnt in range(len(suplist)):
                                        rec = "-".join(suplist[cnt])+"\n"
                                        fh.write(rec)

                                cont = input("Do you wish to make another transactions? [n] to stop : ")
                                if cont.lower() == "n":
                                    print("Transactions has been recorded in Transactions.txt")
                                    l1flag = 1
                                    break 
                    if l1flag ==1:
                        break
                if l1flag ==1:
                    break        
                if supflag == -1:
                    print("Supplier Code not found")
                    break
    except:
        print("Error format/Data not found")
    

def AddPPEdata():
    try:
        print("Please fill the required information with the correct format")
        with open("Assignment\ppe.txt","a") as ppeFile:
            # Keep asking for input until user wish to discontinue
            while True:
                itemname = input("Please enter the PPE item name : ")
                itemcode = input("Please enter the item code : ")
                suppliercode = input("Register / Enter Supplier Code : ")  
                quantity = int(100)
                YYYY = int(input("Please enter the year item inputted (YYYY) : "))
                MM = int(input("Please enter the month item inputted (MM) : "))
                # to limit month from 1 to 12 only
                MM = monthLimit(MM)
                DD = int(input("Please enter the date item inputted (DD) : "))
                # setting limitation for days in every month
                DD = dayLimit(YYYY, MM, DD)
                ppeData = itemname+"-"+itemcode+"-"+suppliercode+"-"+str(quantity)+"-"+str(YYYY)+"-"+str(MM)+"-"+str(DD)+"\n"
                ppeFile.write(ppeData)
                cont = input("Press Enter key to continue or [q] to stop : ")
                if cont.lower()=="q":
                    print("PPE data has been recorded to ppe.txt file")
                    break          
    except:
        print("Error format/Please Try again")               

#REPLACING THE CODE WITH THE GENERATED CODE
def u_code(ind):
    codeList = []
    with open("Assignment\codegate.txt","r") as algocode:
        for code in algocode:
            codeList.append(code.strip().split("-"))
        num = codeList[0][ind]
        numtemp = num[6:]
        numonly = int(numtemp)
        numList = []
        numonly+=1
        numList.append(numonly)
    newcode=[]
    newcode.append(codeList[0][ind][0:6]) # HID989[2]-DID656[3]-TID747[0]
    tempCode = newcode + (numList)
    # newcode = first 6 string  # numList = last digit
    genCode = ""
    for i in range(2):
        genCode = genCode+str(tempCode[i])
    codeList[0][ind] = genCode
    with open("Assignment\codegate.txt","w") as codewriter:
        for code in codeList:
            cd = "-".join(code)
        codewriter.write(cd)

#READ THE GENERATED CODE
def readID(ind):
    codelist = []
    with open("Assignment\codegate.txt","r") as readsup:
        for code in readsup:
            codelist.append(code.strip().split("-"))
    ID = codelist[0][ind]
    return ID

#INITIALLY CREATE THE STARTER CODE
def genAuthcode():
    with open("Assignment\codegate.txt","w") as authFile:
        auth = "HID9890"+"-"+"DID6560"+"-"+"TID7470"
        authFile.write(auth)

#INITIALLY CREATE THE ADMIN ACCOUNT
def userSignUp(file):
    with open("Assignment\login.txt","a") as loginFile:
        while True:
            userName = input("Enter your User ID : ")
            userPW = input("Enter your Password : ")
            LoginData = file +"-"+userName +"-"+ userPW+"\n"
            loginFile.write(LoginData)
            print("User account has been succesfully saved")
            break
    
        

#TO CHECK WHETHER THE ACCOUNT IS REGISTERED OR NOT
def userLogin(file):
    try:
        with open("Assignment\login.txt","r") as readLogin:
            USERLOGDATA = []
            for userData in readLogin:
                USERLOGDATA.append(userData.strip().split("-"))
        
        for cnt in range (len(USERLOGDATA)):
            if file in USERLOGDATA[cnt][0]:
                userLogin = input("Enter existing User ID : ")
                userPassword = input("Enter Password : ")
                if USERLOGDATA[cnt][1] == userLogin and USERLOGDATA[cnt][2] == userPassword:
                    print("Succesful")
                    return True 
                else:
                    print("Login failed")
    except:
        print("Error format/Data not found")

#FUNCTION TO TRACK AVAILABLE QUANTITY OF ITEMS
def viewInformation():
    ppeInfo = []
    supInfo = []
    combInfo = []
    with open("Assignment\ppe.txt","r") as readPPE: 
        for info in readPPE:
            ppeInfo.append(info.strip().split("-"))
    with open("Assignment\suppliers.txt","r") as readSuppliers:
        for info in readSuppliers:
            supInfo.append(info.strip().split("-"))
    allList = []
    for cnt in range(len(supInfo)):
        combInfo = ppeInfo[cnt] + supInfo[cnt]
        allList.append(combInfo)
    # Sorting Ascending
    for x in range(len(allList)-1):
        for y in range(x+1,len(allList)):
            if allList[x][0] > allList[y][0]:
                temp = allList[x]
                allList[x] = allList[y]
                allList[y] = temp
    headerView(allList)

def view25():
    allList = []
    with open("Assignment\ppe.txt","r") as readPPE: 
        for info in readPPE:
            allList.append(info.strip().split("-"))
            
    flag = -1
    for cnt in range(len(allList)):
        quant = int(allList[cnt][3])
        item_name = allList[cnt][0]
        item_ID = allList[cnt][1]
        if quant < 25:
            flag = cnt
            print(item_name+" "+item_ID+" has quantity of "+str(quant)+" boxes left")        
    if flag == -1:
        print("All item stock is above 25 boxes")

def ppeview():
    with open("Assignment\ppe.txt") as fh:
        ppe = []
        for data in fh:
            ppe.append(data.strip().split("-"))

        print("="* 75)
        print("Item Name".center(15)+"|"+"Item Code".center(20)+"|"+"Item Quantity(Box)".center(20)+"|"+"Date Inputted".center(15))
        print("="* 75) 
        for line in range(len(ppe)): 
            print(ppe[line][0].center(15)+"|"+ppe[line][1].center(20)+"|"+ppe[line][3].center(20)+"|"+(ppe[line][4]+"/"+ppe[line][5]+"/"+ppe[line][6]).center(15))
 
def supplyview():
    with open("Assignment\suppliers.txt") as fh:
        supplier = []
        for data in fh:
            supplier.append(data.strip().split("-"))
        print("="* 95)
        print("Supplier Name".center(15)+"|"+"Supplier Code".center(20)+"|"+"Item Supplied".center(20)+"|"+"Supplier Address".center(20)+"|"+"Item quantity".center(15))
        print("="* 95) 
        for line in range(len(supplier)): 
            print(supplier[line][0].center(15)+"|"+supplier[line][1].center(20)+"|"+supplier[line][2].center(20)+"|"+supplier[line][3].center(20)+"|"+supplier[line][4].center(15))

def hospitalview():
    with open("Assignment\hospital.txt") as fh:
        hospital = []
        for data in fh:
            hospital.append(data.strip().split("-"))
        print("="* 75)
        print("Hospital Name".center(15)+"|"+"Hospital Code".center(20)+"|"+"Hospital Address".center(20)+"|"+"Contact Number".center(15))
        print("="* 75) 
        for line in range(len(hospital)): 
            print(hospital[line][0].center(15)+"|"+hospital[line][1].center(20)+"|"+hospital[line][2].center(20)+"|"+hospital[line][3].center(15))

def headerView(lists):
    print("="* 136)
    print("Item Name".center(15)+"|"+"Item Code".center(20)+"|"+"Item Quantity(Box)".center(20)+"|"+"Supplier Name".center(20)+"|"+"Supplier Code".center(20)+"|"+"Supplier Address".center(20)+"|"+"Date Inputted".center(15))
    print("="* 136) 
    for line in range(len(lists)): 
        print(lists[line][0].center(15)+"|"+lists[line][1].center(20)+"|"+lists[line][3].center(20)+"|"+lists[line][7].center(20)+"|"+lists[line][8].center(20)+"|"+lists[line][10].center(20)+"|"+(lists[line][4]+"/"+lists[line][5]+"/"+lists[line][6]).center(15))

# VIEWDISTRIBUTION
def viewDistribution():
    with open("Assignment\distribution.txt","r") as disfh:
        dislist = []
        for elem in disfh:
            dislist.append(elem.strip().split("-"))
        print("="* 77)
        print("Item Code".center(15)+"|"+"Item Quantity(Box)".center(20)+"|"+"Hospital Code".center(20)+"|"+"Distribution Code".center(20))
        print("="* 77) 
        for line in range(len(dislist)): 
            print(dislist[line][0].center(15)+"|"+dislist[line][1].center(20)+"|"+dislist[line][2].center(20)+"|"+dislist[line][3].center(20))    

def modifyPPE():
    try:
        data = []
        with open("Assignment\ppe.txt","r") as fh:
            for line in fh:
                elem = line.strip().split("-")
                data.append(elem)  
        skey = input("Please enter Item Code : ")
        flg = -1
        for cnt in range(len(data)):
            if skey in data[cnt][1]:
                flg = cnt
                break
        if flg == -1:
            print("Data not found")
        if flg != -1:
            print("1 -Item Name   : "+ data[flg][0])
            print("2 -Item Code     : "+ data[flg][1])
            print("3 -Supplier Code : "+ data[flg][2])
            print("4 -Quantity : "+ data[flg][3])
            print("5- Year : "+ data[flg][4])
            print("6 -Month : "+ data[flg][5])
            print("7 -Date : "+ data[flg][6])
            ans = int(input("Ënter the number to modify :"))
            ans = limitopt(ans,7)  
            data[cnt][ans-1] = input("Ënter a new value: ")
            print("***Succesfully changed***")
            with open("Assignment\ppe.txt","w") as fh:
                for cnt in range(len(data)):
                    rec = "-".join(data[cnt])+"\n"
                    fh.write(rec)
    except:
        print("Error or File not found")

def modifySup():
    try:
        data = []
        with open("Assignment\suppliers.txt","r") as fh:
            for line in fh:
                rec = line.strip().split("-")
                data.append(rec)     
        skey = input("Please enter Supplier Code : ")
        flg = -1
        for cnt in range(len(data)):
            if skey in data[cnt][1]:
                flg = cnt
                break
        if flg == -1:
            print("Data not found")
        if flg != -1:
            print("1 -Supplier Name : "+ data[flg][0])
            print("2 -Supplier Code : "+ data[flg][1])
            print("3 -Item Supplied : "+ data[flg][2])
            print("4 -Supplier Address : "+ data[flg][3])
            print("5 -Quantity Supplied : "+ data[flg][4])
            ans = int(input("Ënter the number to modify :"))
            ans = limitopt(ans,5)   
            data[cnt][ans-1] = input("Ënter a new value: ")
            print("***Succesfully changed***")
            with open("Assignment\suppliers.txt","w") as fh:
                for cnt in range(len(data)):
                    rec = "-".join(data[cnt])+"\n"
                    fh.write(rec)
    except:
        print("Error or File not found")

def modifyHosp():
    try:
        data = []
        with open("Assignment\hospital.txt","r") as fh:
            for line in fh:
                rec = line.strip().split("-")
                data.append(rec)     
        skey = input("Please enter Supplier Code : ")
        flg = -1
        for cnt in range(len(data)):
            if skey in data[cnt][1]:
                flg = cnt
                break
        if flg == -1:
            print("Data not found")
        if flg != -1:
            print("1 -Hospital Name : "+ data[flg][0])
            print("2 -Hospital Code : "+ data[flg][1])
            print("3 -Hospital Address : "+ data[flg][2])
            print("4 -Contact Number : "+ data[flg][3])
            ans = int(input("Ënter the number to modify :"))
            ans = limitopt(ans,4)   
            data[cnt][ans-1] = input("Ënter a new value: ")
            print("***Succesfully changed***")
            with open("Assignment\hospital.txt","w") as fh:
                for cnt in range(len(data)):
                    rec = "-".join(data[cnt])+"\n"
                    fh.write(rec)
    except:
        ("Error or File not found")

def searchPPEDetail():
    try:
        ppeInfo = []
        with open("Assignment\ppe.txt","r") as readPPE: 
            for info in readPPE:
                ppeInfo.append(info.strip().split("-"))
        skey = input("Please enter item Code : ")
        flag = -1
        for line in range (len(ppeInfo)):
            if skey in ppeInfo[line][1]:
                flag = line
                print("="* 115)
                print("Item Name".center(15)+"|"+"Item Code".center(20)+"|"+"Supplier Code".center(20)+"|"+"Item Quantity(Box)".center(20)+"|"+"Date Inputted".center(15))
                print("="* 115)
                print(ppeInfo[line][0].center(15)+"|"+ppeInfo[line][1].center(20)+"|"+ppeInfo[line][2].center(20)+"|"+ppeInfo[line][3].center(20)+"|"+(ppeInfo[line][4]+"/"+ppeInfo[line][5]+"/"+ppeInfo[line][6]).center(15)) 
                break
        if flag == -1:
            print("Data not found")         
    except:
        print("Error format/Data not exist")

def searchSupDetail():
    try:
        supInfo = []
        with open("Assignment\suppliers.txt","r") as readSup: 
            for info in readSup:
                supInfo.append(info.strip().split("-"))
        skey = input("Please enter supplier Code : ")
        flag = -1
        for line in range (len(supInfo)):
            if skey in supInfo[line][1]:
                flag = line
                print("="* 116)
                print("Supplier Name".center(15)+"|"+"Supplier Code".center(20)+"|"+"Item Supplied".center(20)+"|"+"Supplier Address".center(20)+"|"+"Quantity Supply".center(20))
                print("="* 116)
                print(supInfo[line][0].center(15)+"|"+supInfo[line][1].center(20)+"|"+supInfo[line][2].center(20)+"|"+supInfo[line][3].center(20)+"|"+supInfo[line][4].center(15)) 
                break
        if flag == -1:
            print("Data not found")         
    except:
        print("Error format/Data not exist")

def searchHospDetail():
    try:
        hospeInfo = []
        with open("Assignment\hospital.txt","r") as readfh: 
            for info in readfh:
                hospeInfo.append(info.strip().split("-"))
        skey = input("Please enter Hospital Code : ")
        flag = -1
        for line in range (len(hospeInfo)):
            if skey in hospeInfo[line][1]:
                flag = line
                print("="* 75)
                print("Hospital Name".center(15)+"|"+"Hospital Code".center(20)+"|"+"Hospital Address".center(20)+"|"+"Contact Number".center(15))
                print("="* 75) 
                print(hospeInfo[line][0].center(15)+"|"+hospeInfo[line][1].center(20)+"|"+hospeInfo[line][2].center(20)+"|"+hospeInfo[line][3].center(15))
                break
        if flag == -1:
            print("Data not found")         
    except:
        print("Error format/Data not exist")

def searchDistribution():
    with open("Assignment\distribution.txt","r") as disfh:
        dislist = []
        for elem in disfh:
            dislist.append(elem.strip().split("-"))
        
        skey = input("Please enter item Code : ")
        flag = -1
        print("="* 77)
        print("Item Code".center(15)+"|"+"Item Quantity(Box)".center(20)+"|"+"Hospital Code".center(20)+"|"+"Distribution Code".center(20))
        print("="* 77)
        for line in range (len(dislist)):
            if skey in dislist[line][0]:
                flag = line
                while True:
                    print(dislist[line][0].center(15)+"|"+dislist[line][1].center(20)+"|"+dislist[line][2].center(20)+"|"+dislist[line][3].center(20))
                    break
        if flag == -1:
            print("Data not found")   

def monthLimit(MM):
    if MM<1 or MM>12:
        mFlag = -1
        while mFlag == -1:
            MM = int(input("Please enter the month in the proper format (MM) : "))
            if MM>0 and MM<=12:
                mFlag=MM
                break
    return MM

def dayLimit(YYYY, MM, DD):
    if MM == 4 or MM == 6 or MM == 9 or MM == 11:
        if DD<1 or DD>30:
            dFlag = -1
            while dFlag == -1:
                DD=int(input("Please enter the date in the proper format : "))
                if DD>0 and DD<=30:
                    dFlag = DD
                    break
    elif YYYY%4==0 and MM==2:
        if DD<1 or DD>29:
            d2Flag = -1
            while d2Flag == -1:
                DD=int(input("Please enter the date with the correct format : "))
                if DD>0 and DD<=29:
                    d2Flag == DD
                    break
    elif YYYY%4!=0 and MM == 2:
        if DD<1 or DD>28:
            d3Flag = -1
            while d3Flag == -1:
                DD=int(input("Please enter the date with the correct format : "))
                if DD>0 and DD<=28:
                    d3Flag == DD
                    break
    elif DD<1 or DD>31:
        d4Flag = -1
        while d4Flag == -1:
            DD=int(input("Please enter the date the correct format : "))
            if DD>0 and DD<=31:
                d4Flag = DD
                break
    return DD

def limitopt(opt,upper):
    while opt<1 or opt>upper:
        opt = int(input("Enter according to the option available : "))
        if opt in range(1,upper+1):
            break
    return opt

def gate(arr,opt,file):
    if arr[opt-1] == 0:       
        userSignUp(file)
        arr[opt-1] =1  
    else:
        print("*** Account Exist ***") 


# ==================================
# Main Function

def ALL_MENU():
    try:
        # AFTER INITIAL CREATION FUNC WILL RETURN 1 to flag
        flag = startPPEdata()
    ############     FLAG FOR MENU
        MENU_ARRAY = [1,0,0,0,0]
    ############## PPE,SUP,HOS,DIS,TRAN # WHEN ADMIN CREATED FOR EACH WILL TURN TO 1
        SUB_MENU_FLAG = [0,0,0,0,0]
        while True: 
            if flag == 1:
                while True:
                #MENU 1
                    print("1 - Create Admin Account")
                    print("2 - PPE File")
                    print("3 - Suppliers File")
                    print("4 - Hospital File")
                    print("5 - Move to Next Menu")
                    option =int(input("Enter your option : "))
                    option = limitopt(option,5)
                    if option == 1:
                    #SUBMENU1-1
                        while True:
                            print("1. ppe.txt")
                            print("2. suppliers.txt")
                            print("3. hospital.txt")
                            print("4. Distribution")
                            print("5. Transactions")
                            print("6. Move to Last Menu")
                            ask = int(input("Enter your option : "))
                            ask = limitopt(ask,6)
                            if ask == 1: 
                                gate(SUB_MENU_FLAG,ask,"ppe")
                            elif ask ==2:
                                gate(SUB_MENU_FLAG,ask,"suppliers")
                            elif ask==3:
                                gate(SUB_MENU_FLAG,ask,"hospital")
                            elif ask==4:
                                gate(SUB_MENU_FLAG,ask,"distribution")             
                            elif ask==5:
                                gate(SUB_MENU_FLAG,ask,"Transactions")
                            elif ask==6:
                                break
                    elif option == 2 and SUB_MENU_FLAG[option-2]==0:
                        print("Please Create Admin account!!")
                    
                    elif option == 2 and MENU_ARRAY[option-2]==1 and SUB_MENU_FLAG[option-2]==1:
                        if userLogin("ppe")==True:
                            while True:
                                print("1. View Personal Protective Equipment Data")
                                print("2. Search Specific Item")
                                print("3. Modify data in File")
                                print("4. Move to Last Menu")
                                ask = int(input("Enter your option : "))
                                ask = limitopt(ask,4)
                                if ask == 1:
                                    ppeview()
                                elif ask ==2:
                                    searchPPEDetail()
                                elif ask ==3:
                                    modifyPPE()
                                elif ask==4:
                                    break
                    
                    elif option == 3 and MENU_ARRAY[option-2]==0:
                        supnum = int(input("Enter how many suppliers to input : "))
                        startSupplydata("w",supnum)
                        MENU_ARRAY[option-2]=1

                    elif option ==3 and SUB_MENU_FLAG[option-2]==0:
                        # WHEN ADMIN ACCOUNT DOES NOT EXISTED
                        print("Please Create Admin Account!!")
                        
                    elif option==3 and MENU_ARRAY[option-2]==1 and SUB_MENU_FLAG[option-2]==1:
                        if userLogin("suppliers") == True:
                            while True:
                                print("1. View Suppliers Data")
                                print("2. Search Specific Supplier")
                                print("3. Modify data in File")
                                print("4. Move to Last Menu")
                                ask = int(input("Enter your option : "))
                                ask = limitopt(ask,4)
                                if ask ==1:
                                    supplyview()
                                elif ask==2:
                                    searchSupDetail()
                                elif ask==3:
                                    modifySup()
                                elif ask==4:
                                    break
                
                    elif option == 4 and MENU_ARRAY[option-2]==0:
                        hosnum=int(input("Enter how many hospital to input : "))
                        startHospital("w",hosnum)
                        MENU_ARRAY[option-2]=1

                    elif option ==4 and SUB_MENU_FLAG[option-2]==0:
                        # WHEN ADMIN ACCOUNT DOES NOT EXISTED
                        print("Please Create Admin Account!!")
                
                    elif option ==4 and MENU_ARRAY[option-2]==1 and SUB_MENU_FLAG[option-2]==1:
                        if userLogin("hospital")==True:
                        # SUBMENU1-4
                            while True:
                                print("1. View Hospital Data")
                                print("2. Search Specific Hospital")
                                print("3. Modify data in File")
                                print("4. Move to Last Menu")
                                ask = int(input("Enter your option : "))
                                ask = limitopt(ask,4)
                                if ask ==1:
                                    hospitalview()
                                elif ask==2:
                                    searchHospDetail()
                                elif ask==3:
                                    modifyHosp()
                                elif ask==4:
                                    break       
                #MOVE TO MENU2
                    elif option == 5:
                        flag =2
                        break

            elif flag == 2:
                while True:
                #MENU 2
                    print("1 - Register more PPE Item")
                    print("2 - Register more Supplier")
                    print("3 - Register more Hospital")
                    print("4 - Hospital Distribution") #DISTRIBUTING ITEM TO HOSPITAL
                    print("5 - Supplier Transaction") #UPDATE QUANTITY WHEN SUPPLIER ADD ITEM
                    print("6 - Inventory Tracking") #TOTAL ITEM & RECORD OF QUANTITY<25\
                    print("7 - Distribution List")
                    print("8 - Move to Last Menu")
                    print("9 - End the Programme")
                    option =int(input("Enter your option : "))
                    option = limitopt(option,9)
                    if option == 1:
                        AddPPEdata() # ADDING MORE DATA INTO ppe.txt
                    elif option == 2:
                        supnum = int(input("Enter how many suppliers to input : "))
                        startSupplydata("a",supnum) # ADDING MORE DATA into suppliers.txt
                    elif option == 3:
                        hosnum=int(input("Enter how many hospital to input : "))
                        startHospital("a",hosnum) # ADDING MORE DATA into hospital.txt
                    elif option == 4:
                        if MENU_ARRAY[option-2]==1:
                            if userLogin("distribution")==True:
                                startDistribution("a")
                        else:
                            print("hospital.txt / Admin account does not exist")
                    elif option == 5:
                        if MENU_ARRAY[1]==1:
                            if userLogin("Transactions")==True:
                                startTransactions()
                        else:
                            print("suppliers.txt / Admin account does not exist")
                    elif option == 6:
                    #SUBMENU2-6
                        while True:
                            print("1. View quantity available for all item")
                            print("2. View all item < 25 boxes")
                            print("3. Move to Last Menu")
                            ask = int(input("Enter your option : "))
                            ask = limitopt(ask,3)
                            if ask == 1:
                                viewInformation()
                            elif ask ==2:
                                view25()
                            elif ask ==3:
                                break
                    elif option==7:
                    #SUBENU2-7
                        while True:
                            print("1. View All Distribution")
                            print("2. Search for specific item distribution")
                            print("3. Move to Last Menu")
                            ask = int(input("Enter your option : "))
                            ask = limitopt(ask,3)
                            if ask ==1:
                                viewDistribution()
                            elif ask ==2:
                                searchDistribution()
                            elif ask==3:
                                break
                    elif option == 8:
                        flag = 1
                        break
                    elif option == 9:
                        flag = 3
                        break             
            elif flag == 3:
                break

        print("End of programme")
    except:
            print("Error format/Data not found, Please Restart the Program")

# MAINLOGIC
ALL_MENU()
# END