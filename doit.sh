> results.md
for x in $(seq 109)
do
  pic=$(printf "%03d" $x)
  descr=$(cat out/$pic.txt | jq ".description.captions[0].text")
  c=$(cat out/$pic.txt | jq ".description.captions[0].confidence")
  confidence=$(printf "%.0f" $(echo "$c * 100" | bc -l))
  tags=$(cat out/$pic.txt | jq ".description.tags" | tr -d '[' | tr -d ']' | tr -d '\n')
  if [ "$descr" = "null" ]
  then
    descr="no clue"
  fi

  echo "### $pic" >> results.md
  echo "![](bbt_$pic.png)  " >> results.md
  echo "**Description:** $descr  " >> results.md
  echo "**Tags:** $tags  " >> results.md
  echo "**Confidence:** $confidence %  " >> results.md  
done
