import glob,os,sys
import numpy as np
import sys

#change this to the path of the data output   
folder='/home/pchamber/Tracer/src/output/'

#you can glue one case or multi-cases at the same time, 'DIMES_0001' etc. are casenames
def glue(casename,npts):

    #specify particle numbers and case numbers (the NPP value in the namelist) here:
    npp=1

    #you don't need to change the following.
    varn=['XYZ','MLD','TSG','GRAD']
    nn = [3,1,4,4]

    for i in range(1,npp+1):
        # casename='%s_%04i'%(cn,i)
        for iv,var in enumerate(varn):
            fns=sorted(glob.glob(folder+casename+'_0001.'+var+'*'))
            print folder+casename+'.'+var
            print casename,var,"total %i files"%len(fns)
            f=open('/home/pchamber/Tracer/upload/filenames_%s'%casename,'w')
            n=nn[iv]
            print 'this is the variable fns ', fns
            d=np.fromfile(fns[0],'>f4')
            print d.shape,n
            d=d.reshape(n,npts)
            nxy,nopt=d.shape
            del d
            t0=fns[0].split('.')[-2]
            t1=fns[-1].split('.')[-2]
            print t0,t1
            print casename
            dds=np.memmap('/home/pchamber/Tracer/upload/'+casename+'.%s.%s.%s.data'%(var,t0,t1),dtype='>f4',shape=(len(fns),n,nopt),mode='write')
            for i in range(len(fns)):
                d=np.fromfile(fns[i],'>f4').reshape(n,-1)
                print d
                f.writelines(fns[i])
                dds[i,...]=d
                del d
            f.close()
            del dds,

