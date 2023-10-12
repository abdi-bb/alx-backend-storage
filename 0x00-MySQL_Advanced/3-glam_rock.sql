-- Calculate the lifespan of bands until 2022 using 'formed' and 'split' attributes
SELECT
    band_name,
    (IFNULL(split, '2022') - formed) AS 'lifespan'
FROM
    metal_bands
WHERE
    FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY
    lifespan DESC;