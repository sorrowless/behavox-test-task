#!/usr/bin/env python3

from depsfinder.dataloader import DataLoader
from depsfinder.logging import getLogger
from depsfinder.ordering import Ordering
from depsfinder.parser import parser

import sys

logger = getLogger(__name__)

if __name__ == "__main__":
    args = parser.parse_args()

    # Calculate our dependencies. It is far from optimal algorithm - costs around O(n^2) but
    # we're talking about services ordering and usually there are not too many of them - 100-200
    # items, so this will work okay. And man - it's a test case and I'm not a
    # Lennart Poettering (__cross to oneself__). Further work still applicable though. For example,
    # moving from calculation for one host to calculation for N hosts where N is 100+, I would
    # optimize it from recursion to plain calculation. It's not too hard and for many nodes will
    # save a lot of CPU cycles.
    calculator = Ordering()
    methods = {
        "start": calculator.calculateDependenciesStart,
        "stop": calculator.calculateDependenciesStop
    }
    
    order = dict()
    data = DataLoader().load(args.file)
    methods[args.action](data, order)
    print(f"\n{args.action} order is: ")
    for k,v in sorted(order.items(), key=lambda x:[x[1]]):
        print(f"{k}:{v}")
