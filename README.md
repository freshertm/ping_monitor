# Ping monitor
Once you have to continuous monitor your connection to different hosts you have to use tool like this. This when run will ping hosts from your list each 10 seconds and write result into sqlite database. Once you need analyze collected data you can export into CSV. 


# Installation
```
pip install ping3
```


# Commands:
  - **run** - start ping process. example: `pingstat.py run`                                                             
  - **list** - display hosts to monitor. example: `pingstat.py list`                                                             
  - **add** - add host to monitor **--host** arg is mandatory, you can add IP or domain names. example: `pingstat.py add --host google.com`
  - **del** - del host from monitor (no ping stat erase). **--host** arg is mandatory. example: `pingstat.py del --host 127.0.0.1`                   
  - **export** - save data into csv file. **--file** arg is mandatory, **--host** is optional filter. example: 'pingstat.py export --file 'res.csv' --host 127.0.0.1'

# Gettings started
- Install packages as described in Installation section
- run `pingstat.py add --host 127.0.0.1` to create your own monitor list. 
- run  `pingstat.py run` to start monitor.
- When you need to get result run `pingstat.py export --file 'res.csv' --host 127.0.0.1`
- 
**Note:** all commands can be run in parallel. So you have not interrupt running monitor to export or change hosts list. When you add or remove host - changes applies immediately, no restart needed.
