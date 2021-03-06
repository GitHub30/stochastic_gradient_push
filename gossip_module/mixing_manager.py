# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

"""
Mixing Manager Class

:description: Class provides an API for dynamically selecting mixing weights
              for gossip
"""


class MixingManager(object):

    def __init__(self, graph):
        self.graph_manager = graph

    def is_regular(self):
        """
        Whether there is bias accumulated in local entry of stationary
        distribution of mixing matrix
        """
        return self.graph_manager.is_regular_graph() and self.is_uniform()

    def is_uniform(self):
        """ Whether mixing weights are distributed uniformly over peers """
        raise NotImplementedError

    def get_mixing_weights(self, residual_adjusted=True):
        """ Create mixing weight dictionary using uniform allocation """
        raise NotImplementedError


class UniformMixing(MixingManager):

    def get_mixing_weights(self, residual_adjusted=True):
        """ Create mixing weight dictionary using uniform allocation """
        mixing_weights = {}
        out_peers, _ = self.graph_manager.get_peers()

        w = 1. / (len(out_peers) + 1.)
        mixing_weights['lo'] = w
        w_op = w if not residual_adjusted else w / mixing_weights['lo']
        mixing_weights['uniform'] = w_op
        for op in out_peers:
            mixing_weights[op] = w_op
        return mixing_weights

    def is_uniform(self): return True
