## This file is part of Scapytain
## See http://www.secdev.org/projects/scapytain for more informations
## Copyright (C) Philippe Biondi <phil@secdev.org>
## This program is published under a GPLv2 license

import operator

class KeyMaker:
    def __init__(self, *args, **kargs):
        self.dct = kargs
        self.dct.update(dict([(x,operator.attrgetter(x)) for x in args]))
        self.default = None
        if args:
            self.default = operator.attrgetter(args[0])
    def __getitem__(self, item):
        return self.dct[item]
    def __contains__(self, item):
        return item in self.dct

    def getter_one(self,name):
        if name in self:
            return self[name]
        return self[self.default]

    def getter(self, name):
        if type(name) is str:
            sk = name.split(",")
            if sk:
                names,getters = zip(*[(x,self.getter_one(x)) for x in sk if x in self])
                return list(names),lambda x:tuple( g(x) for g in getters )
        return [],self.default
        


test_plans = KeyMaker("reference","name","description",
                      nbobj=lambda x:len(x.objectives))

objectives = KeyMaker("reference", "name", "priority", "applicable","description",
                       nbtests = lambda x:len(x.tests) )

test_means = KeyMaker("reference", "name","description",
                      image=lambda x:bool(x.image_mime))

campaigns = KeyMaker("reference", "name", "description",
                     nbtp=lambda x:len(x.test_plan))

campaign_runs = KeyMaker("reference", "name", "description",
                         nblaunched=lambda x:len(x.results))

tests = KeyMaker("reference","name","description",
               version=lambda x:len(x.tests))

