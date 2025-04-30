select * from items
left join main.item_hierarchy ih on items.ITEMNUMBER = ih.ITEMNUMBER
where imfgr not in ('ARM', 'CAS', 'PHE', 'INT', 'JON', 'ALA', 'TAN') and items.ITEMNUMBER  not like '%MISC%'
and iprodl not in ('SAM', 'SET', 'DIS')