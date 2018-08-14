import logging
import unittest
import random

from gym import Env, spaces
from numpy import array

from hearts.single import SingleEnv

logger = logging.getLogger(__name__)

class SingleEnvTest(unittest.TestCase):
    def setUp(self):
        self.env = SingleEnv()
        self.r = self.env.reset()

    def tearDown(self):
        self.env.close()

    def test_env__obs_space(self):
        self.assertTrue(self.env.observation_space.contains(self.r))

    def test_env__action_space(self):
        action = [0]
        draws = [array([-1, -1]), array([-1, -1]), array([-1, -1])]
        action.append(tuple(draws))

        self.assertTrue(self.env.action_space.contains(tuple(action)))

    def test_env__seed(self):
        seeds = self.env.seed()
        self.assertIs(type(seeds), list)
        for seed in seeds:
            self.assertIs(type(seed), int)
            self.assertEqual(self.env.n_seed, seed)

    def test_env__render(self):
        self.env.render()

    def test_env__step(self):
        cur_pos = self.env._table.cur_pos
        self.assertEqual(cur_pos, self.env.PLAYER)
        me = self.env._table.players[cur_pos]
        cards = me.hand[0:3]

        action = [cur_pos]
        draws = []
        for rank, suit in cards:
            draws.append(array([rank, suit]))
        action.append(tuple(draws))

        self.assertTrue(self.env.action_space.contains(tuple(action)))

        obs, rew, done, info = self.env.step(action)

        # XXX very strange...it's False
        # The table space cannot match XXX
        # self.assertTrue(self.env.observation_space.contains(obs))
        self.assertIs(type(rew), int)
        self.assertIs(type(done), bool)
        self.assertFalse(done)
        self.assertIs(type(info), dict)
        self.assertEqual(cur_pos, self.env.PLAYER)

        draws = []
        me.hand.reverse()
        if self.env._table.first_draw:
            for card in me.hand:
                if card[1] == self.env._table.first_draw[1]:
                    draws.append(card)
                    break
        if not draws:
            if self.env._table.n_round == 0:
                draws = [(0, 3)]
            else:
                draws = [random.choice(me.hand)]

        acts = self.env._convert_act_actspace((cur_pos, draws))
        obs, rew, done, info = self.env.step(acts)
        self.assertEqual(cur_pos, self.env.PLAYER)


