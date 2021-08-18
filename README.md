# WCL MageSim Data

Goal is to mine WCL and estimate water elemental's damage based
Karazhan fights.

## Tentative Approach

Pull down X fight logs, all containing a water elemental.
Control for Heroism, totems and drums; strategy TBD. Estimate
waterbolt damage as a function of mage attributes (TBD). Estimate
elemental mana pool and regen via linear dependency on mage's mana
and regen.


## Log

- Pulling and extracting like an idiot. Obviously should pull everything down and then transform
    to a new directory after the fact.
- Waterbolt latencies for auto-attack seem like they could be modeled by well by a Gamma distribution.
    In one manual cast I was able to get it down to 2.517 seconds. Otherwise for auto-cast it's almost
    entirely between 3.15 and 3.30 seconds.
