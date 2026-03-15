-- 1. Overall Summary Stats
SELECT
    COUNT(*)                    AS total_trading_days,
    ROUND(MIN(Close), 2)        AS all_time_low,
    ROUND(MAX(Close), 2)        AS all_time_high,
    ROUND(AVG(Close), 2)        AS avg_close,
    ROUND(MIN(Volume), 2)       AS min_volume,
    ROUND(MAX(Volume), 2)       AS max_volume,
    ROUND(AVG(Volume), 2)       AS avg_volume
FROM tcs_history;

-- 2. Yearly Average Prices
SELECT
    Year,
    ROUND(AVG(Open),  2)        AS avg_open,
    ROUND(AVG(High),  2)        AS avg_high,
    ROUND(AVG(Low),   2)        AS avg_low,
    ROUND(AVG(Close), 2)        AS avg_close,
    ROUND(AVG(Volume),2)        AS avg_volume,
    ROUND(MAX(Close), 2)        AS yearly_high,
    ROUND(MIN(Close), 2)        AS yearly_low
FROM tcs_history
GROUP BY Year
ORDER BY Year;

-- 3. Monthly Average Close Price
SELECT
    Year,
    Month,
    Month_Name,
    ROUND(AVG(Close), 2)        AS avg_close,
    ROUND(MAX(Close), 2)        AS month_high,
    ROUND(MIN(Close), 2)        AS month_low,
    ROUND(AVG(Volume),2)        AS avg_volume
FROM tcs_history
GROUP BY Year, Month
ORDER BY Year, Month;

-- 4. Quarterly Performance
SELECT
    Year,
    Quarter,
    ROUND(AVG(Close), 2)        AS avg_close,
    ROUND(MAX(Close), 2)        AS quarter_high,
    ROUND(MIN(Close), 2)        AS quarter_low,
    ROUND(SUM(Volume),2)        AS total_volume
FROM tcs_history
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- 5. Top 10 Highest Closing Prices
SELECT
    Date,
    ROUND(Open,  2)             AS Open,
    ROUND(High,  2)             AS High,
    ROUND(Low,   2)             AS Low,
    ROUND(Close, 2)             AS Close,
    Volume
FROM tcs_history
ORDER BY Close DESC
LIMIT 10;

-- 6. Top 10 Lowest Closing Prices
SELECT
    Date,
    ROUND(Open,  2)             AS Open,
    ROUND(High,  2)             AS High,
    ROUND(Low,   2)             AS Low,
    ROUND(Close, 2)             AS Close,
    Volume
FROM tcs_history
ORDER BY Close ASC
LIMIT 10;

-- 7. Top 10 Highest Volume Days
SELECT
    Date,
    ROUND(Close, 2)             AS Close,
    Volume
FROM tcs_history
ORDER BY Volume DESC
LIMIT 10;

-- 8. Dividend Events
SELECT
    Date,
    ROUND(Close,     2)         AS Close,
    ROUND(Dividends, 2)         AS Dividends
FROM tcs_history
WHERE Dividends > 0
ORDER BY Date;

-- 9. Stock Split Events
SELECT
    Date,
    ROUND(Close, 2)             AS Close,
    "Stock Splits"              AS Stock_Splits
FROM tcs_history
WHERE "Stock Splits" > 0
ORDER BY Date;

-- 10. Days Where Close > MA50
SELECT
    COUNT(*)                    AS days_above_ma50
FROM tcs_history
WHERE Close > MA50;

-- 11. Days Where Close < MA50
SELECT
    COUNT(*)                    AS days_below_ma50
FROM tcs_history
WHERE Close < MA50;

-- 12. Best Performing Month Overall
SELECT
    Month_Name,
    ROUND(AVG(Daily_Return), 4) AS avg_daily_return,
    COUNT(*)                    AS trading_days
FROM tcs_history
GROUP BY Month_Name
ORDER BY avg_daily_return DESC;

-- 13. Best Performing Year by Return
SELECT
    Year,
    ROUND(SUM(Daily_Return), 2) AS total_return_pct,
    ROUND(AVG(Daily_Return), 4) AS avg_daily_return
FROM tcs_history
GROUP BY Year
ORDER BY total_return_pct DESC;

-- 14. Volatility by Year
SELECT
    Year,
    ROUND(AVG(Volatility_30), 4) AS avg_volatility,
    ROUND(MAX(Volatility_30), 4) AS max_volatility
FROM tcs_history
WHERE Volatility_30 IS NOT NULL
GROUP BY Year
ORDER BY Year;

-- 15. Price Range Analysis by Year
SELECT
    Year,
    ROUND(AVG(Price_Range), 2)  AS avg_daily_range,
    ROUND(MAX(Price_Range), 2)  AS max_daily_range
FROM tcs_history
GROUP BY Year
ORDER BY Year;

-- 16. Buy Signal Days Per Year
SELECT
    Year,
    SUM(CASE WHEN Signal = 1  THEN 1 ELSE 0 END) AS buy_signal_days,
    SUM(CASE WHEN Signal = -1 THEN 1 ELSE 0 END) AS sell_signal_days
FROM tcs_history
GROUP BY Year
ORDER BY Year;

-- 17. Day of Week Performance
SELECT
    Day_of_Week,
    ROUND(AVG(Daily_Return), 4) AS avg_return,
    COUNT(*)                    AS trading_days
FROM tcs_history
GROUP BY Day_of_Week
ORDER BY avg_return DESC;

-- 18. Recent 30 Days Data
SELECT
    Date,
    ROUND(Open,  2)             AS Open,
    ROUND(High,  2)             AS High,
    ROUND(Low,   2)             AS Low,
    ROUND(Close, 2)             AS Close,
    Volume,
    ROUND(MA7,   2)             AS MA7,
    ROUND(MA30,  2)             AS MA30
FROM tcs_history
ORDER BY Date DESC
LIMIT 30;

-- 19. All Time Price Milestones
SELECT
    CASE
        WHEN Close >= 3500 THEN "Above 3500"
        WHEN Close >= 3000 THEN "3000 to 3500"
        WHEN Close >= 2000 THEN "2000 to 3000"
        WHEN Close >= 1000 THEN "1000 to 2000"
        WHEN Close >= 500  THEN "500 to 1000"
        ELSE "Below 500"
    END                         AS price_band,
    COUNT(*)                    AS trading_days
FROM tcs_history
GROUP BY price_band
ORDER BY MIN(Close);

-- 20. Decade Wise Summary
SELECT
    CASE
        WHEN Year BETWEEN 2002 AND 2009 THEN "2002 to 2009"
        WHEN Year BETWEEN 2010 AND 2019 THEN "2010 to 2019"
        WHEN Year BETWEEN 2020 AND 2025 THEN "2020 to 2025"
    END                         AS decade,
    ROUND(AVG(Close),  2)       AS avg_close,
    ROUND(MAX(Close),  2)       AS decade_high,
    ROUND(MIN(Close),  2)       AS decade_low,
    ROUND(AVG(Volume), 2)       AS avg_volume
FROM tcs_history
GROUP BY decade
ORDER BY decade;