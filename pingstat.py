import argparse
from time import sleep
from ping3 import ping
import sqlite3
import csv  

interval=10

def init_db():
    con = sqlite3.connect("tutorial.db")
    
    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists ping(t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, host varchar, time float NULL)")
    cur.execute("CREATE TABLE if not exists hosts_to_monitor(host varchar PRIMARY KEY)")
    cur.execute("CREATE TABLE if not exists settings(key varchar PRIMARY KEY)")

    con.commit()

    return con

def get_hosts(con):
    cur = con.cursor()
    res = cur.execute("SELECT host FROM hosts_to_monitor")
    return (h[0] for h in res.fetchall())

def run_ping(con):
    cur = con.cursor()
    
    while True:
        hosts = {host:ping(host) for host in get_hosts(con)}

        print(hosts)

        hosts_list = [(h,t) for h,t in hosts.items()]

        insert_query = f'INSERT INTO ping (host, time) VALUES (?, ?)'
        cur.executemany(insert_query, hosts_list)
        con.commit()
        
        sleep(interval)

def list_hosts(con):
    print('Hosts to monitor:')
    for host in get_hosts(con):
        print(f' - {host}')

def add_host(con, host):
    if host=='':
        print('please provide host. example: "pingstat.py add --host 127.0.0.1"')
        exit()
    cur = con.cursor()
    cur.execute(f"INSERT INTO hosts_to_monitor VALUES ('{host}')")
    con.commit()

def export(con, filename, host):
    if filename=='':
        print('please provide filename. example: pingstat.py export --file "res.csv" --host 127.0.0.1')
        exit()
    cur = con.cursor()
    query = 'SELECT t, host, time from ping'
    if host != '':
        query += f" WHERE host='{host}'"
    query += ' ORDER BY t asc'
    res = cur.execute(query)
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Timestamp', 'Host', 'ping time'])
        for row in res.fetchall():
            spamwriter.writerow(row)

def del_host(con,host):
    if host=='':
        print('please provide host. example: "pingstat.py del --host 127.0.0.1"')
        exit()
    cur = con.cursor()
    cur.execute(f"DELETE FROM hosts_to_monitor WHERE host='{host}'")
    con.commit()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['run', 'list', 'add', 'del', 'export'], help=''' 
Commands:
  - run - start ping process. example: `pingstat.py run`                                                             
  - list - display hosts to ping example: `pingstat.py list`                                                             
  - add - add host to monitor `--host` arg is mandatory . example: `pingstat.py add --host 127.0.0.1`                               
  - del - del host from monitor (no ping stat erase). `--host` arg is mandatory . example: `pingstat.py del --host 127.0.0.1`                   
  - export - save data into csv file. '--file' arg is mandatory, `--host` is optional filter. example: 'pingstat.py export --file 'res.csv' --host 127.0.0.1'
    ''')
    parser.add_argument('--host', default='', help='host to add, del or filter in export command')
    parser.add_argument('--file', default='', help='filename to write in export command') 
    args = parser.parse_args()

    con = init_db()
    if args.cmd == 'run':
        run_ping(con)
    elif args.cmd == 'list':
        list_hosts(con)
    elif args.cmd == 'add':
        add_host(con, args.host)
        list_hosts(con)
    elif args.cmd == 'del':
        del_host(con, args.host)
        list_hosts(con)
    elif args.cmd == 'export':
        export(con, args.file, args.host)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
