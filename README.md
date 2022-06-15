# ayTempler
A tool to replace annotated keys with their values from the environemnt as a sort of template replacement.

# motivation
The only templating customize supports is through an implementation loophole in config maps.
If for some reason templating is required there sould be an easy way to specify it for yi cd purposes.

# test
Run ```./test.sh``` to run the dockerized pipeline.
Use ```watch -n 0.1 ./test.sh``` to watch out while developing

# usage 

```python ayTempler.py [-h] -i INPUT [-o OUTPUT] [-b BLACKLIST] [-w WHITELIST]``` 

## examples

```python ayTempler.py -i kustomize.yaml``` - replaces a kustomize.yaml in place. Everything that matches a template like ```${NAME}``` will be replaced with the value for the corresponding ```NAME``` key in the environment.

```python ayTempler.py -i kustomize.template -o kustomize.yaml``` - instead of replacing in place this command will create a new file.

```python ayTempler.py -i kustomize.yaml -b FOO -b BAR -b BAZ"``` - blacklist ```${FOO}```, ```${BAR}``` and ```${BAZ}``` so they are not repalced

```python ayTempler.py -i kustomize.yaml -w UHH -w BAZ"``` - whitelist ```${UHH}``` and ```${BAZ}``` so only these variables are candidates for replacement

## options

[-h] shows a help message, -i INPUT specifies the input file for in place replacement, [-o OUTPUT] specifies the output file as an alternative to in place replacement, [-b BLACKLIST] allows to blacklist env names that should not be replaced, incompatible with whitelist, [-w WHITELIST] restricts replaceemnt to the selected list, incompatible with blacklist
