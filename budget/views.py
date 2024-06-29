from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from budget.forms import ExpenseForm,IncomeForm,RegistrationForm,LoginForm,SummaryForm

from budget.models import Expense,Income

from django.contrib import messages

from django.utils import timezone

from django.db.models import Sum 

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from budget.decorators import signin_required

import datetime

# function decorator => method decorator

@method_decorator(signin_required,name='dispatch')
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        # if not request.user.is_authenticated:

        #     messages.error(request,"invalid session please login")

        #     return redirect("signin")

        form_instance=ExpenseForm()

        # qs=Expense.objects.all() expense shown for all

        qs=Expense.objects.filter(user_object=request.user).order_by("-created_date")

        # expense shown for user logged in

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        # if not request.user.is_authenticated:

        #     messages.error(request,"invalid session please login")

        #     return redirect("signin")

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user
            # (in modelform only)

            form_instance.save() 

            messages.success(request,"expense has been created")

            # data=form_instance.cleaned_data


            # print("exp has been created")

            return redirect("expense-add")
        
        else:

            return render(request,"expense_add.html",{"form":form_instance})
        
@method_decorator(signin_required,name="dispatch")
        
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("dinner")

        expense_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_obj)

        return render(request,"expense_edit.html",{"form":form_instance})  

    def post(self,request,*args,**kwargs):

        id=kwargs.get("dinner")

        expense_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_obj,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense updated")

            return redirect("expense-add")

        else:

            messages.error(request," msg not updated")

            return render(request,"expense_add.html",{"form":form_instance})

@method_decorator(signin_required,name='dispatch')

class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=IncomeForm()

        # qs=Income.objects.all()

        qs=Income.objects.filter(user_object=request.user).order_by("-created_date")


        return render(request,"income_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=IncomeForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user


            form_instance.save()

            messages.success(request,"income has been created")

            # print("no msg yet")

            # return redirect("income-add")

            return redirect("income-add")
        
        else:

            return render(request,"income_add.html",{"form":form_instance})
        
@method_decorator(signin_required,name='dispatch')
class IncomeUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("dinner")

        income_obj=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_obj)

        return render(request,"income_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("dinner")

        income_obj=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_obj,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"income updated")

            return redirect("income-add")
        
        else:

            return render(request,"income_add.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})      


@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"msg deleted")

        return redirect("expense-add")      

@method_decorator(signin_required,name='dispatch')
class IncomeDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Income.objects.get(id=id)

        return render(request,"income_detail.html",{"data":qs})

@method_decorator(signin_required,name='dispatch')
class IncomeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Income.objects.get(id=id).delete()

        messages.success(request,"deleted")

        return redirect("income-add")

@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(

                created_date__month=current_month,

                created_date__year=current_year,

                user_object=request.user

            )

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        category_summary=expense_list.values("category").annotate(total=Sum("amount"))

        priority_summary=expense_list.values("priority").annotate(total=Sum("amount"))

        print(priority_summary)

        print(category_summary)

        data={

            "expense_total":expense_total,

            "category_summary":category_summary,

            "priority_summary":priority_summary,
            
        }

        return render(request,"expense_summary.html",data)

        # return redirect("expense-add")

@method_decorator(signin_required,name='dispatch')

class IncomeSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        income_list=Income.objects.filter(

            created_date__month=current_month,

            created_date__year=current_year

        )

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(income_total)

        category_total=income_list.values("category").annotate(total=Sum("amount"))

        print(category_total)

        data={
            
            "income_total":income_total,

            "category_total":category_total


        }

        return render(request,"income_summary.html",data)

        # return redirect("income-add")

        # authentication

            # 1)registration

            # 2)login

            # 3)logout

# store user details

# (username,email,first_name,last_name,password)

# step1: create a model for entering details

# step2:makemigrations & migrate(in database)

# step3:create a registration form

# step4:create view

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save() user.objects.create password will not be encrypted

            data=form_instance.cleaned_data
            # password will be encrypted=>create_user
            User.objects.create_user(**data)

            print("user created")

            return redirect("signin")
        
        else:

            print("creation failed")

            return render(request,"register.html",{"form":form_instance})

# login

# username,password

# step1:extract username,password from form

# step2:authenticate(chck user & pass crct or not)

# step3:session start

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            # print(uname,pwd)

            user_obj=authenticate(request,username=uname,password=pwd)

            # print("user",user_obj)

            if user_obj:

                login(request,user_obj)
                
                # return redirect("expense-add")

                return redirect("dashboard")
            
        messages.error(request,"invalid credential")

        return render(request,"login.html",{"form":form_instance})
        
# session start

@method_decorator(signin_required,name="dispatch")

class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SummaryForm()

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(

            user_object=request.user,

            created_date__month=current_month,

            created_date__year=current_year

            )
        
        income_list=Income.objects.filter(

            user_object=request.user,

            created_date__month=current_month,

            created_date__year=current_year

            )

        print("expense list met",expense_list)

        print("income list",income_list)

        expense_total=expense_list.values('amount').aggregate(total=Sum('amount'))

        income_total=income_list.values('amount').aggregate(total=Sum('amount'))

        print("total exp",expense_total)

        print("total inc",income_total)

        monthly_expense={}

        monthly_income={}

        for month in range(1,13):

            start_date=datetime.date(current_year,month,1)

            if month==12:

                end_date=datetime.date(current_year+1,1,1)

            else:

                end_date=datetime.date(current_year,month+1,1)

            monthly_expense_total=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum("amount"))['total']

            monthly_expense[start_date.strftime('%B')]=monthly_expense_total if monthly_expense_total else 0

            monthly_income_total=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum("amount"))['total']

            monthly_income[start_date.strftime('%B')]=monthly_income_total if monthly_income_total else 0

        print(monthly_expense)

        print(monthly_income)

        return render(request,"dashboard.html",{
            
            "expense":expense_total,
            
            "income":income_total,
            
            "form":form_instance,

            "monthly_income":monthly_income,
            
            "monthly_expense":monthly_expense})
    
    def post(self,request,*args,**kwargs):

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")

            expense_list=Expense.objects.filter(

            user_object=request.user,

            created_date__gte=start_date,

            created_date__lte=end_date

            )
        
        income_list=Income.objects.filter(

            user_object=request.user,

            created_date__gte=start_date,

            created_date__lte=end_date

            )

        print("expense list met",expense_list)

        print("income list",income_list)

        expense_total=expense_list.values('amount').aggregate(total=Sum('amount'))

        income_total=income_list.values('amount').aggregate(total=Sum('amount'))

        print("total exp",expense_total)

        print("total inc",income_total)

        return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance})
    




    

    
    





    
        

        

    
    
