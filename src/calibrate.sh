
fuser -k 5055/tcp
nohup python3 Main.py &
sleep 10
pushd Script
python3 Send.py calibrate &
popd
