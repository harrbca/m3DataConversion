SELECT imfgr || "LPROD#" AS prodLine, MIN(lname) AS lname
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY iprodl ORDER BY itemNumber) AS row_num
    FROM items
    where ITEMNUMBER in ('ARMD4014161', 'ARMD4015161', 'ARMD4016161',   -- alterna ARMALT
                         'ARMD7106461', 'ARMD7110461', 'ARMD7113461', -- alterna ARMALT
                         'ARMST131641', 'ARMST132641', 'ARMST133641',
                         'ARMST281911', 'ARMST282911', 'ARMST283911',
                         'ARMST830811', 'ARMST831811', 'ARMST832811',
                         'ARMST796821', 'ARMST797821', 'ARMST798821',
                         'ARMST851611', 'ARMST852611', 'ARMST854611',
                         'ARMST510611', 'ARMST511611', 'ARMST513611',
                         'ARMST931811', 'ARMST932811', 'ARMST933811',
                         'ARMST901611', 'ARMST902611', 'ARMST903611')
) t
GROUP BY prodLine
ORDER BY prodLine;