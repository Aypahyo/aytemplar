set -e
container=aytempler_test
image=aytempler:test
echo log > test.sh.log

docker build -t $image  . >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
echo docker run --name $container $image
docker run --name $container $image
docker logs $container >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
