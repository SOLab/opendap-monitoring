from monitoring import *
from datetime import datetime
from pymongo import MongoClient


def insertMongo(connstr, coll, message):
    client = MongoClient(connstr)
    db = client.get_default_database()
    collection = db[coll]
    try:
        collection.insert(message)
    finally:
        client.close()


class failureAction(Action):

    def run(self, monitor, service, rule, runner):
        print service.state
        print rule.server
        print "fail %s" % (str(service.name))
        if service.state:
            message = {'name': str(service.name),
                       'server': str(rule.server),
                       'state': 'down',
                       'date': datetime.utcnow()}
            insertMongo(service.mongostr, service.coll, message)
        service.state = False


class successAction(Action):

    def run(self, monitor, service, rule, runner):
        print service.state
        print rule.server
        print "success %s" % (str(service.name))
        if not service.state:
            message = {'name': str(service.name),
                       'server': str(rule.server),
                       'state': 'up',
                       'date': datetime.utcnow()}
            insertMongo(service.mongostr, service.coll, message)
        service.state = True


class MyService(Service):

    def __init__(self, mongostr, coll, name=None,
                 monitor=(), actions={}, state=False):
        self.name = name
        self.rules = []
        self.runners = {}
        self.actions = {}
        self.mongostr = mongostr
        self.coll = coll
        self.state = state
        if not (type(monitor) in (tuple, list)):
            monitor = tuple([monitor])
        map(self.addRule, monitor)
        self.actions.update(actions)


class UrlMonitor():

    def __init__(self, urls, freqsec, timeoutsec, mongostr, coll):
        self.freqsec = freqsec
        self.timeoutmsec = timeoutsec * 1000
        self.services = []
        for site in urls:
            self.services.append(
                MyService(
                    mongostr=mongostr,
                    coll=coll,
                    name=site['name'],
                    monitor=(
                        HTTP(
                            HEAD=site['url'],
                            freq=Time.s(self.freqsec),
                            timeout=Time.ms(self.timeoutmsec),
                            fail=[failureAction()],
                            success=[successAction()]
                        )
                    ),
                )
            )

    def run(self):
        mon = Monitor()
        map(mon.addService, self.services)
        mon.run()
