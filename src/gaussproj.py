#!/usr/bin/env python2.7

import itertools, sys, os
import scipy
import scipy.ndimage as nd
import numpy as np
import stackhandle
import projpp

def numpy_draw_pyplot(r):
    plt.imshow(r, interpolation='nearest')
    plt.show()

def numpy_draw_pil(r):
    i = Image.fromarray(r)
    i.show()

def read_and_conv(filename):
    try:
        na = scipy.misc.imread(filename)
    except IOError, e:
        print "ERROR: couldn't open %s" % filename
        print e
        sys.exit(1)

    #TODO - nicer way of doing this

    try:
        x, y, z = na.shape
    except ValueError:
        return na

    return na[:,:,0]

def load_png_stack_pattern(impattern, istart, iend):
    flush_message("Loading images...")
    ifiles = [impattern % i for i in range(istart, iend)]
    ma = np.dstack(itertools.imap(read_and_conv, ifiles))
    print " done, array is", ma.shape
    return ma

def load_png_stack(ifiles):
    flush_message("Loading images...")
    ma = np.dstack(itertools.imap(read_and_conv, ifiles))
    print " done, array is", ma.shape
    return ma

def flush_message(message):
    print message,
    sys.stdout.flush()

def apply_gaussian_filter(ma, sd):
    flush_message("Applying 3D gaussian filter...")
    bl = nd.gaussian_filter(ma, sd)
    print " done"
    return bl

def get_max(bl, x, y):
    dp = list(bl[x, y, :])
    if not any(dp): return 255
    return dp.index(max(dp))

def find_projection_surface(bl):
    flush_message("Finding projection surface...")
    xmax, ymax, zmax = bl.shape
    surface = np.zeros([xmax, ymax], dtype=np.uint8)
    for x in range(0, xmax):
        for y in range(0, ymax):
            z = get_max(bl, x, y)
            surface[x, y] = z
    print " done"
    return surface

def vavg(ma, x, y, z):
    return 0.25 * sum(ma[x, y, z-3:z])

def projection_from_surface(ma, surface):
    flush_message("Generating projection from surface...")
    xmax, ymax, zmax = ma.shape
    res = np.zeros([xmax, ymax], dtype=np.uint8)
    #print xmax, ymax, zmax
    #sys.exit(0)
    for x in range(0, xmax):
        for y in range(0, ymax):
            z = min(surface[x, y], zmax-1)
            #res[x, y] = vavg(ma, x, y, z)
            res[x, y] = ma[x, y, z]
    print " done"
    return res

def save_numpy_as_png(filename, np):
    scipy.misc.imsave(filename, np)

def projection_from_file_list(ifiles, output_projection, output_surface, params):
    sdx, sdy, sdz = 3, 3, 0

    sds = 0

    ma = load_png_stack(ifiles)

    bl = apply_gaussian_filter(ma, [sdx, sdy, sdz])

    ps = find_projection_surface(bl)
    sps = nd.gaussian_filter(ps, sds)
    #sfilename = os.path.join(output_dir, "surface-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    sfilename = output_surface
    save_numpy_as_png(sfilename, sps)

    res = projection_from_surface(ma, sps)
    #filename = os.path.join(output_dir, "proj-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    filename = output_projection
    scipy.misc.imsave(filename, res)



def main():

    try:
        stackdir = sys.argv[1]
    except IndexError:
        print "Usage: %s stack_dir [output_dir] [sdx] [sdy] [sdz]" % os.path.basename(sys.argv[0])
        sys.exit(1)

    #imgpattern, istart, iend = stackhandle.get_stack_pattern(stackdir)
    ifiles = stackhandle.get_stack_files(stackdir)

    projection_from_file_list(ifiles)


    sys.exit(0)

    try:
        output_dir = sys.argv[2]
    except IndexError:
        output_dir = 'output/'
        print "Using default output directory output/"

    #impattern = 'data/pngstack/ExpID3002_spch4_TL003_plantD_lif_S000_T000_C000_Z0%02d.png'
    #istart = 0
    #iend = 92

    try:
        sdx, sdy, sdz = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    except IndexError:
        print "Using default values for standard deviation"
        sdx, sdy, sdz = 8, 8, 6

    sds = 10

    print "Using standard deviations: %d, %d, %d" % (sdx, sdy, sdz)

    #ma = load_png_stack(imgpattern, istart, iend)
    ma = load_png_stack(ifiles)

    bl = apply_gaussian_filter(ma, [sdx, sdy, sdz])

    ps = find_projection_surface(bl)
    sps = nd.gaussian_filter(ps, sds)
    sfilename = os.path.join(output_dir, "surface-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    save_numpy_as_png(sfilename, sps)

    res = projection_from_surface(ma, sps)
    filename = os.path.join(output_dir, "proj-g3d-%d-%d-%d-%d.png" % (sdx, sdy, sdz, sds))
    scipy.misc.imsave(filename, res)

    #flush_message("Post processing...")
    #pp = projpp.proj_filter(res, 3, 60, 15)
    #print " done"
    #filename = os.path.join(output_dir, 'proj-pp-%d-%d-%d-%d.png' % (sdx, sdy, sdz, sds))
    #scipy.misc.imsave(filename, pp)

    #numpy_draw_pil(res)

if __name__ == "__main__":
    main()
