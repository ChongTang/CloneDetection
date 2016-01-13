rm -rf patch_tmp2/*

for file in $(ls -p ../../../splitedFiles/*.java | grep -v /) #| head  -800)
do
cp ../../../splitedFiles/$file ./patch_tmp2/
done
