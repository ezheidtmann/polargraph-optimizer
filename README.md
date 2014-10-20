polargraph-optimizer
====================

Optimize drawing plan for a polargraph

Example Usage
----

Display statistics about the included drawing plan `map.txt`:

```
$ ./process.py map.txt
Total Glyphs: 8074
Initial penup distance: 4107485
Initial total distance: 4742961
Deduped penup distance: 3494625
Deduped total distance: 4040278
Sorted penup distance:  5319295
Sorted total distance: 5864948
Greedy penup (i=0) 790134
Greedy total (i=0) 1335787
Greedy penup (i=449) 791479
Greedy total (i=449) 1337132
Greedy penup (i=898) 790579
Greedy total (i=898) 1336232
Greedy penup (i=1347) 786376
Greedy total (i=1347) 1332029
Greedy penup (i=1796) 788473
Greedy total (i=1796) 1334126
Greedy penup (i=2245) 789741
Greedy total (i=2245) 1335394
...
```

Deduped with greedy sort yields a plan with approximately 28% of the total travel distance. Equivalently, the new plan is about 3.5x faster.

Currently it not possible to print the optimized plans. This is TODO.
