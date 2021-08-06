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
    