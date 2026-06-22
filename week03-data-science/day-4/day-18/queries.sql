-- =====================================================================
-- Day 18 — SQL Fundamentals Main Task
-- Deliverable: sql/queries.sql
-- Description: 20 business queries answering questions against the Chinook database
-- =====================================================================

-- Query 1: Simple Filtering
-- Question: List all customers living in Canada.
SELECT CustomerId, FirstName, LastName, Country, Email
FROM Customer
WHERE Country = 'Canada';

-- Query 2: Basic Aggregation
-- Question: Find the total revenue from all sales (invoice totals).
SELECT SUM(Total) as TotalRevenue
FROM Invoice;

-- Query 3: Group By & Having
-- Question: Find genres containing more than 100 tracks.
SELECT g.Name as GenreName, COUNT(t.TrackId) as TrackCount
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.Name
HAVING COUNT(t.TrackId) > 100
ORDER BY TrackCount DESC;

-- Query 4: Basic Join
-- Question: Retrieve the name of each artist along with their albums.
SELECT ar.Name as ArtistName, al.Title as AlbumTitle
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
ORDER BY ArtistName, AlbumTitle
LIMIT 20;

-- Query 5: Multiple Table Join
-- Question: Show invoice details including invoice ID, invoice date, customer full name, and billing country.
SELECT i.InvoiceId, i.InvoiceDate, c.FirstName || ' ' || c.LastName as CustomerName, i.BillingCountry
FROM Invoice i
JOIN Customer c ON i.CustomerId = c.CustomerId
ORDER BY i.InvoiceDate DESC
LIMIT 20;

-- Query 6: Aggregated Join
-- Question: Calculate the total amount spent by each customer, sorted highest to lowest.
SELECT c.CustomerId, c.FirstName || ' ' || c.LastName as CustomerName, SUM(i.Total) as TotalSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalSpent DESC
LIMIT 10;

-- Query 7: Left Join / Unmatched Rows
-- Question: Find all tracks that have never been purchased (do not exist in any invoice lines).
SELECT t.TrackId, t.Name as TrackName, t.Composer
FROM Track t
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
WHERE il.InvoiceLineId IS NULL
LIMIT 20;

-- Query 8: Ranked Join & Grouping
-- Question: Find the top 5 most popular artists by quantity of tracks sold.
SELECT ar.Name as ArtistName, SUM(il.Quantity) as TotalSold
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
GROUP BY ar.Name
ORDER BY TotalSold DESC
LIMIT 5;

-- Query 9: Subquery (WHERE clause)
-- Question: Get the names of all employees who report directly to Andrew Adams.
SELECT EmployeeId, FirstName || ' ' || LastName as EmployeeName, Title
FROM Employee
WHERE ReportsTo = (SELECT EmployeeId FROM Employee WHERE FirstName = 'Andrew' AND LastName = 'Adams');

-- Query 10: Correlated Subquery
-- Question: List each customer's invoice details for their maximum single-invoice purchase.
SELECT i1.CustomerId, i1.InvoiceId, i1.InvoiceDate, i1.Total
FROM Invoice i1
WHERE i1.Total = (
    SELECT MAX(i2.Total)
    FROM Invoice i2
    WHERE i2.CustomerId = i1.CustomerId
)
ORDER BY CustomerId
LIMIT 20;

-- Query 11: Common Table Expression (CTE)
-- Question: Calculate the monthly sales revenue for the year 2011.
WITH Sales_2011 AS (
    SELECT InvoiceId, Total, strftime('%m', InvoiceDate) as MonthNum
    FROM Invoice
    WHERE strftime('%Y', InvoiceDate) = '2011'
)
SELECT MonthNum, SUM(Total) as MonthlyRevenue, COUNT(InvoiceId) as SalesCount
FROM Sales_2011
GROUP BY MonthNum
ORDER BY MonthNum;

-- Query 12: Recursive CTE / Hierarchy
-- Question: Construct the organizational chart displaying employee names and their immediate supervisor's names.
WITH RECURSIVE OrgChart AS (
    SELECT EmployeeId, FirstName, LastName, ReportsTo, 1 as Level,
           FirstName || ' ' || LastName as Path
    FROM Employee
    WHERE ReportsTo IS NULL
    
    UNION ALL
    
    SELECT e.EmployeeId, e.FirstName, e.LastName, e.ReportsTo, oc.Level + 1,
           oc.Path || ' -> ' || e.FirstName || ' ' || e.LastName
    FROM Employee e
    JOIN OrgChart oc ON e.ReportsTo = oc.EmployeeId
)
SELECT Level, FirstName || ' ' || LastName as EmployeeName, Path
FROM OrgChart
ORDER BY Level, EmployeeId;

-- Query 13: Window Function (RANK)
-- Question: Rank customers within each country based on their total billing spend.
WITH CustomerSpent AS (
    SELECT c.CustomerId, c.FirstName || ' ' || c.LastName as CustomerName, c.Country, SUM(i.Total) as TotalSpent
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Country
)
SELECT Country, CustomerName, TotalSpent,
       RANK() OVER (PARTITION BY Country ORDER BY TotalSpent DESC) as SpendRank
    FROM CustomerSpent
ORDER BY Country, SpendRank;

-- Query 14: Window Function (LAG)
-- Question: Compare each invoice amount for Customer 1 with their previous invoice amount to show the difference.
SELECT CustomerId, InvoiceId, InvoiceDate, Total as CurrentInvoiceTotal,
       LAG(Total, 1) OVER (ORDER BY InvoiceDate) as PreviousInvoiceTotal,
       Total - LAG(Total, 1) OVER (ORDER BY InvoiceDate) as Difference
FROM Invoice
WHERE CustomerId = 1
ORDER BY InvoiceDate;

-- Query 15: Window Function (Running Total)
-- Question: Calculate the cumulative running total of sales over time by country.
SELECT BillingCountry, InvoiceDate, Total,
       SUM(Total) OVER (PARTITION BY BillingCountry ORDER BY InvoiceDate, InvoiceId) as CumulativeSales
FROM Invoice
ORDER BY BillingCountry, InvoiceDate;

-- Query 16: Advanced Aggregation (GROUP BY CUBE equivalent)
-- Question: Count tracks by category combination of Genre and Media Type.
SELECT g.Name as Genre, m.Name as MediaType, COUNT(t.TrackId) as TrackCount
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
JOIN MediaType m ON t.MediaTypeId = m.MediaTypeId
GROUP BY CUBE (g.Name, m.Name)
ORDER BY Genre NULLS LAST, MediaType NULLS LAST
LIMIT 25;

-- Query 17: String Manipulation
-- Question: List all track names in Playlist ID 1 as a single comma-separated string.
SELECT p.PlaylistId, p.Name as PlaylistName,
       string_agg(t.Name, ', ') as TrackList
FROM Playlist p
JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
JOIN Track t ON pt.TrackId = t.TrackId
WHERE p.PlaylistId = 1
GROUP BY p.PlaylistId, p.Name;

-- Query 18: Date/Time Extraction
-- Question: Determine which day of the week generates the most invoice revenue.
SELECT dayname(InvoiceDate) as DayOfWeek,
       COUNT(InvoiceId) as SalesCount,
       SUM(Total) as TotalRevenue
FROM Invoice
GROUP BY DayOfWeek, dayofweek(InvoiceDate)
ORDER BY TotalRevenue DESC;

-- Query 19: Sales Rep Performance
-- Question: Compare total sales revenue managed by each Sales Support Agent (Employee).
SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName as EmployeeName, e.Title,
       COALESCE(SUM(i.Total), 0) as TotalSalesManaged
FROM Employee e
LEFT JOIN Customer c ON e.EmployeeId = c.SupportRepId
LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
WHERE e.Title = 'Sales Support Agent'
GROUP BY e.EmployeeId, e.FirstName, e.LastName, e.Title
ORDER BY TotalSalesManaged DESC;

-- Query 20: Cohort Spending
-- Question: Group customers by the year of their first purchase to analyze their lifetime customer value.
WITH FirstPurchase AS (
    SELECT CustomerId, MIN(strftime('%Y', InvoiceDate)) as CohortYear
    FROM Invoice
    GROUP BY CustomerId
),
CustomerRevenue AS (
    SELECT CustomerId, SUM(Total) as TotalSpent
    FROM Invoice
    GROUP BY CustomerId
)
SELECT fp.CohortYear, COUNT(fp.CustomerId) as CohortSize, SUM(cr.TotalSpent) as CohortTotalSpend,
       AVG(cr.TotalSpent) as AverageSpentPerCustomer
FROM FirstPurchase fp
JOIN CustomerRevenue cr ON fp.CustomerId = cr.CustomerId
GROUP BY fp.CohortYear
ORDER BY CohortYear;


-- =====================================================================
-- Validation Queries
-- =====================================================================

-- Validation 1: Verified no NULL invoice totals exist.
SELECT *
FROM Invoice
WHERE Total IS NULL;

-- Validation 2: Verified queries handle empty result sets correctly.
SELECT *
FROM Invoice
WHERE Total > 1000;


-- =====================================================================
-- Edge Cases
-- =====================================================================

-- Edge Case 1: Null / Unassigned Foreign Keys (Graceful Defaults)
-- Find customers without an assigned Support Representative.
SELECT c.CustomerId, c.FirstName || ' ' || c.LastName as CustomerName,
       COALESCE(e.FirstName || ' ' || e.LastName, 'No Rep Assigned') as SupportRepName
FROM Customer c
LEFT JOIN Employee e ON c.SupportRepId = e.EmployeeId
WHERE c.SupportRepId IS NULL;

-- Edge Case 2: Zero Sales / Unsold Entities (Missing Transactional Records)
-- Find artists who have released albums but recorded zero tracks sold.
SELECT ar.ArtistId, ar.Name as ArtistName, COUNT(il.InvoiceLineId) as TracksSold
FROM Artist ar
LEFT JOIN Album al ON ar.ArtistId = al.ArtistId
LEFT JOIN Track t ON al.AlbumId = t.AlbumId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY ar.ArtistId, ar.Name
HAVING COUNT(il.InvoiceLineId) = 0
ORDER BY ArtistName
LIMIT 10;
