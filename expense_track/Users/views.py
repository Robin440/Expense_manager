from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Category, Expense
from django.utils import timezone
from datetime import datetime
from django.db.models import Q


def landing_page(request):
    if 'username' in request.session:
        return redirect(home)
    return render(request,'landing_page.html')

def user_login(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found')
            return render(request, 'login.html')
        if user.email== email and user.password==passw:
            login(request, user)
            request.session['username'] = email
            return redirect(home)  
        messages.error(request, 'Invalid login credentials')
        return render(request, 'login.html')

    return render(request, 'login.html')

    
  



def user_registration(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not (username and first_name and last_name and email and password and confirm_password):
            messages.error(request, 'All fields are required')
            return render(request, 'registration.html')

       
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'registration.html')

        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'Username or email already exists')
            return render(request, 'registration.html')

        
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        messages.success(request, 'User registered successfully!')
       
        return redirect('user_login_page')

    return render(request, 'registration.html')

@login_required
def home(request):
    if 'username' in request.session:
        user_email = request.session['username']
        user_instance = User.objects.filter(email=user_email).first()
        
    if user_instance:
        is_member = not user_instance.is_superuser
       
        categories = Category.objects.all()

        if is_member:
            expenses_data = Expense.objects.filter(created_by=user_instance)
            return render(request, 'home.html', {'expenses': expenses_data, 'categories': categories})
        else:
            expenses_data = Expense.objects.all()
            return render(request, 'home.html', {'expenses': expenses_data, 'categories': categories})


    return redirect(user_login)


def logout(request):

    if 'username' in request.session:
        
        request.session.flush()
    return redirect(user_login)


@login_required
def new_expenses(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        date_of_expense = request.POST.get('date_of_expense')
        amount = request.POST.get('amount')

        
        # Create the Expense object
        expense = Expense.objects.create(
            name=name,
            description=description,
            category=category,
            date_of_expense=date_of_expense,
            amount=amount,
            created_by=request.user  # Assuming you have user authentication in place
        )

        messages.success(request, 'Expense created successfully!')
        
       
        return redirect(home)  

    return redirect(home) 

@login_required
def edit_expense(request, expense_id):
    exp = get_object_or_404(Expense, pk=expense_id)
    categories = Category.objects.all()
    

    if request.method == 'POST':
        # Retrieve the updated values from the request
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        date_of_expense = request.POST.get('date_of_expense')
        amount = request.POST.get('amount')

        # Update the expense fields
        exp.name = name
        exp.description = description
        exp.category = category
        exp.date_of_expense = date_of_expense
        exp.amount = amount

        # Save the updated expense
        exp.save()

        messages.success(request, 'Expense updated successfully!')
        return redirect(home)

    # Update the updated_at field even if the form is not submitted
    exp.updated_at = timezone.now()
    exp.save()

    return render(request, 'edit.html', {'expense': exp, 'category': categories})

@login_required
def filter_expenses_by_date(request):
    if request.method=='POST':
        selected_date = request.POST.get('date_input')
        print(f'date = {selected_date}')

    
 
        filtered_expenses = Expense.objects.filter(date_of_expense=selected_date)
        for i in filtered_expenses:
            print(f'filterd {i.name}')

        return render(request, 'filter_date.html', {'filtered_expenses': filtered_expenses})
  
    return render(request, 'filter_date.html',)


@login_required
def search_expenses(request):
    if request.method == 'POST':
        search_input = request.POST.get('search_input')
        print(f'search input = {search_input}')

       
        if search_input is not None:
            filtered_results = Expense.objects.filter(Q(name__icontains=search_input) | Q(category__name__icontains=search_input))

            

           
            return render(request, 'filter_name.html', {'filtered_expenses': filtered_results, 'search_input': search_input})

    return render(request, 'filter_name.html')


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()

    return redirect(home)
    