# -*- coding: utf-8 -*-

from __future__ import division, print_function

from multiprocessing import Pool
import pytest
import numpy as np

from emcee import moves
from emcee.moves.hmc import (
    IdentityMetric, IsotropicMetric, DiagonalMetric, DenseMetric
)

from .test_proposal import _test_normal

__all__ = ["test_normal_nuts"]


@pytest.mark.parametrize("metric", [None, IdentityMetric(3),
                                    IsotropicMetric(3),
                                    DiagonalMetric(np.ones(3)),
                                    DenseMetric(np.eye(3))])
@pytest.mark.parametrize("pool", [True, False])
@pytest.mark.parametrize("tune", [True, False])
@pytest.mark.parametrize("blobs", [True, False])
def test_normal_nuts(pool, metric, tune, blobs, **kwargs):
    if tune:
        move = moves.NoUTurnMove(ntune=500, metric=metric)
    else:
        move = moves.NoUTurnMove(metric=metric)
    kwargs["ndim"] = 3
    kwargs["nwalkers"] = 2
    kwargs["check_acceptance"] = False
    kwargs["nsteps"] = 500 + int(tune) * 500
    kwargs["blobs"] = blobs
    if pool:
        with Pool() as p:
            kwargs["pool"] = p
            _test_normal(move, **kwargs)
    else:
        _test_normal(move, **kwargs)