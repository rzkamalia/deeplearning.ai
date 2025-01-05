+ Vector embeddings capture meaning. Vector embeddings is a machine undestable format of data.

+ There are many ways to calculate the distances between two vectors. Here distance metrics that you might find being used in the context of vector databases:
    + Euclidean Distance(L2)
    + Manhattan Distance(L1)
    + Dot Product
    + Cosine Distance

+ 'brute force' search algorithm
    1. Measure the L2 distance between the query and each vector.
    2. Sort all thse distances.
    3. Return the top K matches. These are the most semantically similar points.