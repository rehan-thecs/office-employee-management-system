from django.shortcuts import render, HttpResponse
from django.db.models import Q
from .models import Employee, Role, Department
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    
    context = {
        'emps': emps
    }
    return render(request, 'all_emp.html', context)

def add_emp(request):
    if request.method == ' POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')
        dept_name = request.POST.get('dept')
        role_name = request.POST.get('role')
        hire_date = request.POST.get('hire_date')

        if not first_name or not last_name or not phone:
            return HttpResponse("Error: Name and Phone are required fields.")

        try:
            department_obj, created = Department.objects.get_or_create(
                name=dept_name,
                defaults={'location': 'Mumbai'}
            )
            
            role_obj, created = Role.objects.get_or_create(name=role_name)

            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=int(salary),
                bonus=int(bonus) if bonus else 0,
                phone=int(phone),
                dept=department_obj,
                role=role_obj,
                hire_date=hire_date
            )
            new_emp.save()

            return HttpResponse("Employee added successfully! <a href='/'>Go back to Home</a>")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("Invalid Request Method")

def remove_emp(request, emp_id=0):
    if request.method == 'POST':
        try:
            emp_id = request.POST.get('emp_id')
            emp_to_remove = Employee.objects.get(id=emp_id)
            emp_to_remove.delete()
            return HttpResponse("Employee Removed Successfully! <a href='/'>Return to Home</a>")
        except Employee.DoesNotExist:
            return HttpResponse("Error: Please select a valid employee.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'remove_emp.html', context)



def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )

        if dept:
            emps = emps.filter(dept__name__icontains=dept)

        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {'emps': emps}
        return render(request, 'filter_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')

    else:
        return HttpResponse("Invalid Request")
