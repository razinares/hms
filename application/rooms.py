from application.db import *



# ARRAY for Bed numbers
array = [[[101,102,103,104,105], [106,107,108, 109, 110]], [[201, 202], [203, 204], [205, 206], [207,208], [209, 210]], [[301], [302], [303], [304], [305]]]


# Returns available beds array
def avlRoom():
    array = [[[101, 102, 103, 104, 105], [106, 107, 108, 109, 110]],
             [[201, 202], [203, 204], [205, 206], [207, 208], [209, 210]], [[301], [302], [303], [304], [305]]]

    pat = Patients.query.filter_by(status="Active").all()
    genroom1 = array[0][0]
    genroom2 = array[0][1]
    semiroom1 = array[1][0]
    semiroom2 = array[1][1]
    semiroom3 = array[1][2]
    semiroom4 = array[1][3]
    semiroom5 = array[1][4]
    singleroom1 = array[2][0]
    singleroom2 = array[2][1]
    singleroom3 = array[2][2]
    singleroom4 = array[2][3]
    singleroom5 = array[2][4]
    avl = [[genroom1] + [genroom2]] + [[semiroom1] + [semiroom2] + [semiroom3] + [semiroom4] + [semiroom5]] + [
        [singleroom1] + [singleroom2] + [singleroom3] + [singleroom4] + [singleroom5]]
    for p in pat:
        if p.tbed == "General":
            if p.assignBed < 106:
                try:
                    genroom1.remove(p.assignBed)
                except:
                    pass
            else:
                try:
                    genroom2.remove(p.assignBed)
                except ValueError:
                    pass
        elif p.tbed == "Semi":
            if p.assignBed == 201 or p.assignBed == 202:
                try:
                    semiroom1.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 203 or p.assignBed ==204:
                try:
                    semiroom2.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 205 or p.assignBed ==206:
                try:
                    semiroom3.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 207 or p.assignBed == 208 :
                try:
                    semiroom4.remove(p.assignBed)
                except ValueError:
                    pass
            else:
                try:
                    semiroom5.remove(p.assignBed)
                except ValueError:
                    pass
        elif p.tbed == "Single":
            if p.assignBed == 301:
                try:
                    singleroom1.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 302:
                try:
                    singleroom2.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 303:
                try:
                    singleroom3.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 304:
                try:
                    singleroom4.remove(p.assignBed)
                except ValueError:
                    pass
            elif p.assignBed == 305:
                try:
                    singleroom5.remove(p.assignBed)
                except ValueError:
                    pass

        else:
            return array

    return avl



# Gets the number of available rooms
def availRooms(index):
    array = [[[101, 102, 103, 104, 105], [106, 107, 108, 109, 110]],
             [[201, 202], [203, 204], [205, 206], [207, 208], [209, 210]], [[301], [302], [303], [304], [305]]]
    pat = Patients.query.filter_by(status="Active").all()
    avl = 0
    if index == "General":
        a = 0
        for p in pat:
            if p.tbed == "General":
                a += 1
        avl = (len(array[0][0]) + len(array[0][1])) - a
    elif index == "Semi":
        b = 0
        for p in pat:
            if p.tbed == "Semi":
                b += 1
        avl = (len(array[1]) * len(array[1][0])) - b

    elif index == "Single":
        c = 0
        for p in pat:
            if p.tbed == "Single":
                c += 1
        avl = (len(array[2]) * len(array[2][0])) - c

    return avl



#Dict for room pricing
room = {1: {"bed": 5 , "qty": 2, "cost": 2000}, 2: {"bed": 2, "qty": 5, "cost": 4000}, 3: {'bed': 1, 'qty': 5, "cost": 8000}}







# Additional Functions for room
def rooms():
    pat = Patients.query.filter_by(status="Active").all()
    a = 0
    b = 0
    c = 0
    for p in pat:
        if p.tbed == "General":
            a += 1
        elif p.tbed =="Semi":
            b += 1
        elif p.tbed == "Single":
            c += 1

    return {1: a, 2: b, 3: c}

# ROOM BILL
def roomBill(index, days):
    if days == None:
        days = 1
    if index == "General":
        bill = room[1]['cost'] * days
    elif index == "Semi":
        bill = room[2]['cost'] * days
    elif index == "Single":
        bill = room[3]['cost'] * days

    else:
        bill = 0

    return bill