import daemon, signal, lockfile
import syslog

from data import CSV_FILE_PATH
from datetime import datetime
from kraken_crawler import start

context = daemon.DaemonContext(
    working_directory='/var/lib/crawler',
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/kraken_crawler.pid')
)

market_data=open(CSV_FILE_PATH, 'a+')
context.files_preserve = [market_data]

context.open()

with context:
	syslog.syslog("Starting Daemon..")
	try:
		start()
	except:
		syslog("Daemon terminated")
