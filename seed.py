import random
from faker import Faker
from google.cloud import bigquery
import pandas as pd

fake = Faker()

PROJECT_ID = "project-4a015a49-6bde-48f1-a3c"
DATASET_ID = "niyyahtrack"

client = bigquery.Client(project=PROJECT_ID)

def load_table(table_name, rows):
    df = pd.DataFrame(rows)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()
    print(f"Loaded {len(rows)} rows into {table_ref}")

# DONOR
donors = [
    {
        "donor_id": i,
        "donor_first_name": fake.first_name(),
        "donor_last_name": fake.last_name(),
        "donor_phone": fake.numerify(text="###-###-####"),
        "donor_email": fake.email(),
    }
    for i in range(1, 51)
]
load_table("donor", donors)

# CHARITY
charities = [
    {
        "charity_id": i,
        "charity_name": fake.company(),
        "charity_phone": fake.numerify(text="###-###-####"),
        "charity_email": fake.email(),
    }
    for i in range(1, 51)
]
load_table("charity", charities)

# PROJECT
projects = [
    {
        "project_id": i,
        "project_name": fake.bs(),
        "project_description": fake.text(),
        "charity_id": fake.random_int(min=1, max=50),
    }
    for i in range(1, 51)
]
load_table("project", projects)

# TESTIMONIALS
testimonials = [
    {
        "testimonial_id": i,
        "testimonial_title": fake.sentence(),
        "testimonial_date": str(fake.date()),
        "testimonial_content": fake.text(),
        "testimonial_author": fake.name(),
        "project_id": fake.random_int(min=1, max=50),
    }
    for i in range(1, 51)
]
load_table("testimonials", testimonials)

# DONATION
donations = [
    {
        "donation_id": i,
        "donation_confirmation": fake.bothify(text="TXN-####-??##"),
        "donation_amount": float(fake.pydecimal(left_digits=5, right_digits=2, positive=True)),
        "donation_date": str(fake.date_this_decade()),
        "donation_type": random.choice(["zakat", "sadaqah", "sadaqah_jariya", "waqf"]),
        "donor_id": fake.random_int(min=1, max=50),
        "charity_id": fake.random_int(min=1, max=50),
        "project_id": fake.random_int(min=1, max=50),
    }
    for i in range(1, 51)
]
load_table("donation", donations)

print("All tables seeded successfully.")