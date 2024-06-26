# mypy: allow-untyped-defs
from __future__ import annotations

import warnings

import pytest


def func(msg):
    warnings.warn(UserWarning(msg))


@pytest.mark.parametrize("i", range(20))
def test_foo(i):
    func("foo")


def test_foo_1():
    func("foo")


@pytest.mark.parametrize("i", range(20))
def test_bar(i):
    func("bar")
