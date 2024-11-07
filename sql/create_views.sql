DROP VIEW IF EXISTS v_post_param_pivoted;
CREATE VIEW v_post_param_pivoted
AS SELECT
    post_id,
    MAX(CASE WHEN param_key = 'block' THEN param_value ELSE '' END) AS block,
    MAX(CASE WHEN param_key = 'pty_characteristics' THEN param_value ELSE '' END) AS pty_characteristics,
    MAX(CASE WHEN param_key = 'commercial_type' THEN param_value ELSE '' END) AS commercial_type,
    MAX(CASE WHEN param_key = 'land_type' THEN param_value ELSE '' END) AS land_type,
    MAX(CASE WHEN param_key = 'size_unit' THEN param_value ELSE '' END) AS size_unit,
    MAX(CASE WHEN param_key = 'apartment_type' THEN param_value ELSE '' END) AS apartment_type,
    MAX(CASE WHEN param_key = 'floors' THEN param_value ELSE '' END) AS floors,
    MAX(CASE WHEN param_key = 'furnishing_rent' THEN param_value ELSE '' END) AS furnishing_rent,
    MAX(CASE WHEN param_key = 'direction' THEN param_value ELSE '' END) AS direction,
    MAX(CASE WHEN param_key = 'width' THEN param_value ELSE '' END) AS width,
    MAX(CASE WHEN param_key = 'floornumber' THEN param_value ELSE '' END) AS floornumber,
    MAX(CASE WHEN param_key = 'furnishing_sell' THEN param_value ELSE '' END) AS furnishing_sell,
    MAX(CASE WHEN param_key = 'toilets' THEN param_value ELSE '' END) AS toilets,
    MAX(CASE WHEN param_key = 'rooms' THEN param_value ELSE '' END) AS rooms,
    MAX(CASE WHEN param_key = 'property_status' THEN param_value ELSE '' END) AS property_status,
    MAX(CASE WHEN param_key = 'length' THEN param_value ELSE '' END) AS length,
    MAX(CASE WHEN param_key = 'price_m2' THEN param_value ELSE '' END) AS price_m2,
    MAX(CASE WHEN param_key = 'property_legal_document' THEN param_value ELSE '' END) AS property_legal_document,
    MAX(CASE WHEN param_key = 'size' THEN param_value ELSE '' END) AS size,
    MAX(CASE WHEN param_key = 'deposit' THEN param_value ELSE '' END) AS deposit,
    MAX(CASE WHEN param_key = 'house_type' THEN param_value ELSE '' END) AS house_type,
    MAX(CASE WHEN param_key = 'ad_type' THEN param_value ELSE '' END) AS ad_type,
    MAX(CASE WHEN param_key = 'street_id' THEN param_value ELSE '' END) AS street_id
FROM post_param
GROUP BY post_id;

DROP VIEW IF EXISTS v_post_detail_address_parsed;
CREATE VIEW v_post_detail_address_parsed AS
WITH get_array AS (
    SELECT *, array_length(items, 1) AS num_items FROM (
        SELECT *, string_to_array(address, ',') AS items
        FROM post_detail
    ) AS t
), split_address AS (
    SELECT *,
        CASE WHEN num_items >= 4 THEN
            trim(split_part(address, ',', num_items))::text
        END AS province,
        CASE WHEN num_items >= 4 THEN
            trim(split_part(address, ',', num_items - 1))::text
        END AS district,
        CASE WHEN num_items >= 4 THEN
            trim(split_part(address, ',', num_items - 2))::text
        END AS ward,
        CASE WHEN num_items >= 4 THEN
            trim(split_part(address, ',', num_items - 3))::text
        END AS street
    FROM get_array
)

SELECT post_id, post_url, post_type, post_title,
       street, ward, district,
       CASE WHEN province LIKE '%Hồ Chí Minh%' THEN
           'Hồ Chí Minh' ELSE province
       END AS province
FROM split_address
