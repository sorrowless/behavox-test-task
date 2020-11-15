from logging import getLogger
from typing import Dict
from depsfinder.exceptions import RingDependencyError


class Ordering(object):
    def __init__(self):
        self.logger = getLogger(__name__)

    def calculateDependenciesStart(self, initialData: Dict = {}, orderedData: Dict = {}):
        initialLength = len(initialData)
        # Simple optimization. We could move this into RingDependencyError check but checking it
        # here will save us up to O(1) cycles.
        if initialLength == 0:
            return orderedData
        #
        for key in list(initialData.keys()):
            if not initialData[key]:
                # In case you define your services as
                # srv1:
                # srv2:
                #   deps: []
                #
                # we have to explicitly convert it from None to dict
                initialData[key] = {}
            if not initialData[key].get('deps', False):  # if there are no deps, sevrice started first
                orderedData[key] = 0
                initialData.pop(key, None)  # remove key as it is not needed anymore
                continue
            depsResolved = True
            keyOrder = -1
            deps = initialData[key]['deps']
            for depkey in deps:
                # If there is a key in dependencies which does not exist yet in ordered dat, it means
                # that we cannot start current service yet cause not all its dependencies were
                # resolved yet
                if depkey not in orderedData:
                    depsResolved = False
                    break
                else:
                    keyOrder = max(keyOrder, orderedData[depkey]) + 1
            if depsResolved:
                orderedData[key] = keyOrder
                initialData.pop(key, None)
        if initialLength == len(initialData):
            self.logger.error(
                "Sorry, but seems your order is unsolvable. There are next items: "
                f"{initialData.keys()} which depends on each other. Fix your "
                "initial ordering and back away."
            )
            raise RingDependencyError

        # if not all initial fields were processed, it means we still have some deps unresolved, so run
        # next iteration
        if initialData:
            self.calculateDependenciesStart(initialData, orderedData)

    def calculateDependenciesStop(self, initialData: Dict = {}, orderedData: Dict = {}):
        initialLength = len(initialData)
        if initialLength == 0:
            return orderedData
        # Simple optimization. We could move this into RingDependencyError check but checking it
        # here will save us up to O(1) cycles.
        if initialLength == 0:
            return orderedData
        #
        keys = list(initialData)  # gives us only the keys
        levelItems = dict()
        # levelKeysOrder stores max order number for already processed items. Basically it
        # means that all items on current level will have an order of levelKeysOrder
        levelKeysOrder = max([orderedData[key] for key in orderedData] or [-1]) + 1

        for key in keys:
            canBeStoppedAtThisLevel = True
            for potentialKey in keys:  # Oh my god, O(n^2). Would be nice to optimize it in real task
                if key == potentialKey:  # skip key comparation with itself
                    continue
                if not initialData[key]:
                    # In case you define your services as
                    # srv1:
                    # srv2:
                    #   deps: []
                    #
                    # we have to explicitly convert it from None to dict
                    initialData[key] = {}
                deps = initialData.get(potentialKey).get('deps', False)
                if deps and (key in deps):
                    canBeStoppedAtThisLevel = False
                    break
            if canBeStoppedAtThisLevel:
                levelItems[key] = levelKeysOrder

        for key in levelItems:
            orderedData[key] = levelItems[key]
            initialData.pop(key, None)

        if initialLength == len(initialData):
            self.logger.error(
                "Sorry, but seems your order is unsolvable. There are next items: "
                f"{initialData.keys()} which depends on each other. Fix your "
                "initial ordering and back away."
            )
            raise RingDependencyError

        # if not all initial fields were processed, it means we still have some deps unresolved, so run
        # next iteration
        if initialData:
            self.calculateDependenciesStop(initialData, orderedData)
