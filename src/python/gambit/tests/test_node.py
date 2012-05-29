import gambit
from nose.tools import assert_raises
from gambit.lib.error import MismatchError, UndefinedOperationError


class TestGambitNode(object):
    def setUp(self):
        self.extensive_game = gambit.read_game("test_games/basic_extensive_game.efg")
        
    def tearDown(self):
        del self.extensive_game
        
    def test_get_infoset(self):
        "Test to ensure that we can retrieve an infoset for a given node"
        assert self.extensive_game.root.infoset != None
        assert self.extensive_game.root.children[0].infoset != None
        assert self.extensive_game.root.children[0].children[1].children[0].infoset == None

    def test_get_outcome(self):
        "Test to ensure that we can retrieve an outcome for a given node"
        assert self.extensive_game.root.children[0].children[1].children[0].outcome == self.extensive_game.outcomes[1]
        assert self.extensive_game.root.outcome == None

    def test_get_player(self):
        "Test to ensure that we can retrieve a player for a given node"
        assert self.extensive_game.root.player == self.extensive_game.players[0]
        assert self.extensive_game.root.children[0].children[1].children[0].player == None
        
    def test_get_parent(self):
        "Test to ensure that we can retrieve a parent node for a given node"
        assert self.extensive_game.root.children[0].parent == self.extensive_game.root
        assert self.extensive_game.root.parent == None

    def test_get_prior_action(self):
        "Test to ensure that we can retrieve the prior action for a given node"
        assert self.extensive_game.root.children[0].prior_action == self.extensive_game.root.infoset.actions[0]
        assert self.extensive_game.root.prior_action == None
        
    def test_get_prior_sibling(self):
        "Test to ensure that we can retrieve a prior sibling of a given node"
        assert self.extensive_game.root.children[1].prior_sibling == self.extensive_game.root.children[0]
        assert self.extensive_game.root.children[0].prior_sibling == None

    def test_get_next_sibling(self):
        "Test to ensure that we can retrieve a next sibling of a given node"
        assert self.extensive_game.root.children[0].next_sibling == self.extensive_game.root.children[1]
        assert self.extensive_game.root.children[1].next_sibling == None

    def test_is_terminal(self):
        "Test to ensure that we can check if a given node is a terminal node"
        assert self.extensive_game.root.is_terminal == False
        assert self.extensive_game.root.children[0].children[0].children[0].is_terminal == True

    def test_is_successor_of(self):
        "Test to ensure that we can check if a given node is a successor of a supplied node"
        assert self.extensive_game.root.children[0].is_successor_of(self.extensive_game.root) == True
        assert self.extensive_game.root.is_successor_of(self.extensive_game.root.children[0]) == False
        assert_raises(TypeError, self.extensive_game.root.is_successor_of, 9)
        assert_raises(TypeError, self.extensive_game.root.is_successor_of, "Test")
        assert_raises(TypeError, self.extensive_game.root.is_successor_of, self.extensive_game.players[0])

    def test_is_subgame_root(self):
        "Test to ensure that we can check if a given node is a marked subgame"
        assert self.extensive_game.root.is_subgame_root() == True
        assert self.extensive_game.root.children[0].is_subgame_root() == False

    def test_append_move_error_terminal(self):
        "Test to ensure the node is terminal"
        assert_raises(UndefinedOperationError, self.extensive_game.root.append_move, "")

    def test_append_move_error_player_actions(self):
        "Test to ensure there are actions when appending with a player"
        assert_raises(UndefinedOperationError, self.extensive_game.root.append_move, 
                        self.extensive_game.players[0])
        assert_raises(UndefinedOperationError, self.extensive_game.root.append_move, 
                        self.extensive_game.players[0], 0)

    def test_append_move_error_player_mismatch(self):
        "Test to ensure the node and the player are from the same game"
        game = gambit.new_tree()
        assert_raises(MismatchError, game.root.append_move,
                        self.extensive_game.players[0], 1)

    def test_append_move_error_infoset_actions(self):
        "Test to ensure there are no actions when appending with an infoset"
        assert_raises(UndefinedOperationError, self.extensive_game.root.append_move, 
                        self.extensive_game.players[0].infosets[0], 1)

    def test_append_move_error_infoset_mismatch(self):
        "Test to ensure the node and the player are from the same game"
        game = gambit.new_tree()
        assert_raises(MismatchError, game.root.append_move,
                        self.extensive_game.players[0].infosets[0])

    def test_insert_move_error_player_actions(self):
        "Test to ensure there are actions when inserting with a player"
        assert_raises(UndefinedOperationError, self.extensive_game.root.insert_move, 
                        self.extensive_game.players[0])
        assert_raises(UndefinedOperationError, self.extensive_game.root.insert_move, 
                        self.extensive_game.players[0], 0)

    def test_insert_move_error_player_mismatch(self):
        "Test to ensure the node and the player are from the same game"
        game = gambit.new_tree()
        assert_raises(MismatchError, game.root.insert_move,
                        self.extensive_game.players[0], 1)

    def test_insert_move_error_infoset_actions(self):
        "Test to ensure there are no actions when inserting with an infoset"
        assert_raises(UndefinedOperationError, self.extensive_game.root.insert_move, 
                        self.extensive_game.players[0].infosets[0], 1)

    def test_insert_move_error_infoset_mismatch(self):
        "Test to ensure the node and the player are from the same game"
        game = gambit.new_tree()
        assert_raises(MismatchError, game.root.insert_move,
                        self.extensive_game.players[0].infosets[0])
