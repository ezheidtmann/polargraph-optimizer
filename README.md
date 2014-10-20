polargraph-optimizer
====================

Optimize drawing plan for a polargraph

Example Usage
----

Optimize the included drawing plan `map.txt`:

```
$ time ./process.py map.txt > map_optimized.txt
Total Glyphs: 8074
Initial penup distance: 4107485
Initial total distance: 4742961
Deduped penup distance: 3494625
Deduped total distance: 4040278
Sorted penup distance:  5319295
Sorted total distance: 5864948
Greedy penup (i=0) 790134
Greedy total (i=0) 1335787

real  0m32.711s
user  0m32.658s
sys 0m0.032s
```

Now `map_optimized.txt` includes a reordered drawing plan with duplicate glyphs removed and with an improved ordering.

Deduplication with greedy sort yields a plan with approximately 28% of the total travel distance. Equivalently, the new plan is about 3.5x faster.
