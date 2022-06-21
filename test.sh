set -e
container=aytempler_test
image=aytempler:test
echo log > test.sh.log

docker build -t $image  . >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
echo run tests
docker run --name $container $image
docker logs $container >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
echo try install commands
docker run --entrypoint "/bin/bash" --name $container $image -c "pip install . && REPL=success aytemplar -i tests/test_aytempler_data/alternative_output_file_in.txt -o out.txt && cat out.txt"
docker logs $container >> test.sh.log 2>&1
docker rm -f $container >> test.sh.log 2>&1 || true
