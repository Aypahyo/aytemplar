# ayTempler
A tool to replace annotated keys with their values from the environemnt as a sort of template replacement.

# motivateion
The only templating customize supports is through an implementation loophole in config maps.
If for some reason templating is required there sould be an easy way to specify it for yi cd purposes.



# test
Run ```./test.sh``` to run the dockerized pipeline.
Use ```watch -n 0.1 ./test.sh``` to watch out while developing

# usage 

```python ayTempler.py [-h] -i INPUT [-o OUTPUT] [-b BLACKLIST] [-w WHITELIST]``` 

## examples

```python ayTempler.py -i kustomize.yaml``` will replace kustomize.yaml in place with template replacements for ${NAME} with the value of NAME in the environment.

```python ayTempler.py -i kustomize.template -o kustomize.yaml``` will create kustomize.yaml from the tempalte and replace everything it matches

```python ayTempler.py -i kustomize.yaml -b FOO -b BAR -b BAZ"``` will backlist and not replace ${FOO}, ${BAR}, ${BAZ} but it will replace ${UHH}

```python ayTempler.py -i kustomize.yaml -w UHH -w BAZ"``` will whitelist and replace ${UHH} and ${BAZ} but it will not replace ${FOO} and ${BAR}

## options

[-h] shows a help message, -i INPUT specifies the input file for in place replacement, [-o OUTPUT] specifies the output file as an alternative to in place replacement, [-b BLACKLIST] allows to blacklist env names that should not be replaced, incompatible with whitelist, [-w WHITELIST] restricts replaceemnt to the selected list, incompatible with blacklist