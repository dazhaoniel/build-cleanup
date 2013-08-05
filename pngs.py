# Check usage of .png files in Drawable folders, selector .xml and layout .xml files
# Author: Daniel ZHAO
# Last Update: Aug 5, 2013
# Accepts two command, first a target directory for output file, second specify (true or false) whether you want delete unused files :)
# command line prompt example: [python scriptname.py ./ true]

import os
import sys
import re

# Global Variables
# For drawables
# png_list = [] # drawable file names list
# png_not_in_use = [] # not used drawable names 
# drawable_dir = [] # drawable-/ desnsity directory paths, ie drawable-xxhdpi/

# # For selectors
# selector_dir = [] # file path of selectors inside drawable/
# selector_file_path = [] # file with selectors: layout files and styles.xml
# selector_list = [] # a list of file names of selectors
# selector_not_use = []

# # For layouts
# layout_dir = []
# layout_list = [] # layout file name list
# layout_file_list = [] # everything in res/layout and src/
# layout_not_use = []

drawabledict = {}
layoutdict = {}
srcdict = {} # everything under src/ with styles.xml and Manifest files
selectordict = {}
drawables = set() # a set of drawables (unique, .png files)


def checkDrawables(f, pngs, path_drawable):

	for root, dirs, files in os.walk( path_drawable ):
		for filename in files:
			if (filename != '.DS_Store'):
				pngs.append( filename )


def scanLayout( filelist, layoutlist ):
	EXIST = False

	for layout in layoutlist:
		for filename in filelist:
			EXIST = readLayout( filename, layout )
			if EXIST == True:
				break
		else:
			layout_not_use.append( layout )

def scanSelectors( filelist, selectorlist):
	EXIST = False
	for selector in selectorlist:
		for filename in filelist:
			EXIST = readSelector( filename, selector )
			if EXIST == True:
				break
		else:
			if selector not in selector_not_use:
				selector_not_use.append( selector )

def scanDrawables( filelist, drawablelist ):
	# infos = []
	EXIST = False

	for drawable in drawablelist:
		dname = drawable.partition('.')[0]
		for filename in filelist:
			EXIST = readDrawable( filename, dname )
			if EXIST == True:
				break
		else:
			if ( drawable not in png_not_in_use):
				png_not_in_use.append( drawable )


def startProcess( rootdir ):
	filedir = rootdir + '/'

	# Get directory list within the root directory
	for root, dirs, files in os.walk(filedir):
		for fname in files:
			# file_path = os.path.join(root, fname)
			if ( fname.find('.DS_Store') != -1 ):
				continue
			
			if (root.find('libs') != -1 or root.find('gen') != -1 or root.find('out') != -1 or root.find('.svn') != -1 ):
				continue
			
			# if ( root.find('drawable-') == -1 ):
			# 	if ( fname == 'AndroidManifest.xml') or ( fname == 'AndroidManifestTemplate.xml') or (root.find('res') != -1):
			# 		if ( file_path not in filepaths):
			# 			filepaths.append( file_path )

			if ( root.find('src') != -1 or fname.find('styles') != -1 or fname.find('Manifest') != -1 ):
				srcdict[ ( fname, os.path.join(root, fname) ) ] = False

					# layout_file_list.append( file_path )
					# selector_file_path.append( file_path )
			if ( root.find('drawable') != -1 ):
				if ( root.find('drawable-') != -1 ):
					drawabledict[ ( fname, os.path.join(root, fname) ) ] = False
					drawables.add( fname )
				else:
					selectordict[ ( fname, os.path.join(root, fname) ) ] = False
			# 	if ( root.find('drawable') != -1 ):
			# 		f = open(file_path, 'r')
			# 		fcontent = f.read()
			# 		regexMatching = re.findall('<selector', fcontent)
			# 		if len(regexMatching) > 0:
			# 			f.close()
			# 			if root not in selector_dir:
			# 				selector_dir.append( root )
			# 			selector_file_path.append( file_path )
			# 			selector_list.append( fname )
			
			# if ( root.find('res/drawable-') != -1 ) and ( fname not in png_list ):
			# 	png_list.append(fname)
			# 	if ( root not in drawable_dir ):
			# 		drawable_dir.append(root)
			
			if ( root.find('res/layout') != -1 ):
				layoutdict[ ( fname, os.path.join(root, fname) ) ] = False


			# if ( root.find('values') != -1 ):
			# 	if (fname == 'styles.xml'):
			# 		selector_file_path.append ( file_path )

			# filedict[ ( fname, os.path.join(root, fname) ) ] = False


def readDrawable(filename, pname):
	FILE_FOUND = False

	f = open(filename, 'r')
	fcontent = f.read()
	regexMatching = re.findall(pname, fcontent)
	if len(regexMatching) > 0:
		f.close()
		return True
	return False


def readSelector(filename, pname):
	FILE_FOUND = False
	d_selector = 'drawable/' + pname.partition('.')[0]
	r_selector = 'R.drawable.' + pname.partition('.')[0]

	f = open(filename, 'r')
	fcontent = f.read()
	layoutMatching = re.findall( d_selector, fcontent)
	srcMatching = re.findall( r_selector, fcontent)
	if len(layoutMatching) > 0 or len(srcMatching) > 0:
		f.close()
		return True
	return False


def readLayout( filename, lname):
	FILE_FOUND = False
	r_layout = 'R.layout.'+ lname.partition('.')[0]
	r_include = '@layout/'+ lname.partition('.')[0]

	f = open(filename, 'r')
	fcontent = f.read()
	layoutMatching = re.findall(r_layout, fcontent)
	includeMatching = re.findall(r_include, fcontent)
	if len(layoutMatching) > 0 or len(includeMatching) > 0:
		f.close()
		return True
	return False


def fileDelete(f):
	print '\n=========== Removing Drawables =========='
	f.write('\n\n=========== Removing Drawables ==========\n')

	for drawabledir in drawable_dir:
		for root, dirs, files in os.walk( drawabledir ):
			for fname in files:
				if fname in png_not_in_use:
					os.remove( os.path.join(root, fname) )
					print os.path.join(root, fname) + ' -- removed'
					f.write( os.path.join(root, fname) + ' -- removed\n')

	print '\n=========== Removing Selectors =========='
	f.write('\n\n=========== Removing Selectors ==========\n')

	for selectordir in selector_dir:
		for root, dirs, files in os.walk( selectordir ):
			for fname in files:
				if fname in selector_not_use:
					os.remove( os.path.join(root, fname) )
					print os.path.join(root, fname) + ' -- removed'
					f.write( os.path.join(root, fname) + ' -- removed\n')

	print '\n=========== Removing Layouts =========='
	f.write('\n\n=========== Removing Layouts ==========\n')
	# print layout_not_use
	for layoutdir in layout_dir:
		# print layoutdir
		for root, dirs, files in os.walk( layoutdir ):
			for fname in files:
				if fname in layout_not_use:
					# print fname
					os.remove( os.path.join(root, fname) )
					print os.path.join(root, fname) + ' -- removed'
					f.write( os.path.join(root, fname) + ' -- removed\n')

	return



def main(argv):

	rootdir = 'negotiator_dev_repo'
	# for current working directory, use os.getcwd()

	# python bouncer.py ./ true
	if ( len(argv) == 3 ): 
		outputdir = argv[1]
		shouldDelete = argv[2]
	
	# python bouncer.py false
	if ( len(argv) == 2 ) and ( argv[1] == 'true' or argv[1] == 'false' ):
		outputdir = os.getcwd()
		shouldDelete = argv[1]
	
	# python bouncer.py ./
	if ( len(argv) == 1 ):
		outputdir = os.getcwd()
		shouldDelete = 'false'

	if (len(argv) == 2 and argv[1] != 'true' and argv[1] != 'false' ):
		outputdir = argv[1]
		shouldDelete = 'false'

	outputfile = os.path.join( outputdir, 'bouncer_results.txt' )
	f = open(outputfile, 'w')

	# Get a directory list
	startProcess(rootdir)
	# drawables = set( drawabledict.key[0] )
	# print len( drawables )

	# print '========== Layout =========='
	# f.write('========== Layout ==========\n')

	# scanLayout(layout_file_list, layout_list)
	# print 'Total layout files: ' + str(len(layout_list))
	# f.write( 'Total layout files: ' + str(len(layout_list)) + '\n')

	# print 'Total not used layout files: ' + str(len(layout_not_use) )
	# f.write('Total not used layout files: ' + str(len(layout_not_use) ) + '\n' )



	# print '\n========== Unused Layout =========='
	# f.write('\n========== Unused Layout ==========\n')
	
	# for fname in layout_list:
	# 	if fname in layout_not_use:
	# 		print fname
	# 		f.write( fname + '\n')


	# print '\n========== Selectors =========='
	# f.write('\n\n========== Selectors ==========\n')

	# scanSelectors(selector_file_path, selector_list)

	# print 'Total selectors: ' + str(len(selector_list))
	# f.write( 'Total selectors: ' + str(len(selector_list)) + '\n')

	# print 'Total not used selectors: ' + str(len(selector_not_use) )
	# f.write('Total not used selectors: ' + str(len(selector_not_use) ) + '\n' )


	# print '\n========== Unused Selectors =========='
	# f.write('\n========== Unused Selectors ==========\n')
	# for fname in selector_list:
	# 	if fname in selector_not_use:
	# 		print fname
	# 		f.write( fname + '\n')


	# print '\n========== Drawables =========='
	# f.write('\n\n========== Drawables ==========\n')

	# print 'Totals: ' + str(len(png_list))
	# f.write('Totals: ' + str(len(png_list)) + '\n')

	# scanDrawables(filepaths, png_list)
	
	# for png in png_not_in_use:
	# 	png_list.remove(png)

	# print '\nTotal Drawable counts (exclude unused): ', len(png_list)
	# f.write( 'Total Drawable counts (exclude unused): ' + str(len(png_list)) + '\n')

	# print '========== Drawables not in use: ' + str(len(png_not_in_use))+' ==========\n'
	# f.write('\n========== Drawables not in use: ' + str(len(png_not_in_use))+' ==========\n')

	# for unused in png_not_in_use:
	# 	print unused
	# 	f.write( unused + '\n')

	# for drawabledir in drawable_dir:
	# 	pngs_density = []
	# 	checkDrawables(f, pngs_density, drawabledir)

	# 	print '\n========== Missing from '+ drawabledir +' =========== '
	# 	f.write('\n\n========== Missing from '+ drawabledir +' ========== \n')

	# 	count = 0

	# 	for fname in png_list:
	# 		if fname not in pngs_density:
	# 			count += 1
	# 			print fname
	# 			f.write(fname + '\n')

	# 	print '( Total '+ str(count) +' )'
	# 	f.write('( Total '+ str(count) +' ) \n')


	# if ( shouldDelete == 'true'):
	# 	fileDelete(f)

	f.close()

if __name__ == '__main__':
	main(sys.argv)