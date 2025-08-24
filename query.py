if filter_obj:
    for key, value in filter_obj.items():
        if value is None:  # IS NULL
            stmt = stmt.where(getattr(table.c, key).is_(None))
        elif isinstance(value, list):
            if value:
                stmt = stmt.where(getattr(table.c, key).in_(value))
        else:
            stmt = stmt.where(getattr(table.c, key) == bindparam(key, value))




if neg_filter_obj:
    for key, value in neg_filter_obj.items():
        if value is None:  # handle IS NOT NULL
            stmt = stmt.where(getattr(table.c, key).is_not(None))
        elif isinstance(value, list):
            if value:  # skip empty list
                stmt = stmt.where(getattr(table.c, key).notin_(value))
        else:
            stmt = stmt.where(getattr(table.c, key) != value)
