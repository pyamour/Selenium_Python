# -*- coding: utf-8 -*-
# conftest.py
import pytest

def pytest_collection_modifyitems(config, items):
    """ basing on mark scenario，run test case in order"""
    for item in items:
        scenarios = [
            marker for marker in item.own_markers
            if marker.name.startswith('scenario')
            and marker.name in config.option.markexpr
        ]
        if len(scenarios) == 1 and not item.get_closest_marker('run'):
           item.add_marker(pytest.mark.run(order=scenarios[0].args[0]))
