#java -cp . splitPatches
#cd /if7/ct4ew/research/ray/project/RepertoireTool/cmdLine/src
#rm -rf ../runtime/results/linux_patches/*
#rm -rf linux_patches/*
#cd /if7/ct4ew/research/ray/project/splitedLinuxPatches
#for file in /if7/ct4ew/research/ray/project/splitedLinuxPatches/*.c
# $(ls -p *.c | grep -v /) | head  -800)
#do
#cp $file patch_linux1/
#done
#cp /if7/ct4ew/research/ray/project/splitedLinuxPatches/*.c patch_linux1/
#cd /if7/ct4ew/research/ray/project/RepertoireTool/cmdLine/src
rm -rf ../runtime/results/LinuxPatches2014_new/*
./Repertoire.py -d ../runtime/LinuxPatches2014_new -o ../runtime/results  > ../runtime/LinuxPatches2014_new.log
#./test.py > linux
