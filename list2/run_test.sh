for filename in $(ls test_64*)
do
	dieharder -a -g 201 -f $filename > result_${filename%.*} &
done;
