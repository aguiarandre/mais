from google.cloud import bigquery


def freq(dataset_id,
         table_id, 
         col_name,
         project_id='basedosdados',
         order_by_freq=False, 
         ascending=True,
         verbose=True
        ):
    """
    Return a dataframe containing the frequency table of the `col_name` 
    (which can be a list of columns) specified.
    """

    client = bigquery.Client()
    if not (isinstance(col_name, list) or isinstance(col_name,tuple)):
        col_name = [col_name]
    
    # generate the query for the frequency table
    table_name = f'{project_id}.{dataset_id}.{table_id}'
    query_str = _freq_query(table_name, col_name)
    
    freq_cols = ['perc_' + col.lower() for col in col_name]
    cols_str = ' and '.join(col_name)

    if order_by_freq:
        job = client.query(query_str)
        result = job.to_dataframe().sort_values(by='frequency', 
                                                ascending=ascending)
    else:
        job = client.query(query_str)
        result = job.to_dataframe().sort_values(by=col_name, 
                                                ascending=ascending)

    return result
    
    
def _freq_query(table_name, col_name):
    keys = ', \n\t\t'.join(col_name)
    
    # each calculated column of the frequency table
    counts = ['COUNT(*) AS frequency',
                'COUNT(*)/(SUM(COUNT(*)) OVER()) AS percentage',
                'SUM(COUNT(*)) OVER window_freq AS cumulative_freq',
                '(SUM(COUNT(*)) OVER window_freq)/(SUM(COUNT(*)) OVER ()) AS cumulative_percentage']

    aggregations = ',\n\t'.join(counts)
    
    query_str = f"""
        SELECT {keys},
            {aggregations}
        FROM {table_name}
        GROUP BY {keys}
    WINDOW window_freq AS (ORDER BY COUNT(*) RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    """
    
    return query_str