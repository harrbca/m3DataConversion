select * from items
left join main.item_hierarchy ih on items.ITEMNUMBER = ih.ITEMNUMBER
where imfgr not in ('INT', 'JON', 'ALA', 'TAN') and items.ITEMNUMBER  not like '%MISC%'
  and items.ITEMNUMBER not in ('ARMLABOUR')
and iprodl not in ('SAM', 'SET', 'DIS')