SELECT imfgr || "LPROD#" AS prodLine, MIN(lname) AS lname
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY iprodl ORDER BY itemNumber) AS row_num
    FROM items
    WHERE iprodl IN ('ING')
) t
WHERE row_num <= 3
GROUP BY prodLine
ORDER BY prodLine;