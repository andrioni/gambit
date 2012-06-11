from cython.operator cimport dereference as deref

cdef class SupportStrategies(Collection):
    "Represents a collection of strategies in a support."
    cdef c_StrategySupport support
    def __len__(self):    return self.support.MixedProfileLength()
    def __getitem__(self, strat):
        if not isinstance(strat, int):
            return Collection.__getitem__(self, strat)
        cdef c_ArrayInt num_strategies
        cdef Strategy s
        num_strategies = self.support.NumStrategies()
        for i in range(1,num_strategies.Length()+1):
            if strat - num_strategies.getitem(i) < 0:
                s = Strategy()
                s.strategy = self.support.GetStrategy(i, strat+1)                
                return s
            strat = strat - num_strategies.getitem(i)
        raise IndexError("Index out of range")

cdef class StrategySupport:
    cdef c_StrategySupport support

    def __repr__(self):
        return "<Support from Game '%s'>" % self.game.title

    # def __dealloc__(self):
    #     del_StrategySupport(self.support)

    def __richcmp__(StrategySupport self, other, whichop):
        if isinstance(other, StrategySupport):
            if whichop == 2:
                #return deref(self.support) == deref((<StrategySupport>other).support)
                return self.support == (<StrategySupport>other).support
            elif whichop == 3:
                #return deref(self.support) != deref((<StrategySupport>other).support)
                return self.support != (<StrategySupport>other).support
            else:
                raise NotImplementedError
        else:
            if whichop == 2:
                return False
            elif whichop == 3:
                return True
            else:
                raise NotImplementedError

    def __hash__(self):
        return long(<long>self.game.deref())

    property game:
        def __get__(self):
            cdef Game g
            g = Game()
            g.game = self.support.GetGame()
            return g

    property players:
        def __get__(self):
            cdef Players p
            p = Players()
            p.game = (<Game>self.game).game
            return p

    property strategies:
        def __get__(self):
            cdef SupportStrategies s
            s = SupportStrategies()
            s.support = self.support
            return s

    def delete(self, strat):
        cdef StrategySupport new_support
        if isinstance(strat, Strategy):
            new_support = StrategySupport()
            new_support.support = self.support
            new_support.support.RemoveStrategy((<Strategy>strat).strategy)
            return new_support
        raise TypeError("delete requires a Strategy object")

    def undominated(self, strict=False, external=False):
        cdef StrategySupport new_support
        new_support = StrategySupport()
        new_support.support = self.support.Undominated(strict, external)
        return new_support

    def is_subset_of(self, spt):
        if isinstance(spt, StrategySupport):
            #return self.support.IsSubsetOf(deref((<StrategySupport>spt).support))
            return self.support.IsSubsetOf((<StrategySupport>spt).support)
        raise TypeError("is_subset_of requires a StrategySupport object")
