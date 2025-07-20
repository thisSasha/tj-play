CLIENT_PATH='/home/sasha/.local/share/PrismLauncher/instances/TJ Play/minecraft'
cp -r "$CLIENT_PATH/mods/" ./client/
ls "$CLIENT_PATH/mods/" > ./client/mods/.filelist
cp -r "$CLIENT_PATH/resourcepacks/" ./client/
ls "$CLIENT_PATH/resourcepacks/" > ./client/resourcepacks/.filelist
cp -r "$CLIENT_PATH/options.txt" ./client/
