import PIL
from PIL import Image
import sys
import random
import function

def evalrange(fxn,start,stop,step):
    x=start
    input = []
    output = []
    while x<stop:
        input.append(x)
        output.append(fxn.evaluate(x=x))
        x+=step
    return input,output
    
def drawline(img,x1,y1,x2,y2):
    if x1>x2:
        drawline(img,x2,y2,x1,y1)
        return
    dx = x2-x1
    if dx == 0:
        return
    dy = y2-y1
    step = dy/dx
    while x1 < x2:
        img[x1,y1]=(0)
        x1+=1
        y1+=step

def normalize(x,y,left,right,top,bottom):
    xrange=right-left
    yrange=top-bottom
    outdata=[]
    for x,y in zip(x,y):
        x=(x-left)/xrange
        y=(y-bottom)/yrange
        outdata.append((x,y))
    return outdata

class grf:
    def __init__(self,filename='graph.grf'):
        self.data={}
        with open(filename,'r') as gf:
            for line in gf:
                sp = line.split('=')
                if len(sp) != 2:
                    pass
                self.data[sp[0]]=sp[1]
        self.exp = self.data['exp']
        self.var = self.data['variable']
        self.left = float(self.data['left'])
        self.right = float(self.data['right'])
        self.top = float(self.data['top'])
        self.bottom = float(self.data['bottom'])
        self.step = float(self.data['step'])
        self.dims = self.data['dims'].split(',')
        self.dims = (int(self.dims[0]),int(self.dims[1]))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('usage: {} image grf\n'.format(sys.argv[0]))
        sys.exit(1)
    
    graph = grf(sys.argv[2])
    
    fxn = function.math_function(graph.exp[:-1])
    print(fxn)

    x,y = evalrange(fxn,graph.left,graph.right,graph.step)
    with open('data.csv','w') as wdata:
        wdata.write('x,y,\n')
        for item in zip(x,y):
            wdata.write('{},{},\n'.format(*item))
    data = normalize(x,y,graph.left,graph.right,graph.top,graph.bottom)


    dstimg = Image.new('L',graph.dims,'white')
    dstpixels = dstimg.load()

    for point in data:
        if point[1] >= 1 or point[1] <= 0:
            continue
        
        x = int(graph.dims[0]*point[0])
        y = (graph.dims[1]-1)-int((graph.dims[1]-1)*point[1])
        dstpixels[x,y]=(0)
    dstimg.save(sys.argv[1])
