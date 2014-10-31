polargraph-optimizer
====================

Optimize drawing plan for a polargraph

Example Usage
----

Optimize the included drawing plan `map.txt`:

```
$ time ./process.py map.txt > map_optimized.txt 
Total Glyphs: 8074
Initial penup distance:   4107485
Initial total distance:   4742961
Deduped penup distance:   3494625
Deduped total distance:   4040278
Sorted penup distance:    5319295
Sorted total distance:    5864948
Greedy penup (i=0)         119543
Greedy total (i=0)         665196

real  1m14.309s
user  1m14.214s
sys 0m0.072s
```

Now `map_optimized.txt` includes a reordered drawing plan with duplicate glyphs removed and with an improved ordering.

About the algorithm
----

The optimization algorithm is basically this:

  * Remove path sections which are exact duplicates of earlier sections
  * Reorder paths:
    * Pick the first path as the first path in the input file
    * Find the path that starts nearest the previous one's endpoint, or the one which, if reversed, would start nearest the previous one's endpoint
    * Repeat until we have processed all paths

For the drawing plan `map.txt` included, this results in a 7.1x improvement in total pen travel distance (see code for definition of distance). Actual results will vary due to a variety of factors. Please report real-life results so we can include them here!

Contributors
----

[Evan Heidtmann](https://github.com/ezheidtmann)
[Olivier Bouwman](https://github.com/olivierbouwman)
