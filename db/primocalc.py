import datetime
import threading
import time


def calendar(currentpatch,nextpatchdate):
    global patchdates
    patchdates = {}
    while True:
        currenttime = datetime.datetime.now()
        if currenttime > nextpatchdate - datetime.timedelta(days=21):
            nextpatchdate = currenttime + datetime.timedelta(days=21)
            half = 1
            patchdates = {}
            currentpatch += 0.1
            currentpatch = round(currentpatch,2)
        if patchdates == {}:
            half = 1
            p = currentpatch
            p += 0.1
            p = round(p,2)
            for i in range(10):
                if half == 1:
                    patchdates[str(p)] = {str(half): nextpatchdate}
                    #patchdates[str(currentpatch)][str(half)] = nextpatchdate
                    half = 2
                elif half == 2:
                    # half = 1
                    # currentpatch += 0.1
                    # currentpatch = round(currentpatch,2)
                    patchdates[str(p)]["2"] = nextpatchdate
                    p += 0.1
                    p = round(p,2)
                    half = 1
                nextpatchdate = nextpatchdate + datetime.timedelta(days=21)
        time.sleep(1.0)

# calthread = threading.Thread(target=calendar,args = (4,datetime.datetime(2023,9,27,3)))
# calthread.start()

# print(patchdates)

# print("welcome to gacha calc, input your shit")
# primos = int(input("current primos: "))
# crystals = int(input("CRYSTALLIZED: "))
# fates = int(input("fates: "))
# pity = int(input("pity your down bad souls: "))
# guarantee = input("guarenteed? (y/n) ")
# targetpatch = input("where is your WAIFU: ")
# half = input("half: ")
# fivestars = int(input("5 stars: "))
# havewelk = input("have wekin? (y/n) ")
# havebp = input("have bp? (y/n) ")


def worsecase(fivestars,guarantee):
    primoneed = 0
    for i in range(fivestars):
        if guarantee == True:
            primoneed += 90*160
            guarantee = False
        else:
            primoneed += 180*160
            guarantee = True
    return primoneed


def bestcase(fivestars):
    primoneed = 0
    for i in range(fivestars):
        primoneed += 90*160
    return primoneed

def accumulate(days,havewelk,havebp,welkin,welkinplan,bp,bpplan,target):
    dailies = 60
    welk = 90
    currentpatch = 4.0
    primos4free = days*dailies
    patch2targ = (target[0] - currentpatch)*10
    patch2targ = round(patch2targ,2)

    if havewelk == True:
        # 1 welkin = 30days
        if welkin < days:
            primos4free += welk*welkin
            for i in range(1,welkinplan+1):
                primos4free += welk*30
                if i*30 > days-welkin:
                    primos4free += welk*(days-welkin-((i-1)*30))
                    break
        else:
            primos4free += welk*days
   
    elif havebp == True:
        # 1 bp round = patchround
        # 4 fates 680 primos per patch
        if bp < 50:
            primos4free += ((((40-bp)//10)+1)*160) + 680
        if bpplan > patch2targ:
            primos4free += (target[0] - currentpatch)*((4*160)+680)
        if bpplan <= patch2targ:
            primos4free += bpplan*((4*160)+680)
    return primos4free

def plan(days,primos4free,reqprimos,havewelk,havebp,welkin,bpplan,target):
    welk = 90
    currentpatch = 4.0
    patch2targ = (target[0] - currentpatch)*10
    patch2targ = round(patch2targ,2)

    if primos4free < reqprimos:
        print("you will need an extra", reqprimos - primos4free)
        welkneed = 1
        bpneed = 0
        if havewelk == False or days-welkin > 0:
            while primos4free < reqprimos and (welkneed*30) <= days-welkin:
                primos4free += welk*30
                welkneed += 1

        if havebp == False or bpplan < patch2targ:
            while primos4free < reqprimos and bpneed+bpplan < patch2targ:
                primos4free += (4*160)+680
                bpneed += 1
        
        extra = reqprimos - primos4free
        if extra < 0:
            extra = 0

        print(welkneed,"more welkin than planned",bpneed,"more battle passes (lv50) than planned","and an extra",extra,"primos")
    else:
        welkneed = 0
        bpneed = 0
    
    return primos4free,reqprimos,welkneed,bpneed

def calculations(primos,crystals,fates,pity,targetpatch,half,fivestars,havewelk,havebp,welkin,bp,welkinplan,bpplan,patchdates,fiveorprimos):
    currenttime = datetime.datetime.now()
   
    
    worseprimos = worsecase(fivestars,guarantee) - primos - crystals - (fates*160) - (pity*160)
    bestprimos = bestcase(fivestars) - primos - crystals - (fates*160) - (pity*160)
    print(patchdates[targetpatch][half])
    timeremaining = patchdates[targetpatch][half] - currenttime
    days = timeremaining.days
    target = [float(targetpatch),int(half)]
    currenttotal = primos+crystals
    primos4free = accumulate(days,havewelk,havebp,welkin,welkinplan,bp,bpplan,target)
    primosmade = primos4free - currenttotal
    fates4free = primos4free//160

    print("\n")
    print("days remaining", days)
    print("primos you can make by the end of target patch half", primos4free)
    print("best case primos needed", bestprimos)
    bestplan = plan(days,primos4free,bestprimos,havewelk,havebp,welkinplan,bpplan,target)
    print("worse case primos needed", worseprimos)
    worseplan = plan(days,primos4free,worseprimos,havewelk,havebp,welkinplan,bpplan,target)
    possible,bestreq,bestwelk,bestbp = bestplan[0],bestplan[1],bestplan[2],bestplan[3]
    possible,worsereq,worsewelk,worsebp = worseplan[0],worseplan[1],worseplan[2],worseplan[3]
    print("god bless ya gambling addict")

    return currenttotal,primosmade,fates4free,target,primos4free,possible,bestreq,bestwelk,bestbp,worsereq,worsewelk,worsebp


print(calculations(primos,crystals,fates,pity,targetpatch,half,fivestars,havewelk,havebp,patchdates))


#bp is 40 days 
#bp gets fates every lv10 except lv50 gets 680 primos