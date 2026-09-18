# 0004: Squash duplicate commits on arithmeticEnv fixes

Two commits with the same message were created during iterative debugging of `arithmeticEnv.py`. The first was incomplete; the second added remaining fixes. We squashed both into a single commit covering all changes: added operations, fixed operand order in divide/subtract/power/modulo, and fixed lt/gt/le/ge.

**Status:** accepted