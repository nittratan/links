filter_obj = {"is_tagged": False}
neg_filter_obj = {"clnt_audt_id": None}

SELECT * 
FROM your_table
WHERE is_tagged = false
  AND clnt_audt_id IS NOT NULL;

