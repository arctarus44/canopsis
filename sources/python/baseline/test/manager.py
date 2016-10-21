from unittest import TestCase, main

from canopsis.middleware.core import Middleware
from canopsis.task.core import get_task

from canopsis.timeserie.timewindow import get_offset_timewindow
from canopsis.baseline.manager import Baseline


class BaseTest(TestCase):

    def setUp(self):
        self.baseline_storage = Middleware.get_middleware_by_uri(
            'storage-default-testbaseline://'
        )
        self.baselineconf_storage = Middleware.get_middleware_by_uri(
            'storage-default-testbaselineconf://'
        )

        self.manager = Baseline()
        self.manager[Baseline.STORAGE] = self.baseline_storage
        self.manager[Baseline.CONFSTORAGE] = self.baselineconf_storage

        self.baselineconf_storage.put_element(
            element={
                "_id": "truc",
                "resource": "test",
                "period": 60,
                "entity": "test",
                "baseline_name": "truc",
                "mode": "floatting",
                "margin": 0,
                "check_frequency": 'true',
                'value_name': 'cpu',
                'value': 12
            }
        )

    def tearDown(self):
        self.baselineconf_storage.remove_elements()


class TestManager(BaseTest):

    def test_get_baselines(self):
        #raise NotImplementedError
        pass

    def test_add_baseline_conf(self):
        #raise NotImplementedError
        pass

    def test_put(self):
        #raise NotImplementedError
        pass

    def test_manage_baselines_list(self):
        #raise NotImplementedError
        pass

    def test_beat(self):
        #raise NotImplementedError
        pass

    def test_reset_timestamp(self):
        #raise NotImplementedError
        pass

    def test_check_baseline(self):
        #raise NotImplementedError
        pass

    def test_value_sum(self):
       l = [[325131,1],[32131321312,2],[3215,3],[0,4],[6554,5],[654,6],[654546,0]]
       self.assertEqual(self.manager.values_sum(l), 21)

    def test_value_average(self):
       l = [[325131,1],[32131321312,2],[3215,3],[0,4],[6554,5],[654,6],[654546,0]]
       self.assertEqual(self.manager.value_average(l), 3)

    def test_value_max(self):
       l = [[325131,1],[32131321312,2],[3215,3],[0,4],[6554,5],[654,6],[654546,0]]
       self.assertEqual(self.manager.value_max(l), 6)

    def test_value_min(self):
       l = [[325131,1],[32131321312,2],[3215,3],[0,4],[6554,5],[654,6],[654546,0]]
       self.assertEqual(self.manager.value_min(l), 0)

    def test_aggregation(self):
       l = [[325131,1],[32131321312,2],[3215,3],[0,4],[6554,5],[654,6],[654546,0]]
       self.assertEqual(self.manager.aggregation(l,'sum'), 21)
       self.assertEqual(self.manager.aggregation(l,'min'), 0)
       self.assertEqual(self.manager.aggregation(l,'max'), 6)
       self.assertEqual(self.manager.aggregation(l,'average'), 3)

    def test_check_frequency(self):
        self.assertEqual(self.manager.check_frequency('truc'), True)

    def test_get_value_name(self):
        self.assertEqual(self.manager.get_value_name('truc'), 'cpu')

if __name__ == '__main__':
    main()
