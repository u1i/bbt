for x in $(seq 109)
do
  pic=$(printf "%03d" $x)
  ./analyze.sh https://raw.githubusercontent.com/u1i/bbt/master/bbt_${pic}.png > out/$pic.txt
done
