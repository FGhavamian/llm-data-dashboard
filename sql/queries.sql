-- Query 1:
select year(datetime), month(datetime), sum(revenue) from Sales group by year(datetime), month(datetime);

-- Query 2:
select sum(amount) from Costs group by category;