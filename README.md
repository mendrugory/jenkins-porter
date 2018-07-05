# Jenkins Porter

Tool which will help you to save your jenkins job configuration, restore them, remove them all or directly copy between Jenkins servers.

## Save

```shell
$ python3 jenkins-porter.py save -o <origin server> -uo <origin user> -po <origin password> -f <destination folder>
```

The destination folder does not have to exist.

## Restore

```shell
$ python3 jenkins-porter.py restore -t <target server> -ut <target user> -pt <target password> -f <destination folder>
```

## Copy

```shell
$ python3 jenkins-porter.py copy -o <origin server> -uo <origin user> -po <origin password> -t <target server> -ut <target user> -pt <target password>
```

## Clean

```shell
$ python3 jenkins-porter.py clean -t <target server> -ut <target user> -pt <target password>
```