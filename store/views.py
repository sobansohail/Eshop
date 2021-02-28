from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# Create your views here.
def index(request):
  if request.method=='GET':      
    cart=request.session.get('cart')
    if not cart:
          request.session['cart']={}
    products=None
    categories=Category.get_all_categories()
    categoryID=request.GET.get('category')
    if categoryID:
        products=Product.get_all_products_by_categoryid(categoryID)
    else:
        products=Product.get_all_products()
    data={}
    data['products']=products
    data['categories']=categories
    return render(request,'index.html', data)
  else:
      product=request.POST.get('product')  
      remove=request.POST.get('remove')
      cart=request.session.get('cart')
      if cart:
            quantity=cart.get(product)
            if quantity:  
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product]=quantity+1    
            else:
                 cart[product]=1 
      else:
        cart={}
        cart[product]=1

      request.session['cart']=cart
     

      return redirect('homepage')
 
  if cart:
      quantity=cart.get(product)
      if quantity:
          cart[product]=quantity+1
      else: 
          cart[product]=1
 
  else:
      cart={}
      cart[products]=1
  request.session['cart']=cart
     
def registeruser(request):
        postData=request.POST
        first_name=postData.get('firstname')
        last_name=postData.get('lastname')
        phone=postData.get('phone')
        email=postData.get('email')
        password=postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
           
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
    
def signup(request):
    if request.method=='GET':
        return render(request , 'signup.html')
    else :
        return registeruser(request)
   

def validateCustomer(customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 3:
            error_message = 'First Name must atleast be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 3:
            error_message = 'Last Name must atleast be 3 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 11:
            error_message = 'Phone Number must be 11 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message        
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
         email=request.POST.get('email')
         password=request.POST.get('password')
         customer=Customer.get_customer_by_email(email)
         error_message=None
         if customer:
             flag=check_password(password, customer.password)
             if flag:
                 request.session['customer']=customer.id
                 request.session['email']=customer.email
                 return redirect('homepage')
             else:
                error_message='Email or Password is invalid !!'
         else:
             error_message='Email or Password is invalid !!'
         return render(request, 'login.html',{'error':error_message})
def logout(request):
    request.session.clear()
    return redirect('login')   

def cart(request):
     if request.method=='GET':
         ids= list(request.session.get('cart').keys())
         products=Product.get_products_by_id(ids)
         

         return render(request,'cart.html',{'products':products})

def checkout(request):
    if request.method=='GET':
        return render(request,'checkout.html')

def end(request):
    if request.method=='GET':
         
        return render(request,'end.html')


