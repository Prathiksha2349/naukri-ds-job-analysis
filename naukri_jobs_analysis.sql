CREATE DATABASE naukri_project;
USE naukri_project;


CREATE TABLE naukri_jobs (
    -- Original columns kept by your script
    title VARCHAR(255),
    companyName VARCHAR(255),
    location VARCHAR(255),
    experience VARCHAR(255),
    salary VARCHAR(255),
    skills TEXT,
    company_rating VARCHAR(50),
    createdDate DATETIME, -- Saved directly as standard string format by Pandas
    
    -- Cleaned columns added by your functions
    title_clean VARCHAR(255),
    experience_clean VARCHAR(255),
    sal_min DECIMAL(10,2) NULL,
    sal_max DECIMAL(10,2) NULL,
    sal_mid DECIMAL(10,2) NULL,
    city VARCHAR(255),
    
    -- The 14 exact skill flag columns added in Block G
    skill_python INT DEFAULT 0,
    skill_sql INT DEFAULT 0,
    skill_machine_learning INT DEFAULT 0,
    skill_deep_learning INT DEFAULT 0,
    skill_power_bi INT DEFAULT 0,
    skill_tableau INT DEFAULT 0,
    skill_nlp INT DEFAULT 0,
    skill_azure INT DEFAULT 0,
    skill_aws INT DEFAULT 0,
    skill_spark INT DEFAULT 0,
    skill_tensorflow INT DEFAULT 0,
    skill_pytorch INT DEFAULT 0,
    skill_excel INT DEFAULT 0,
    skill_statistics INT DEFAULT 0
);

-- Step 1: Allow local data loading for this connection session
SET GLOBAL local_infile = 1;

-- Step 2: Clear existing data rows if any previous failed imports are hanging out
TRUNCATE TABLE naukri_jobs;

-- Step 3: Run the direct loader with your precise Windows file location
LOAD DATA LOCAL INFILE 'C:/Users/prath/Desktop/naukri-ds-job-analysis/Data/naukri_cleaned.csv'
INTO TABLE naukri_jobs
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n' -- Matches the specific row endings of a Windows text file
IGNORE 1 LINES;            -- Safely bypasses your column names text row

-- Q1: Job count by role
SELECT title_clean, COUNT(*) AS total_jobs
FROM naukri_jobs
GROUP BY title_clean ORDER BY total_jobs DESC;

-- Q2: Average salary by role (disclosed only)
SELECT title_clean,
       COUNT(*) AS jobs_with_salary,
       ROUND(AVG(sal_mid),1) AS avg_salary_lpa
FROM naukri_jobs
WHERE sal_mid IS NOT NULL
GROUP BY title_clean HAVING jobs_with_salary >= 5
ORDER BY avg_salary_lpa DESC;

-- Q3: Top 10 hiring cities
SELECT city, COUNT(*) AS openings
FROM naukri_jobs
WHERE city NOT IN ('Remote','Unknown')
GROUP BY city ORDER BY openings DESC LIMIT 10;

-- Q4: Experience level demand
SELECT experience_clean, COUNT(*) AS jobs
FROM naukri_jobs
GROUP BY experience_clean ORDER BY jobs DESC;

-- Q5: Salary transparency by city
SELECT city,
       COUNT(*) AS total,
       SUM(CASE WHEN sal_mid IS NOT NULL THEN 1 ELSE 0 END) AS disclosed,
       ROUND(SUM(CASE WHEN sal_mid IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_disclosed
FROM naukri_jobs
WHERE city NOT IN ('Remote','Unknown')
GROUP BY city HAVING total >= 50
ORDER BY pct_disclosed DESC;

-- Q6: Top 15 companies hiring
SELECT companyName, COUNT(*) AS openings
FROM naukri_jobs
GROUP BY companyName ORDER BY openings DESC LIMIT 15;

-- Q7: Salary by experience (disclosed only)
SELECT experience_clean,
       ROUND(AVG(sal_mid),1) AS avg_salary,
       ROUND(MIN(sal_mid),1) AS min_sal,
       ROUND(MAX(sal_mid),1) AS max_sal,
       COUNT(*) AS count
FROM naukri_jobs
WHERE sal_mid IS NOT NULL AND experience_clean != 'Unknown'
GROUP BY experience_clean ORDER BY avg_salary;

-- Q8: Which city has highest avg salary?
SELECT city, ROUND(AVG(sal_mid),1) AS avg_salary, COUNT(*) AS count
FROM naukri_jobs
WHERE sal_mid IS NOT NULL AND city NOT IN ('Remote','Unknown')
GROUP BY city HAVING count >= 5
ORDER BY avg_salary DESC LIMIT 10;

-- Q9: Python vs SQL demand by city
SELECT city,
       SUM(skill_python) AS python_jobs,
       SUM(skill_sql) AS sql_jobs,
       COUNT(*) AS total
FROM naukri_jobs
WHERE city NOT IN ('Remote','Unknown')
GROUP BY city HAVING total >= 100
ORDER BY total DESC;

-- Q10: Jobs posted by month (trend)
SELECT DATE_FORMAT(createdDate, '%Y-%m') AS month,
       COUNT(*) AS jobs_posted
FROM naukri_jobs
WHERE createdDate IS NOT NULL
GROUP BY month ORDER BY month;