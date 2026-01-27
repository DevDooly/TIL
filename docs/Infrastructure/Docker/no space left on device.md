# Docker Machine: No space left on device

## Cleanup

```
$ docker volume rm $(docker volume ls -qf dangling=true)
```

**Additional Commands:**

```
$ docker volume ls -qf dangling=true
```

**Check Volume list:**
```
$ docker volume ls
```

## Remove the unused Images
```
$ docker rmi $(docker images | grep "^<none>" | awk '{print $3}')
```
