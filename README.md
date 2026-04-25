# NiyyahTrack — Zakat & Charity Analytics Pipeline

## Overview
Niyyah Tracks is an analytics engineering project designed to model and analyze charitable giving data. The system transforms raw data related to donations, projects, donors, and testimonials into structured models and meaningful metrics that evaluate the impact and efficiency of charitable initiatives.
<br><br>
This project focuses on building a clean data pipeline using dbt and PostgreSQL, following best practices in data modeling and analytics engineering.

## Objectives
- Design a relational database for tracking charity and zakat data
- Transform raw data into clean, analysis-ready models
- Define meaningful business metrics for evaluating impact
- Apply analytics engineering workflows using dbt
  
## Data Model
The system is built around the following core entities:
- **Projects** — charitable initiatives
- **Donations** — contributions made toward projects
- **Donors** — individuals making donations
- **Testimonials** — qualitative feedback linked to projects

## ERD
![Niyyah Tracks ERD](./assets/niyyah_tracks_erd.png)
This schema models the relationships between donors, projects, donations, and testimonials, enabling structured analysis of charitable impact and efficiency.
## Tech Stack
- **PostgreSQL** — relational database for raw data storage
- **Python** (psycopg2, Faker) — synthetic data generation and database seeding
- **dbt** (data build tool) — data transformation and modelling
- **pgAdmin 4** — database management and query execution

## dbt Pipeline
The project follows a layered dbt architecture:<br>
**1. Staging Layer:** 5 models — one per raw table<br>
**2. Mart Layer**
- `dim_donors` — donor dimension table
- `dim_projects` — project dimension table with charity name joined in
- `fct_donations` — fact table joining donations with donor, project, and charity info

## Analysis Queries
Five analysis queries built on top of `fct_donations`:

1. **Total raised per project** — which projects attract the most donations
2. **Total donations by type** — breakdown across zakat, sadaqah, sadaqah jariya, waqf
3. **Total raised per charity** — which charities raise the most
4. **Repeat donors** — donors who gave more than once (retention metric)
5. **Cost per beneficiary** — total raised per project divided by number of testimonials (impact metric)

### Example Queries
```sql
-- Cost per beneficiary
WITH total_donations AS (
    SELECT project_name, SUM(donation_amount) AS total_raised
    FROM fct_donations
    GROUP BY project_name
),
count_testimonials AS (
    SELECT COUNT(testimonial_id) AS testimonial_count, p.project_name
    FROM stg_testimonials s
    JOIN dim_projects p ON s.project_id = p.project_id
    GROUP BY p.project_name
)
SELECT c.project_name, total_raised, testimonial_count,
    ROUND(total_raised/testimonial_count::numeric, 2) AS cost_per_beneficiary
FROM count_testimonials c
JOIN total_donations ON c.project_name = total_donations.project_name
```

## Key Metric
#### Cost per Beneficiary
A derived metric used to evaluate the efficiency of charitable projects:
`cost_per_beneficiary = total_donations ÷ number_of_testimonials`
This metric provides a proxy for impact by comparing financial input to recorded outcomes.
## Setup
#### Prerequisites
- PostgreSQL 18
- Python 3.11+
- dbt-postgres
#### Installation
`pip install psycopg2-binary faker python-dotenv dbt-postgres`
#### Environment Variables
Create a .env file in the project root:
`DB_PASSWORD=your_postgres_password`
#### Database Setup
Run the schema file in pgAdmin or psql:
`\i sql/schema.sql`
#### Seed Data
`python data/seed.py`
#### dbt
```git 
cd niyyah_dbt
dbt run
```

## Key Learnings
- Built an end-to-end analytics pipeline using dbt and PostgreSQL  
- Designed a relational schema to model donations, projects, and testimonials  
- Applied layered data modeling (staging → marts) using `source()` and `ref()`  
- Developed business-oriented metrics such as cost per beneficiary  
- Strengthened SQL skills including joins, aggregations, and CTEs  
- Learned how to structure data for meaningful analysis rather than raw querying  
