from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from product.models import Category, Product 
from warehouseStore.models import *
from django.utils import timezone
from django.db.models import Sum, F
from order.models import *
import random

def view(request):
    response = HttpResponse("hello")
    response.set_cookie('device')
    return response



def checkout(request):
    if request.user.is_authenticated:
        cur_user = request.user.username
        cart = cart_list = Cart.objects.values('p__p_name', 'p__instore_price', 'quantity').filter(m = cur_user)
        total = cart.annotate(tot = F('p__instore_price') * F('quantity')).aggregate(Sum('tot'))
        user_info = Member.objects.get(m_id=cur_user)
        enough_bal = True
        if request.method == "POST":
            if request.POST.get('card'):
                card_num = request.POST['card']
                balance = Membercardinfo.objects.get(m = cur_user, card_num = card_num)
                if balance.balance > total['tot__sum']:
                    balance.balance = round(balance.balance - total['tot__sum'], 2)
                    balance.save()
                else:
                    enough_bal = False
            else:
                card_num = request.POST['cardnumber']
                
            if request.POST.get('address'):
                address_info = Memberaddress.objects.get(m=user_info, address1=request.POST.get('address', ''))
                address1 = address_info.address1
                address2 = address_info.address2
                state = address_info.state
                zipcode = address_info.zipcode
            else:
                address1 = request.POST['street']
                address2 = request.POST['box']
                state = request.POST.get('state')
                zipcode=request.POST['zip']
                print(address1, address2, state, zipcode)
            
            if enough_bal:              
                new_ord = Orderlist(order_date=timezone.now())
                new_ord.save()
                cart_list = Cart.objects.filter(m = cur_user)
                t = timezone.now()
                tracking_num = str(t)+str(new_ord.order_id)  
                for cart in cart_list:
                    w = Warehouseinv.objects.get(p= cart.p)
                    w.quantity -= cart.quantity
                    
                    if w.quantity < 0:
                        return redirect('/')
                    else:
                        w.save()
            
                    new_online_ord = Onlineorder(
                        order=new_ord,
                        p = cart.p,
                        order_date=t,
                        quantity = cart.quantity,
                        customer_type = user_info.type,
                        m = user_info,
                        email = user_info.email,
                        card_info = card_num,
                        address1 = address1,
                        address2 = address2,
                        state = state,
                        zip_code= zipcode,
                        phone_num = user_info.phone,
                        recipient_name= request.POST['r_name'],
                        recipient_phone= request.POST['r_phone'],
                        sc = None,
                        tracking_num= tracking_num
                    )
                    new_online_ord.save()
    
                Cart.objects.filter(m=cur_user).delete()
            else:
                return redirect('/')
                    
            return render(request, "thankyou.html", {'tracking_num':tracking_num})
        else:
            card = Membercardinfo.objects.filter(m = cur_user)
            address = Memberaddress.objects.filter(m = cur_user)
            print(total)
            context = {"cart_list": cart,
                        "total": total,
                        "card_list" : card,
                        "address_list" : address}
            return render(request, "checkout.html", context)
            
    else:
        cur_user = request.COOKIES['device']
        if request.method == "POST":
            new_ord = Orderlist(order_date=timezone.now())
            new_ord.save()
            cart_list = Cart.objects.filter(m = cur_user)
            t = timezone.now()
            tracking_num = str(t)+str(new_ord.order_id)  
            for cart in cart_list:
                w = Warehouseinv.objects.get(p= cart.p)
                w.quantity -= cart.quantity
                
                if w.quantity < 0:
                    return render('/')
                else:
                    w.save()
                
                new_online_ord = Onlineorder(
                    order=new_ord,
                    p = cart.p,
                    order_date= t,
                    quantity = cart.quantity,
                    customer_type = None,
                    m = None,
                    email = None,
                    card_info = request.POST['cardnumber'],
                    address1 = request.POST['street'],
                    address2 = request.POST['box'],
                    state = request.POST['state'],
                    zip_code=request.POST['zip'],
                    phone_num = request.POST['phone'],
                    recipient_name= request.POST['r_name'],
                    recipient_phone= request.POST['r_phone'],
                    sc = None,
                    tracking_num= tracking_num
                )
                new_online_ord.save()
            Cart.objects.filter(m=cur_user).delete()
            return render(request, "thankyou.html", {'tracking_num':tracking_num})
         
        else: 
            cur_user = request.COOKIES['device']
            cart = cart_list = Cart.objects.values('p__p_name', 'p__instore_price', 'quantity').filter(m = cur_user)
            total = cart.annotate(tot = F('p__instore_price') * F('quantity')).aggregate(Sum('tot'))
            card = Membercardinfo.objects.filter(m = cur_user)
            address = Memberaddress.objects.filter(m = cur_user)
            print(total)
            context = {"cart_list": cart,
                        "total": total,
                        "card" : card,
                        "address" : address}
            return render(request, "checkout.html", context)
    
        
def cart_delete(request, p_id):
    c = Cart.objects.get(p = p_id)
    c.delete()
    print(c)
    return redirect('/cart')

def cart_plus(request, p_id):
    c = Cart.objects.get(p = p_id)
    c.quantity += 1
    c.save()
    return redirect('/cart')

def cart_minus(request, p_id):
    c = Cart.objects.get(p = p_id)
    c.quantity -= 1
    if c.quantity  == 0 :
        cart_delete(request, p_id)
    else:
        c.save()
    return redirect('/cart')

def product_detail(request, p_id):
    product = Product.objects.values('p_id','p_name','category', 'instore_price', 'manufacturer_id__manufacturer_name').get(p_id = p_id)
    whi = Warehouseinv.objects.values('quantity').get(p = p_id)
    
    if request.method == "POST":
        cur_user = ""
        if request.user.is_authenticated:    
            cur_user = request.user.username
        else:
            cur_user = request.COOKIES['device']
        mem = Member.objects.get(m_id = cur_user)
        prd = Product.objects.get(p_id = p_id)
        quan = request.POST.get('quantity', 0)
        c = Cart.objects.filter(m = mem, p = prd)
        try:
            if c:
                new_c = Cart(
                    m = mem, 
                    p = prd,
                    quantity = c[0].quantity + int(quan)
                )
                c[0].delete()
                new_c.save()
                return redirect('/cart')
            else:
                new_c2 = Cart(
                    m = mem,
                    p = prd,
                    quantity = quan
                )
                new_c2.save()
                return redirect('/cart')
        except Exception as e:
            print(e)
            return redirect('/')
        
    else:    
        return render(request, 'product_detail.html', {'product_detail' : product, "quantity": whi})


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'])
            
            auth.login(request, user)
        
            member = Member(
                m_id = request.POST['username'],
                name = request.POST['name'],
                phone = request.POST['phone'],
                email = request.POST['email'],
                type = request.POST['type'],
                user_status = 1,
                reg_date = timezone.now(),
                billing_date  = timezone.now(),
            )
            member.save()
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect. or user id does not exist'})
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

# home
def home(request):
    product_list = Product.objects.all()
    if request.method == "POST":
        if request.POST.get('category') == 'all' and request.POST.get('man') == 'all':
            product_list = Product.objects.all()
        elif request.POST.get('category') == 'all' and (not request.POST.get('man') == 'all'):
            product_list = Product.objects.filter(manufacturer=request.POST.get('man'))
        elif (not request.POST.get('category') == 'all') and request.POST.get('man') == 'all':
            product_list = Product.objects.filter(category=request.POST.get('category'))
        else:
            product_list = Product.objects.filter(manufacturer=request.POST.get('man'), category=request.POST.get('category')) 
            
    product_list = product_list.values('p_id','p_name','category', 'instore_price', 'manufacturer__manufacturer_name') 
    manufacturer_list = Manufacturer.objects.all().values('manufacturer_name', 'manufacturer_id')
    category_list = Category.objects.all().values('category')
    
    if request.user.is_authenticated:
        cur_user = request.user.username
        try: 
            store_admin = storeAdmin.objects.get(store_a_id =cur_user)
            inv = Storeinv.objects.values('p__p_name', 'quantity','p__instore_price').filter(s = store_admin.s)
            wh = Warehouseinv.objects.values('p__p_name', 'quantity', 'p').filter(w = 'w_1')
            if request.method == 'POST':
                p = Product.objects.get(p_id = request.POST['product'])
                print(p)
                q = request.POST['quantity']
                in_stock = Warehouseinv.objects.get(p=p)
                if int(q) < in_stock.quantity:
                    try:
                        store_inv = Storeinv.objects.get(s = store_admin.s, p = p)
                        store_inv.quantity += int(q)
                        store_inv.save()
                    except:
                        new_product = Storeinv(
                            s = store_admin.s,
                            p = p,
                            quantity= int(q),
                            threshold = 50
                        )
                        new_product.save()
                    
                    wh_inv = Warehouseinv.objects.get(w = 'w_1', p = p)
                    wh_inv.quantity -= int(q)
                    wh_inv.save()
                    
                    log = Restockstore(
                        s = store_admin.s,
                        w = Warehouse.objects.get(w_id = 'w_1'),
                        p = p,
                        quantity= int(q),
                        restock_date= timezone.now()
                    )
                    log.save()
                    context = {"store_inv": inv, "warehouse_inv":wh, "message" : "success"}
                    return render(request, 'store_admin.html', context) 
                else:
                    context = {"store_inv": inv, "warehouse_inv":wh, "error" : "can't request more than what we have"}
                    return render(request, 'store_admin.html', context) 
                
            else:
                context = {"store_inv": inv, "warehouse_inv":wh}
                return render(request, 'store_admin.html', context)
            
        except: 
            try:
                wh_admin = warehouseAdmin.objects.get(wh_a_id=cur_user)
                if request.method == "POST":
                    try:
                        p = Product.objects.get(p_id = request.POST['product'])
                        q = request.POST['quantity']
                        wh_inv = Warehouseinv.objects.get(w = wh_admin.w, p = p)
                        wh_inv.quantity += int(q)
                        wh_inv.save()
                        
    
                        log = Restockwarehouse(
                            w = wh_admin.w,
                            p = p,
                            quantity= int(q),
                            manufacturer= p.manufacturer,
                            restock_date = timezone.now()
                        )
                        log.save()
                    
                        inv = Warehouseinv.objects.values('p__p_name', 'quantity', 'p__manufacturer_id__manufacturer_name', 'p').filter(w = Warehouse.objects.get(w_id = 'w_1'))
                        context = {'warehouse_inv': inv, "message": "message"}
                        return render(request, 'warehouse_admin.html', context)
                    except:
                        inv = Warehouseinv.objects.values('p__p_name', 'quantity', 'p__manufacturer_id__manufacturer_name', 'p').filter(w = Warehouse.objects.get(w_id = 'w_1'))
                        context = {'warehouse_inv': inv, "error": "message"}
                        return render(request, 'warehouse_admin.html', context)
                else:
                    inv = Warehouseinv.objects.values('p__p_name', 'quantity', 'p__manufacturer_id__manufacturer_name','p').filter(w = Warehouse.objects.get(w_id = 'w_1'))
                    context = {'warehouse_inv': inv}
                    return render(request, 'warehouse_admin.html', context)
        
            except:
                try:
                    cur_user = Member.objects.get(m_id = request.user.username) 
                    
                    context = {'username': cur_user.get_name(), 'product_list':product_list, 'manufacturer_list':manufacturer_list, 'category_list':category_list} 
                    return render(request, 'home.html', context)
                except:
                    return render(request, 'home.html', {'product_list':product_list, 'manufacturer_list':manufacturer_list, 'category_list':category_list})
        
    else:
        device = request.COOKIES['device']
        customer = Member.objects.get_or_create(
            m_id = device,
            name = "non_user",
            phone = "-1",
            email = device,
            type = 1,
            user_status = 1,
            reg_date = '2999-12-31',
            billing_date = '2999-12-31')
        return render(request, 'home.html', {'product_list':product_list, 'manufacturer_list':manufacturer_list, 'category_list':category_list} )


def cart(request):
    if request.user.is_authenticated:    
        cart_list = Cart.objects.values('p__p_name', 'p__instore_price', 'quantity', 'p').filter(m = request.user.username)
        context = {
            'cart_list' : cart_list
        }
        return render(request, 'cart.html', context)
    else:
        device = request.COOKIES['device']
        cart_list = Cart.objects.values('p__p_name', 'p__instore_price', 'quantity', 'p').filter(m = device)
        context = {
            'cart_list' : cart_list
        }
        return render(request, 'cart.html', context)
        
        
        


def card(request):
    if request.user.is_authenticated:
        cur_user = request.user.username
        mem = Member.objects.get(m_id = cur_user)
        card_list = Membercardinfo.objects.filter(m_id = mem)
        print(card_list)
        context = {'card_list' : card_list}
        return render(request, 'card.html', context)
        
    
def address(request):
    if request.user.is_authenticated:
        cur_user = request.user.username
        mem = Member.objects.get(m_id = cur_user)
        address_list = Memberaddress.objects.filter(m_id = mem)
        context = {'address_list' : address_list}
        return render(request, 'address.html', context ) 
    

def edit(request):    
    cur_user = request.user.username
    member = Member.objects.get(m_id = cur_user)
    if request.method == 'POST':
        new_email = request.POST['email']
        new_phone = request.POST['phone']
        type = request.POST['type']
        member.email = new_email
        member.phone = new_phone
        member.type = type
        member.save()
        return redirect('/')  
    else:
        context = {'member': member}
        return render(request, "edit.html", context)

def add_card(request):
    cur_user = request.user.username
    card_list = Membercardinfo.objects.filter(m = cur_user)
    print(type(cur_user))
    if request.method == 'POST':
        try:
            new_card = request.POST['cardnumber']
            if new_card == "":
                return card(request)
            new_cardholder = request.POST['cardholder']
            new_exp_month = request.POST['month']
            new_exp_year = request.POST['year']
            n_card = Membercardinfo(
                m_id = cur_user,
                card_num = new_card,
                card_name = new_cardholder,
                card_exp_month= new_exp_month,
                card_exp_year= new_exp_year,
                balance = float(random.randint(100000, 100000000))/100
            )
            n_card.save()
           
            bank.save()
            return card(request)
        except Exception as e:
            print(e)
            return card(request)
    else:
        return render(request, "new_card.html") 
    

def add_address(request):
    cur_user = request.user.username
    mem = Member.objects.get(m_id = cur_user)
    add_list = Memberaddress.objects.filter(m_id = mem)
    if request.method == 'POST':
        try:
            address1 = request.POST['street']
            if address1 == "":
                return address(request)
            address2 = request.POST['box']
            state = request.POST['state']
            zip_code = request.POST['zip']
            n_add = Memberaddress(
                m_id = cur_user,
                address1 = address1,
                address2 = address2,
                state= state,
                zipcode = zip_code
            )
            n_add.save()
            
            return address(request)
        except Exception as e:
            print(e)
            return address(request)
    else:
        return render(request, "new_address.html") 
    
def history(request):
    mem = Member.objects.get(m_id=request.user.username)
    hist = Onlineorder.objects.values('p__p_name', 'quantity', 'card_info', 'order_date','address1','phone_num').filter(m = mem)
    return render(request, "history.html", {'history':hist})

def card_delete(request, card_num):
    c = Membercardinfo.objects.get(card_num=card_num)
    c.delete()
    print(c)
    return redirect('/card') 

def address_delete(request, address):
    mem = Member.objects.get(m_id=request.user.username)
    add = Memberaddress.objects.get(m=mem, address1=address)
    add.delete()
    return redirect('/address')  