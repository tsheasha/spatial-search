I will try to keep this as short as possible as requested.

Spatial seaerch brings along many ideas, most prominent of which are:-
    1) Use a datastructure to store the data in a way that the the co-ordinate
    system is maintained and efficient proximity queries can be accomplished.
    Example of such structures are R* Trees, Segment Trees, K-d trees. These
    structures have the ability to self-balance very efficiently and maintain
    a very small overlap areas between the bounding rectangles *which is the way
    they store the data*. I have decided *not* to go with this approach.

    2) Another approach is to pre-process the data and store the locaitons
    in a lower dimension system to allow for simple range queries to be able
    to retrieve near by points. The preprocessing I chose to implement is the 
    geohash, which is a derivative from the Z-order curve and is someitmes also
    called the z-index. By using thise hash as an index in a database range queries
    can be very easily done by looking for a prefix of the geohash of the current location
    and all geohashes matching that prefix lie within the proximity chosen. *dropping characters
    from the right-end of the geohash increases the radius of the search. I chose this approach.

By using a geohash as an Index in the database I created from the provided csv files
I can easily perform proximity searches. One thought that came to ming when chosing between
1) and 2) was whather we will be dealing with static/dynamic data. The locations of shops will
not change so static it was. The reason being, since the trees are self-balancing, reinsertions
will not affect the time to search they would function better with dynamic data.
Geohashes are much more efficient though with static data.

Edge cases are handles after the bulk processing has been done by the range query, to identify
outliers in a brute-force approach by measuring the distance and excludinf those in the same geohash
block but not in the same radius.

As for performance, having the data in-memory would be more efficient, however, since this should
keep in mind an increasing data-set the choice wa smade to keep the data in a database. In a real
system however, it would be useful to have an in-memory store for *hot* locations to avoid lots of
slave reads.

I have documented the code and provided tests, looking forward to discuss this solution in a call if
it is to your liking.
