FILE=$1

echo 'Inferring from lowTipsConsistent.csv...' | tee $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data lowTipsConsistent.csv >> $FILE
echo 'Inferring from lowTipsInconsistent.csv...' | tee -a $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data lowTipsInconsistent.csv >> $FILE

echo 'Inferring from mediumTipsConsistent.csv...' | tee -a $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data mediumTipsConsistent.csv >> $FILE
echo 'Inferring from mediumTipsInconsistent.csv...' | tee -a $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data mediumTipsInconsistent.csv >> $FILE

echo 'Inferring from highTipsConsistent.csv...' | tee -a $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data highTipsConsistent.csv >> $FILE
echo 'Inferring from highTipsInconsistent.csv...' | tee -a $FILE
webppl examples/tipping/src/predicting.wppl --require . --require examples/tipping/ --require webppl-fs -- --data highTipsInconsistent.csv >> $FILE

echo "Finished. Results written to: $FILE" | tee -a $FILE
