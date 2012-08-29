import subprocess, shutil

lcommand = "bin/getLnumbers"
parfile = "data/matchyourcell_01.par"
genlfile = "lcoeffs.txt"

def process(input_filename, output_filename):
    print "Getting L numbers %s to %s" % (input_filename, output_filename)
    generate_l_coeffs(input_filename, input_filename, output_filename)

def generate_l_coeffs(of, sf, lf):
    runcommand = [lcommand, parfile, "tmp", of, sf, sf]

    print "Generating %s" % lf
    p = subprocess.Popen(runcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #TODO - Error handling
    o, se = p.communicate()

    #print se, so

    #print "From %s to %s" % (genlfile, lf)
    shutil.copy(genlfile, lf)
 
