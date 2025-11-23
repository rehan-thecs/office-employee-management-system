import os
import django
import csv
from datetime import datetime

# 1. Setup Django Environment
# This allows us to use models outside of running the server
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'office_management.settings')
django.setup()

# 2. Import your models
from app.models import Employee, Role, Department

def run_seed():
    print("--- Starting Data Import ---")

    # ----------------------------------------
    # PART 1: Import Departments
    # ----------------------------------------
    print("Importing Departments...")
    with open('departments.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Department.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'location': row['location']
                }
            )
    print("✓ Departments added.")

    # ----------------------------------------
    # PART 2: Import Roles
    # ----------------------------------------
    print("Importing Roles...")
    with open('roles.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Role.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name']
                }
            )
    print("✓ Roles added.")

    # ----------------------------------------
    # PART 3: Import Employees
    # ----------------------------------------
    print("Importing Employees (This may take a moment)...")
    employee_count = 0
    
    with open('employees.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # We need to find the actual Department and Role objects
            # based on the IDs in the CSV
            try:
                dept_obj = Department.objects.get(id=row['dept_id'])
                role_obj = Role.objects.get(id=row['role_id'])

                # Parse date string "2023-01-01" into a Python Date object
                h_date = datetime.strptime(row['hire_date'], '%Y-%m-%d').date()

                Employee.objects.get_or_create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    defaults={
                        'salary': int(row['salary']),
                        'bonus': int(row['bonus']),
                        'phone': int(row['phone']),
                        'dept': dept_obj,
                        'role': role_obj,
                        'hire_date': h_date
                    }
                )
                employee_count += 1
            except Exception as e:
                print(f"Error adding {row['first_name']}: {e}")

    print(f"✓ Successfully added {employee_count} employees.")
    print("--- Data Import Complete ---")

if __name__ == '__main__':
    run_seed()