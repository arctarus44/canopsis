# -*- coding: utf-8 -*-

from time import time

from canopsis.middleware.registry import MiddlewareRegistry

from canopsis.configuration.configurable.decorator import (
    add_category, conf_paths
)
from canopsis.timeserie.timewindow import get_offset_timewindow, TimeWindow
from canopsis.context.manager import Context


@conf_paths('baseline/baseline.conf')
@add_category('BASELINE')
class Baseline(MiddlewareRegistry):
    """Baseline"""

    STORAGE = 'baseline_storage'
    CONFSTORAGE = 'baselineconf_storage'
    CONTEXT_MANAGER = 'context'

    def __init__(self, *args, **kwargs):
        """__init__

        :param *args:
        :param **kwargs:
        """
        super(Baseline, self).__init__(*args, **kwargs)
        self.check = True

    def get_baselines(self, baseline_name, timewindow=None):
        """get_baselines"""
        if timewindow is None:

            _timewindow = TimeWindow(0, time())

        else:
            _timewindow = timewindow

        return self[Baseline.STORAGE].get(data_id=baseline_name, timewindow=_timewindow)

    def put(self, name, value):
        point = (time(), value)
        self[Baseline.STORAGE].put(data_id=name, points=[point])

    def add_baselineconf(
        self,
        baseline_name,
        mode,
        period,
        margin,
        entity,
        resource,
        value=None
    ):
        element = {
            'baseline_name': baseline_name,
            'mode': mode,
            'value': value,
            'period': period,
            'margin': margin,
            'entity': entity,
            'resource': resource
        }

        if self.check:
            if not len(self[Baseline.CONFSTORAGE].get_elements(query={'_id':'baselines'})) > 0:
                self[Baseline.CONFSTORAGE].put_element({'_id':'baselines', 'list':[]})
                self.check = False

        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id':'baselines'}):
            baselines = i

        l = baselines['list']
        l.append({baseline_name: time() + period})
        #revoir par ce que la on écrase pas mais on ajoute dans la liste bref c'est de la merde'
        baselines['list'] = l
        self[Baseline.CONFSTORAGE].put_element(baselines)
        return self[Baseline.CONFSTORAGE].put_element(element, _id=baseline_name)

    def beat(self):
        now = time()
        baselines = {}
        for i in self[Baseline.CONFSTORAGE].get_elements(query={'_id':'baselines'}):
            baselines = i
        baseline_list = baselines['list']

        for i in baseline_list:
            if now > i.items()[0][1]:
                self.logger.error('voila on est bon on doit checker')
        #continuer ici/revoir le check pour ensuite passer a check baseline et on sera pas mal




        """
        for baseline_name, timestamp in self.baselines.items():
            f = open('/home/tgosselin/fichierdelog3', 'a')
            f.write('for en beat\n')
            f.close()
            if now > timestamp:
                f = open('/home/tgosselin/fichierdelog3', 'a')
                f.write('on check !\n')
                f.close()
                self.check_baseline(baseline_name, timestamp)
            else:
                f = open('/home/tgosselin/fichierdelog3', 'a')
                f.write('on check pas encore \n')
                f.close()
                f = open('/home/tgosselin/fichierdelog3', 'a')
                f.write('fin du beat manager\n')
                f.close()
        """
    def check_baseline(self, baseline_name, timestamp):
        f = open('/home/tgosselin/fichierdelog3', 'a')
        f.write('check baseline\n')
        f.close()
        conf = self[Baseline.CONFSTORAGE].get_elements(
            query={"_id": baseline_name})
        baselineconf = {}

        for i in conf:
            baselineconf = i

        timewindow = TimeWindow(
            start=timestamp - conf['period'], stop=timestamp)
        """
        result = self.get_baselines(baseline_name, timewindow)

        f = open('/home/tgosselin/fichierdelog3', 'a')
        f.write('a{0}\n'.format(result))
        f.close()
        """
    # chopper la config de la baseline a checker dans mongo donc un petit get qui va bien
    # faire la requete des métrique a chopper en fonction de la config travailler le get avec la time window
    # déclencher l'alarme remettre le compteur a jour etc
