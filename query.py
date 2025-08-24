git commit -m "fix(find_data): correct neg_filter_obj handling for IS NOT NULL, NOT IN, and != conditions

Previously, neg_filter_obj with None generated invalid SQL (col != NULL).
Now:
- None → col IS NOT NULL
- list/tuple/set → col NOT IN (...)
- scalar values → col != :param (safe bindparam)

Example:
  filter_obj = {'is_tagged': False}
  neg_filter_obj = {'clnt_audt_id': None}

Generates:
  SELECT * FROM your_table
  WHERE is_tagged = false AND clnt_audt_id IS NOT NULL;
"
