import gambit
import fractions
from nose.tools import assert_raises

class TestGambitStrategySupport(object):
    def setUp(self):
        self.game = gambit.new_table([2,2])
        
        self.profile_double = self.game.mixed_profile()
        self.profile_rational = self.game.mixed_profile(True)
        self.support = self.profile_double.support

        self.tree_game = gambit.read_game("test_games/mixed_behavior_game.efg")

        self.tree_profile_double = self.tree_game.mixed_profile()
        self.tree_profile_rational = self.tree_game.mixed_profile(True)
        self.tree_support = self.tree_profile_double.support

        
    def tearDown(self):
        del self.game
        del self.tree_game
        del self.profile_double
        del self.profile_rational
        del self.tree_profile_double
        del self.tree_profile_rational
        del self.support
        del self.tree_support
            

    def test_both_supports(self):
        "Test to ensure generated supports from double and rational-valued\
        profiles are equal"
        assert self.support == self.profile_rational.support
        assert self.tree_support == self.tree_profile_rational.support

    def test_getting_game(self):
        "Test retrieving the game object from a support"
        assert self.support.game == self.game
        assert self.tree_support.game == self.tree_game

    def test_getting_direct_strategies(self):
        "Test retrieving strategies from a support"
        assert self.support.strategies[0] == self.game.players[0].strategies[0]
        assert self.support.strategies[1] == self.game.players[0].strategies[1]

    def test_getting_players(self):
        "Test retrieving players from a support"
        assert self.support.players[0] == self.game.players[0]
        assert self.support.players[1] == self.game.players[1]
        assert self.tree_support.players[0] == self.tree_game.players[0]
        assert self.tree_support.players[1] == self.tree_game.players[1]
        assert self.tree_support.players[2] == self.tree_game.players[2]
        
    def test_is_subset_of(self):
        "Test to find check if a support is a subset of another one"
        assert self.support.is_subset_of(self.support)
        assert not self.support.is_subset_of(self.tree_support)
