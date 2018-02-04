import pandas as pd

# Cache results from search for use in the future rather than recalculating
def cache_result(topdf, con):
    topdf.to_sql("result_cache", con, if_exists="append", index=False)


# Check and return data from the cache
def return_cache_result(movieId, con):
    sql_string = "select * from result_cache where likedMovie = {};".format(movieId)
    df = pd.read_sql_query(sql_string, con)
    return df


# generate empty cache container
def get_empty_cache():
    empty_cache = pd.DataFrame(0, index=[0,1,2], columns=['0','1','2','3','4','5','6','7'])
    return empty_cache