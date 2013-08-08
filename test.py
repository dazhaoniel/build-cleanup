# Check usage of .png files in Drawable folders, selector .xml and layout .xml files
# Author: Daniel ZHAO
# Last Update: Aug 8, 2013
# Accepts two command, first a target directory for output file, second specify (true or false) whether you want delete unused files :)
# command line prompt example: [python scriptname.py ./ true]

import os
import sys
import re

# Global Variables
drawabledict = {}
drawablecheckdict = {} # additional, with menu/ etc.
layoutdict = {}
srcdict = {} # everything under src/ with styles.xml and Manifest files
selectordict = {}

drawableset = set() # a set of drawables (unique, .png files)
drawable_dir = set() # ie /res/drawable-xhdpi/
layoutset = set()
selectorset = set()

def scan_file( targetset, srclist, scanitem ):
	EXIST = False
	usedset = set()

	if scanitem == 'layout':
		for filename in targetset:
			for key, value in srclist.items():
				if value == False:
					EXIST = read_layout( key[1], filename )
					if EXIST == True:
						usedset.add( filename )
						break

	if scanitem == 'selector':
		for filename in targetset:
			for key, value in srclist.items():
				if value == False:
					EXIST = read_selector( key[1], filename )
					if EXIST == True:
						usedset.add( filename )
						break

	if scanitem == 'drawable':
		for filename in targetset:
			for key, value in srclist.items():
				if value == False:
					EXIST = read_drawable( key[1], filename )
					if EXIST == True:
						usedset.add( filename )
						break

	targetset.difference_update( usedset )


def update_dict( targetset, srcdict ):
	for key, value in srcdict.items():
		if key[0] in targetset:
			srcdict[ key ] = True


def start_process( rootdir ):
	filedir = rootdir + '/'

	# Get directory list within the root directory
	for root, dirs, files in os.walk(filedir):
		for fname in files:
			if ( fname.find('.DS_Store') != -1 ):
				continue
			
			if (root.find('libs') != -1 or root.find('gen') != -1 or root.find('/out') != -1 or root.find('.svn') != -1 ):
				continue

			if ( root.find('src') != -1 or fname.find('styles') != -1 or fname.find('Manifest') != -1 ):
				srcdict[ ( fname, os.path.join(root, fname) ) ] = False

			if ( root.find('layout') != -1 ):
				layoutdict[ ( fname, os.path.join(root, fname) ) ] = False
				layoutset.add( fname )

			if ( root.find('drawable') != -1 ):
				if ( root.find('drawable-') != -1 ):
					drawable_dir.add( root )
					drawabledict[ ( fname, os.path.join(root, fname) ) ] = False
					drawableset.add( fname )
				else:
					f = open(os.path.join(root, fname), 'r')
					fcontent = f.read()
					regexMatching = re.findall('<selector', fcontent)
					if len(regexMatching) > 0:
						f.close()
						selectordict[ ( fname, os.path.join(root, fname) ) ] = False
						selectorset.add( fname )

			if ( root.find('/res') != -1 and root.find('drawable-') == -1 ):
				key = ( fname, os.path.join(root, fname) )
				if key not in selectordict:
					drawablecheckdict[ ( fname, os.path.join(root, fname) ) ] = False


def read_drawable(filename, pname):
	f = open(filename, 'r')
	fcontent = f.read()
	regexMatching = re.findall(pname.partition('.')[0], fcontent)
	if len(regexMatching) > 0:
		f.close()
		return True
	return False


def read_selector(filename, pname):
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


def read_layout( filename, lname):
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


def file_delete(f, srcdict):
	for key, value in srcdict.items():
		if value == True:
			os.remove( key[1] )
			print key[1] + ' -- removed'
			f.write( key[1] + ' -- removed\n')
			del srcdict[key]
	return



def main(argv):

	rootdir = '../your_directory_name' # change to your directory name, without the / at the end
	# for current working directory, use os.getcwd()

	# python test.py ./ true
	if ( len(argv) == 3 ): 
		outputdir = argv[1]
		_delete = argv[2]
	
	# python test.py false
	if ( len(argv) == 2 ) and ( argv[1] == 'true' or argv[1] == 'false' ):
		outputdir = os.getcwd()
		_delete = argv[1]
	
	# python test.py ./
	if ( len(argv) == 1 ):
		outputdir = os.getcwd()
		_delete = 'false'

	if (len(argv) == 2 and argv[1] != 'true' and argv[1] != 'false' ):
		outputdir = argv[1]
		_delete = 'false'

	outputfile = os.path.join( outputdir, 'test_results.txt' )
	f = open(outputfile, 'w')

	# Get a directory list
	start_process(rootdir)

	print '========== Layout =========='
	f.write('========== Layout ==========\n')

	print 'Total layout files: ' + str(len(layoutset))
	f.write( 'Total layout files: ' + str(len(layoutset)) + '\n')

	scan_file( layoutset, srcdict, 'layout' )
	scan_file( layoutset, layoutdict, 'layout' )
	update_dict( layoutset, layoutdict )

	print 'Total not used layout files: ' + str(len(layoutset) )
	f.write('Total not used layout files: ' + str(len(layoutset) ) + '\n' )

	print '\n========== Unused Layout =========='
	f.write('\n========== Unused Layout ==========\n')
	
	for key, value in layoutdict.items():
		if value == True:
			print key[0]
			f.write( key[0] + '\n')


	print '\n========== Selectors =========='
	f.write('\n\n========== Selectors ==========\n')

	print 'Total selectors: ' + str(len(selectorset))
	f.write( 'Total selectors: ' + str(len(selectorset)) + '\n')

	scan_file( selectorset, srcdict, 'selector' )
	scan_file( selectorset, layoutdict, 'selector' )
	scan_file( selectorset, selectordict, 'selector' )
	update_dict( selectorset, selectordict )

	print 'Total not used selectors: ' + str(len(selectorset) )
	f.write('Total not used selectors: ' + str(len(selectorset) ) + '\n' )


	print '\n========== Unused Selectors =========='
	f.write('\n========== Unused Selectors ==========\n')

	for key, value in selectordict.items():
		if value == True:
			print key[0]
			f.write( key[0] + '\n')


	print '\n========== Drawables =========='
	f.write('\n\n========== Drawables ==========\n')

	print 'Total drawables: ' + str(len(drawableset))
	f.write('Total drawables: ' + str(len(drawableset)) + '\n')

	useddrawable = set()
	useddrawable.update( drawableset )

	scan_file( drawableset, srcdict, 'drawable' )
	scan_file( drawableset, layoutdict, 'drawable' )
	scan_file( drawableset, selectordict, 'drawable' )
	scan_file( drawableset, drawablecheckdict, 'drawable' )
	update_dict( drawableset, drawabledict )

	useddrawable.difference_update( drawableset )

	print '\nTotal Drawable counts (exclude unused): ', len(useddrawable)
	f.write( 'Total Drawable counts (exclude unused): ' + str(len(useddrawable)) + '\n')

	print '========== Drawables not in use: ' + str(len(drawableset))+' ==========\n'
	f.write('\n========== Drawables not in use: ' + str(len(drawableset))+' ==========\n')

	for drawable in drawableset:
		print drawable
		f.write( drawable + '\n')

	for drawabledir in drawable_dir:

		print '\n========== Missing from '+ drawabledir +' =========== '
		f.write('\n\n========== Missing from '+ drawabledir +' ========== \n')

		missingdrawable = set()
		missingdrawable.update( useddrawable )

		for key, value in drawabledict.items():
			if ( value == False and key[1].find(drawabledir) != -1 ):
				if key[0] in missingdrawable:
					missingdrawable.remove( key[0] )

		for drawable in missingdrawable:
			print drawable
			f.write( drawable + '\n')

		print '( Total '+ str(len(missingdrawable)) +' )'
		f.write('( Total '+ str(len(missingdrawable)) +' ) \n')


	if ( _delete == 'true'):
		print '\n=========== Removing Layouts =========='
		f.write('\n\n=========== Removing Layouts ==========\n')
		file_delete(f, layoutdict)

		print '\n=========== Removing Selectors =========='
		f.write('\n\n=========== Removing Selectors ==========\n')
		file_delete(f, selectordict)

		print '\n=========== Removing Drawables =========='
		f.write('\n\n=========== Removing Drawables ==========\n')
		file_delete(f, drawabledict)

	f.close()

if __name__ == '__main__':
	main(sys.argv)