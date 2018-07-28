
## Before run this server, mysql server should be running first, and the database market should be ok.

```buildoutcfg
$ mysql -u root -p
Enter password:****** 
$ mysql> create DATABASE market;
```

### Modify the db url string in run.py file

```buildoutcfg
os.environ["DATABASE_URL"] = 'mysql://root:password@localhost/market'
```

### run the program

```buildoutcfg
$ python3 run.py
```