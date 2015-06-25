# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 14:28:47 2015

@author: jingpeng
"""
import numpy as np
import matplotlib.pylab as plt

class CompareVol:
    def __init__(self, v1, v2, cmap='gray'):
        self.v1 = v1
        self.v2 = v2
        self.Nz = min(v1.shape[0], v2.shape[0])
        self.z = 0
        self.cmap = cmap
        
    def __show_slice(self):
        self.ax1.images.pop()
        self.ax1.imshow(self.v1[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax1.set_xlabel( 'first volume: slice {}'.format(self.z) )

        self.ax2.images.pop()
        self.ax2.imshow(self.v2[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax2.set_xlabel( 'second volume: slice {}'.format(self.z) )
        self.fig.canvas.draw()
        
    def __press(self, event):
#        print 'press ' + event.key
        if 'down' in event.key and self.z<self.Nz:
            self.z+=1            
        elif 'up' in event.key and self.z>-self.Nz:
            self.z-=1
        self.__show_slice()        
        
    def vol_compare_slice(self):   
        self.fig, (self.ax1, self.ax2) = plt.subplots(1,2, sharey=True)
        self.fig.canvas.mpl_connect('key_press_event', self.__press)
        self.ax1.imshow(self.v1[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax1.set_xlabel( 'first  volume: slice {}'.format(self.z) )
        self.ax2.imshow(self.v2[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax2.set_xlabel( 'second volume: slice {}'.format(self.z) )
	plt.show()
    
class VolSlider:
    def __init__(self, fname, cmap='gray'):
        if ".h5" in fname or ".hdf5" in fname:
            import h5py
            f = h5py.File(fname)
            self.v1 = f['/main']
            if len(f['/main'].dims) == 3:
                self.Nz = self.v1.dims[0]
            elif len(f['/main'].dims) == 4:
                self.Nz = self.v1.dims[1]
            else:
                raise RuntimeError('invalid input matrix dimension')
        else:
            import emirt.io
            self.v1 = emirt.io.imread( fname )
            self.Nz = self.v1.shape[0]
        self.z = 0
        self.cmap = cmap
        
    def __show_slice(self):
        self.ax1.images.pop()
        if len(self.v1.dims) == 3:
            self.ax1.imshow(self.v1[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        else:
            self.ax1.imshow(self.v1[0,self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax1.set_xlabel( 'first volume: slice {}'.format(self.z) )
        self.fig.canvas.draw()
        
    def __press(self, event):
#        print 'press ' + event.key
        if 'down' in event.key and self.z<self.Nz:
            self.z+=1            
        elif 'up' in event.key and self.z>-self.Nz:
            self.z-=1
        self.__show_slice()        
        
    def show(self):   
        self.fig, self.ax1 = plt.subplots(1,1)
        self.fig.canvas.mpl_connect('key_press_event', self.__press)
        if len(self.v1.dims) == 3:
            self.ax1.imshow(self.v1[self.z,:,:], interpolation='nearest', cmap=self.cmap)
        else:
            self.ax1.imshow(self.v1[0,self.z,:,:], interpolation='nearest', cmap=self.cmap)
        self.ax1.set_xlabel( 'first  volume: slice {}'.format(self.z) )

def mat_show(mat, xlabel=''):
    import matplotlib.pylab as plt   
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.matshow(mat, cmap=plt.cm.gray_r)    
    # add numbers
    Nx, Ny = mat.shape
    x,y = np.meshgrid(range(Nx), range(Ny))
    for i,j in zip(x.ravel(),y.ravel()):
        s = str( np.round(mat[i,j], decimals=2) )
        if mat[i,j]<np.mean(mat):
            ax1.annotate(s, xy=(i,j), ha='center', va='center')
        else:
            ax1.annotate(s, xy=(i,j), ha='center', va='center', color='white')
    ax1.set_xlabel(xlabel)
    plt.show()

def imshow(im):
    import matplotlib.pylab as plt
    plt.imshow(im)
    
# show the labeled image with random color
def random_color_show( im, mode='im' ):
    import matplotlib.pylab as plt
    import matplotlib.colors as mcolor
    # make a random color map, but the background should be black
    if 0==im.max():
        assert('the maximum label is 0!!')
    cmap_array = np.random.rand ( im.max(),3)
    cmap_array[0,:] = [0,0,0]   
    cmap=mcolor.ListedColormap( cmap_array )
    if mode=='im':
        plt.imshow(im, cmap= cmap )
    elif mode=='mat':
        # approximate the matshow for compatability of subplot
        nr, nc = im.shape
        extent = [-0.5, nc-0.5, nr-0.5, -0.5]
        plt.imshow(im, extent=extent, origin='upper',interpolation='nearest', cmap=cmap) 
#        plt.matshow(im, cmap=mcolor.ListedColormap( cmap_array ) )
    else:
        print 'unknown mode'

def progress(count, total, suffix=''):
    import sys
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
