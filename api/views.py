from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.views import APIView

from api.serializers import UserSerializer,IncomeSerializer,ExpenseSerializer

from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication

from rest_framework import permissions

from api.permissions import OwnerOnly,Owneronly

from budget.models import Income,Expense

from django.utils import timezone

from django.db.models import Sum

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)
        # deserialization

        if serializer_instance.is_valid():

            serializer_instance.save()

            # data=serializer_instance.validated_data

            # User.objects.create_user(**data)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)




class IncomeViewset(ModelViewSet):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    # permission_classes=[permissions.IsAuthenticated]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(user_object=request.user)

        serializer_instance=IncomeSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)

class IncomeSummaryView(APIView):
        

        permission_classes=[permissions.IsAuthenticated]

        authentication_classes=[authentication.TokenAuthentication]

        def get(self,request,*args,**kwargs):

            current_month=timezone.now().month

            current_year=timezone.now().year

            all_incomes=Income.objects.filter(

                user_object=request.user,

                created_date__month=current_month,

                created_date__year=current_year
            )

            total_income=all_incomes.values("amount").aggregate(total=Sum("amount"))

            total_category=all_incomes.values("category").annotate(total=Sum("amount"))

            data={

                "total_income":total_income,

                "total_category":total_category
            }

            return Response(data=data)



class ExpenseViewset(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    # permission_classes=[permissions.IsAuthenticated]

    permission_classes=[Owneronly]

    def list(self,request,*args,**kwargs):

        qs=Expense.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)

class ExpenseSummaryView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expenses=Expense.objects.filter(

            user_object=request.user,

            created_date__month=current_month,

            created_date__year=current_year

        )

        total_expense=all_expenses.values("amount").aggregate(total=Sum("amount"))

        category_expense=all_expenses.values("category").annotate(total=Sum("amount"))

        priority_summary=all_expenses.values("priority").annotate(total=Sum("amount"))

        data={

            "total_expense":total_expense,

            "category_expense":category_expense,

            "priority_summary": priority_summary,
        }

        return Response(data=data)