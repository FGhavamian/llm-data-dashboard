-- Sales table contains revenue earned at each day
CREATE TABLE Sales (
    date DATE NOT NULL,
    revenue DECIMAL(10, 2) NOT NULL
);

-- This table contains costs at each month divided by different categories (such as, utilities, logistics, ...). This table does not include costs due to tax. 
CREATE TABLE Costs (
    datetime DATETIME,
    category VARCHAR(255),
    amount DECIMAL(10, 2)
);

-- This table contains amount of tax at each month. The column is_paid shows whether this amount is paid or not. 
CREATE TABLE Tax (
    datetime DATETIME,
    amount DECIMAL(10, 2),
    is_paid BOOLEAN
);
