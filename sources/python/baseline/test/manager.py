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
            'storage-default-testbaselineconf'
        )

        self.manager = Baseline()
        self.manager[Baseline.BASELINE_STORAGE] = self.baseline_storage
        self.manager[Baseline.BASELINECONF_STORAGE] = self.baselineconf_storage

        self.config_storage.put_element(
            element={
                "_id": "truc",
                "resource": "test",
                "period": 60,
                "value": null,
                "entity": "test",
                "baseline_name": "truc",
                "mode": "floatting",
                "margin": 0
            }
        )

    def tearDown(self):
        self.alarm_storage.remove_elements()


class TestManager(BaseTest):

    def test_get_baselines(self):
        raise NotImplementedError

    def test_add_baseline_conf(self):
        raise NotImplementedError

    def test_put(self):
        raise NotImplementedError

    def test_manage_baselines_list(self):
        raise NotImplementedError

    def test_beat(self):
        raise NotImplementedError

    def test_reset_timestamp(self):
        raise NotImplementedError

    def test_check_baseline(self):
        raise NotImplementedError


if __name__ == '__main__':
    main()
