from sqlalchemy import bindparam

if neg_filter_obj:
    for key, value in neg_filter_obj.items():
        col = getattr(table.c, key)

        if value is None:  
            # IS NOT NULL
            stmt = stmt.where(col.is_not(None))

        elif isinstance(value, (list, tuple, set)):
            vals = list(value)
            if vals:  # skip empty list
                stmt = stmt.where(col.notin_(vals))

        else:
            # safe "!=" with bindparam to avoid bool type error
            stmt = stmt.where(col != bindparam(f"neg_{key}", value))
