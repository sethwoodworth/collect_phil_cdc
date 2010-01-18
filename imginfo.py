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
# needs PIL

pics = []
size = []
format = []
mode = []

def imginfo(dirlist):
	for dir in dirlist:
		items_in_dir = os.listdir(dir)
        # makes a list of the items in dir, a word in dirlist
		for item in items_in_dir:
			pathtoitem=dir+'/'+item
            # defines pathtoitem as a direction to a 
			if os.path.isfile(pathtoitem):
				try:
					Image.open(pathtoitem)
                    # checks to see if the file located at pathtoitem is an image by attempting to open it with PIL
					pics.append(pathtoitem)
                    # if it's an image, append the path to the 'pics' list
				except IOError:
					print "item located at " + pathtoitem + " is unopenable by PIL"
			else:
				pathtoitem=dir+'/'+item
				dirlist.append(pathtoitem)
	for pic in pics:
		im = Image.open(pic)
		size.append(list(im.size))
		format.append(im.format)
		mode.append(im.mode)
	array = [ pics, size, format, mode ]
	return array

if __name__ == "__main__":
	dirlist = ['/tmp/pics']
	print imginfo(dirlist)
