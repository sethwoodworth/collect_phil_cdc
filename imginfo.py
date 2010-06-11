################################################################################
##################    ###  ###   ###########    ###  ###   #####################
################## ## ## ## ## ## ########## ## ## ## ## ## ####################
################## # ### ## ## ## ########## # ### ## ## ## ####################
################## ## ###  ###   ########### ## ###  ###   #####################
################################################################################
##                                                                            ##  
##          Copyright 2010 Ian Daniher <exploding.mind@gmail.com>             ##
##                                                                            ##
##                  Licensed under the GPLv3 or later,                        ##
##                  see PERMISSION for copying permission                     ##
##                  and COPYING for the GPL License                           ##
##                                                                            ##
################################################################################
################################################################################
                                                                   
import os, re
import Image
import Queue
# needs PIL

pics = []
size = []
format = []
mode = []
images_dir = 'data/hires/'

def imginfo(dir):
    dir_queue = Queue.Queue(0)
    dir_queue.put(dir)
#    while not dir_queue.empty():
    while True:
        dir = dir_queue.get()
        print 'dir: ' + dir
        items_in_dir = os.listdir(dir)
        # makes a list of the items in dir, a word in dirlist
        for item in items_in_dir:
            pathtoitem=dir+'/'+item
            # defines pathtoitem as a direction to a 
            if os.path.isfile(pathtoitem):
                print pathtoitem
                try:
                    Image.open(pathtoitem)
                    # checks to see if the file located at pathtoitem is an image by attempting to open it with PIL
                    pics.append(pathtoitem)
                    # if it's an image, append the path to the 'pics' list
                except IOError:
                    print "item located at " + pathtoitem + " is unopenable by PIL"
                except:
                    print "something terrible and unexpected has happened. run for your life."
            # if we're looking at a dir:
            else:
                pathtoitem=dir+'/'+item
                print pathtoitem
                dir_queue.put(pathtoitem)
                import pdb; pdb.set_trace()
	for pic in pics:
		im = Image.open(pic)
		size.append(list(im.size))
		format.append(im.format)
		mode.append(im.mode)
	array = [ pics, size, format, mode ]
	return array

if __name__ == "__main__":
	print imginfo(images_dir)
