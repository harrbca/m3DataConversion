SELECT IMFGR, MIN(mname) AS MNAME
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY iprodl ORDER BY itemNumber) AS row_num
    FROM items
    WHERE iprodl IN ('ING')
) t
WHERE row_num <= 3
GROUP BY IMFGR
ORDER BY IMFGR;