#!/bin/bash

usage(){
	echo "Usage: modapk [apk] [new_apk] [options]"
	echo "Options: -r [file]: remove file in apk"
	echo "         -c [file]: create file in apk"
	echo "         -w [file] [content]: write into file"
}

if [ $# -eq 0 ]; then
	usage
	exit
fi

source_apk=

case $1 in 
	--help )	usage
			exit
			;;
	* )		source_apk=$1
esac
shift
dest_apk=$1
shift

unzip -q $source_apk -d apk_tmp
cd apk_tmp/

while [ "$1" != "" ]; do
	case $1 in
		-r ) 	shift
			rm -rf $1
			;;
		-c )	shift
			touch $1
			;;
		-w )	shift
			echo $2 > $1
			shift
			;;
		* )	usage
			exit
	esac
	shift
done

rm -rf META-INF

zip -q repack.apk -r *
echo "android" | jarsigner -keystore ../android.keystore -signedjar $dest_apk repack.apk 'androidkey'
mv $dest_apk ../
cd ..
rm -rf apk_tmp
