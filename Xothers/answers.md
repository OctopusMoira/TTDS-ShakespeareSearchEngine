

# indexer \ search module
## regarding shakespear text analysis https://m-clark.github.io/text-analysis-with-R/shakespeare.html
index saved efficiently => use mongodb (B+ tree)
preprocess => early modern english
    casefolding
    replace commas with blank
    remove stop words (selected list, for special quote "to be or not to be". only 8. a, an, the etc.)
    // use unicodedata (remove codes), re remove redundant space
    replace special characters like with accents. = normalization ( café to cafe etc. )
    RIGHT NOW => each line contains only 1-9, a-z, blank space (seperated by one space only), æ, œ.
    
    => this is early/modern english. stemming can destroy the strcture and misinterpret the result.
    still stemming (porter)

    bm25 + regre + predict + basic (categories)

# retrieval model
    whole package for query (sat the same):
    casefold, comma, stop word, porter
    BM25 according to https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables (same default values)

    user query length => < n words

# large data collection
around 100k
english (early/modern)
line level.
text + image
one shot

# interface
web
details

# optimization
query plan https://docs.mongodb.com/manual/tutorial/optimize-query-performance-with-indexes-and-projections/

# gunicorn (multiple user? not sure)
eventlet work class, thread 2
--worker-connections default 1000

# search predict
lstm https://www.tensorflow.org/tutorials/text/text_generation

# real-time search

# hosted on server

# more
data source from https://shakespeare.folger.edu/download-the-folger-shakespeare-complete-set/
use beautifulsoup extract and clean data
stemming => different versions, different functions

spell checker? => instead phonetics
basic (categories) => and, or, (boolean), 

>>>>>>>>>>>>>>>>>>>>>>>>head
evaluation?


<!-- no phrase search => because the original text may include special letters, punctuation etc.
instead we allow proximity search. which shall be seen as a tolerable version. -->







