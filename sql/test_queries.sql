alter table post_detail
add posted_at int;

select price_in_mil, to_timestamp(posted_at)::date as posted_at from post_detail
where post_id = '119875182';

select * from pending_post_entity
where status = 'E';

select province, count(1) from v_post_detail_address_parsed
group by province
order by count(1)