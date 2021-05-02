FILE=$1

echo "Writing to $FILE" | tee $FILE

i=0
until [ $i -gt 9 ]
do
  dataFile="examples/tipping/data/generatedData15r/simulation$i.txt"
  echo "\n\nInferring from $dataFile..." | tee -a $FILE
  webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data $dataFile >> $FILE

  ((i++))
done
echo "Done"