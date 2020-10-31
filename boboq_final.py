# A very simple Flask Hello World app for you to get started with...
from main import Item, Bin, Packer
from flask import Flask


app = Flask(__name__)

packer = Packer()

def add_products(cart):
    for item in cart:
        for amount in range(int(item[-1])):
            packer.add_item(Item("[product]",float(item[0])/100,float(item[1])/100,float(item[2])/100,float(item[3])/100))

def minimum_palett_number(weight):
    est_units = weight/400
    # Decimal Check
    if est_units % 1 <= 0.375:
        return (int(est_units),1)
    else:
        return (int(est_units+1),0)



def addPalett(PalettTyp):
    if PalettTyp == 0:
        packer.add_bin(Bin('halfpalett', 0.6, 0.8, 1.8, 150))
        return
    packer.add_bin(Bin('ganzepalett', 1.2, 0.8, 2.0, 400))
    return

def addDifferentPaletts(palletDist):
    for fullPalett in range(palletDist[0]):
        addPalett(1)
    if palletDist[1] == 1:
        addPalett(0)
    return

def add_next_palett(palettDist):
    if palettDist[1] == 0:
        return (palettDist[0],1)
    else:
        return (palettDist[0]+1,0)


@app.route('/')
def hello_world():
    return '88'

@app.route('/<stre>')
def ret_string(stre):
    total_products_weight =  packer.get_total_weight()
    #print("total_weight" + str(total_products_weight))
    minimum_palett_numbers = minimum_palett_number(total_products_weight)
    addDifferentPaletts(minimum_palett_numbers)
    firstsplit = stre.split(";")
    cart = [x.split(",") for x in firstsplit]
    add_products(cart)
    packer.pack(bigger_first=True ,distribute_items=True)
    current_palett_dis = minimum_palett_numbers
    return str(current_palett_dis)
    while packer.bins[-1].unfitted_items != []:
        packer.clear_bins()
        current_palett_dis = add_next_palett(current_palett_dis)
        addDifferentPaletts(current_palett_dis)
        packer.pack(bigger_first=True,distribute_items=True)

#print("start")
#print(ret_string("32,27,25,15,5;37,37,20,12.8,5"))
#print("end")
