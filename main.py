from logger import UrlMonitor

if __name__ == '__main__':
    freqsec = 60
    timeoutsec = 10
    mongostr = 'mongodb://10.172.0.196:27017/odyssey'
    collection = 'opendap-logs'
    urls = [
        {'name': 'naiad-srv0',
         'url': 'http://naiad-srv0.solab.rshu.ru:8085/opendap/'},
        {'name': 'naiad-srv2',
         'url': 'http://naiad-srv2.solab.rshu.ru:8080/opendap/'},
        {'name': 'naiad-srv3',
         'url': 'http://naiad-srv3.solab.rshu.ru:8080/opendap/'},
        {'name': 'naiad-srv4',
         'url': 'http://naiad-srv4.solab.rshu.ru:8080/opendap/'},
        {'name': 'naiad-srv5',
         'url': 'http://naiad-srv5.solab.rshu.ru:8080/opendap/'},
    ]

    a = UrlMonitor(urls, freqsec, timeoutsec, mongostr, collection)
    a.run()
