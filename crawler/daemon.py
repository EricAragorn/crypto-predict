import daemon, signal, lockfile

from crawler.kraken_crawler import start

context = daemon.DaemonContext(
    pidfile=lockfile.FileLock("/var/run/kraken_crawler.pid")
)

market_data=open('../data/market_data.csv', 'a+')
context.files_preserve = [market_data]

with context:
    start()
