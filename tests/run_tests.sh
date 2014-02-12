#/bin/bash
echo "RUNNING TESTS"

run="../src/run.py"
count=0

cat tests | while read test; do
  count=$((count+1))
  echo -ne "\e[39mTest $count: "
  oracle=$(eval $run $test)
  if [ $oracle -eq 1 ]; then
    echo -e "\e[32mPASS"
  else
    echo -e "\e[31mFAIL"
  fi
done

echo -e "\e[39mFINISHED"
