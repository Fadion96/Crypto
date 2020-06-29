for filename in $(ls test_*.bin)
do
	dieharder -a -g 201 -f $filename > result_${filename%.*} 
done;
