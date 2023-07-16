import os
import shutil
import subprocess

for root, dirs, files in os.walk( "./EXAMPLES" ):
	for file in files:
		if file.endswith( ".py" ):
			print( os.path.join( root , file ) )
			shutil.copy( os.path.join( root, file ) , "." )
			f = open( 'input_data.py' )
			line = f.readlines( )
			f.close()
			f = open( 'input_data.py' , 'w' )
			for i in range( 0 , len( line ) ):
				line_replaced = line[ i ].replace( '=' , ' ' )
				aux = line_replaced.split()
				if( len( aux ) > 0 ):
					if( aux[ 0 ] == 'cone_levels' ):
						line_cl = i
						f.writelines( 'cone_levels = 5 \n' )
					elif( aux[ 0 ] == 'N' ):
						line_N = i
						f.writelines( 'N = 10 \n' )
					else:
						f.writelines( line[ i ] )
			f.close()			
			os.system( "python3 ECMapProb.py" )
			
