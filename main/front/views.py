from django.shortcuts import render
from django.db.models import Sum, Q
from datetime import datetime
from django.shortcuts import render, redirect
from main import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    products = models.Product.objects.all()
    outs = models.Out.objects.all()
    enters = models.Enter.objects.all()
    returns = models.Return.objects.all()
    categories = models.Category.objects.all()
    try:
      context ={
          'products': products,
          'outs': outs,
          'enters': enters,
          'returns': returns,
          'categories': categories,
      }
    except:
      return redirect('error')
    return render(request, 'index.html', context)

# >>>>>>>>>>>>>>>>>>> Category: list, create, update, delete <<<<<<<<<<<<<<<<<<<<<<


# --------- Category list ------------------
@login_required
def category_list(request):
    """Category List"""
    queryset = models.Category.objects.all()
    context = {'queryset': queryset}
    return render(request, 'category/list.html', context)


# --------- Category create ------------------
@login_required
def category_create(request):
    """Category Create"""
    if request.method == 'POST':
        name = request.POST['name']
        models.Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'category/create.html')


# ---------- Category update ------------------
@login_required
def category_update(request, code):
    """Category Update"""
    category = models.Category.objects.get(code=code)
    if request.method == 'POST':
        name = request.POST['name']
        category.name = name
        category.save()
        return redirect('category_list')
    context = {'category': category}
    return render(request, 'category/update.html', context)


#  -------------- Category delete ----------------
@login_required
def category_delete(request, code):
    """Category Delete"""
    category = models.Category.objects.get(code=code)
    category.delete()
    return redirect('category_list')



# >>>>>>>>>>>>>>>>>>>>>>>> Product: create, update, delete, list <<<<<<<<<<<,


# --------- Product create ----------------
@login_required
def product_create(request):
    """Product Create"""
    categories = models.Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(code=request.POST.get('category_code'))
        image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        count = request.POST.get('count')
        product = models.Product.objects.create(
            name=name,
            category=category,
            image=image,
            description=description,
            price=price,
            count=count,
        )
        return redirect('product_list')
    return render(request, 'product/create.html', {'categories': categories})


# --------- Product list ------------------
@login_required
def product_list(request):
    name = request.GET.get('name')
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    products = models.Product.objects.all()

    if name:
        products = products.filter(name__icontains=name)
    if category:
        products = products.filter(category__name__icontains=category)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d')

    enters = models.Enter.objects.all()
    outs = models.Out.objects.all()
    if date_from and date_to:
        enters = enters.filter(data__range=(date_from, date_to))
        outs = outs.filter(data__range=(date_from, date_to))

    context = {
        'products': products,
        'categories': models.Category.objects.all(),
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'product/list.html', context)




# ---------- Product update ----------
@login_required
def product_update(request, code):
    """Product update """
    product = models.Product.objects.get(code=code)
    categories = models.Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(code=request.POST.get('category_code'))
        image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        count = request.POST.get('count')
        product.name = name
        product.category = category
        product.image = image
        product.description = description
        product.price = price
        product.count = count
        product.save()
        return redirect('product_list')
    context = {'product': product, 'categories': categories}
    return render(request, 'product/update.html', context)


# ---------- Product delete ------------------------
def product_delete(request, code):
    """Product Delete"""
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')




# >>>>>>>>>>>>>>>>>>>>> Enter: list, create, update <<<<<<<<<<<<<<<



# ----------- Enter: list  ----------------
@login_required
def enter_create(request):
    """Enter Create"""
    products = models.Product.objects.all()
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        quantity = int(request.POST.get('quantity'))
        
        product = models.Product.objects.get(code=product_code)

        models.Enter.objects.create(
            product=product,
            quantity=quantity,
        )

        product.count += quantity
        product.save()
        
        return redirect('enter_list')
    
    context = {'products': products}
    return render(request, 'enter/create.html', context)




#--------------- Enter list --------------------
@login_required
def enter_list(request):
    """Enter List"""
    queryset = models.Enter.objects.all()
    context = {'queryset': queryset}
    return render(request, 'enter/list.html', context)



# -------------- Enter update ------------------
@login_required
def enter_update(request, id):
    """Enter Update"""
    enter = models.Enter.objects.get(id=id)
    products = models.Product.objects.all()
    
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        quantity = int(request.POST.get('quantity'))
        
        product = models.Product.objects.get(code=product_code)

        quantity_diff = quantity - enter.quantity

        enter.product = product
        enter.quantity = quantity
        enter.save()

        product.count += quantity_diff
        product.save()
        
        return redirect('enter_list')
    
    context = {'enter': enter, 'products': products}
    return render(request, 'enter/update.html', context)

    


# >>>>>>>>>>>>>>>>>>>> Out: list update create <<<<<<<<<<<<<



# ----------- Out: create  ----------------
@login_required
def out_create(request):
    """Out Create"""
    products = models.Product.objects.all()
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        quantity = int(request.POST.get('quantity'))
        
        product = models.Product.objects.get(code=product_code)
        
        if product.count < quantity:
            messages.error(request, 'Omborda yetarli mahsulot mavjud emas.')
            return redirect('out_create')
        

        models.Out.objects.create(
            product=product,
            quantity=quantity,
        )
        
        product.count -= quantity
        product.save()
        
        enter_records = models.Enter.objects.filter(product=product).order_by('id')
        remaining_quantity = quantity
        
        for enter in enter_records:
            if enter.quantity > remaining_quantity:
                enter.quantity -= remaining_quantity
                enter.save()
                break
            else:
                remaining_quantity -= enter.quantity
                enter.quantity = 0
                enter.save()
        
        return redirect('out_create')
    
    context = {'products': products}
    return render(request, 'out/create.html', context)



#--------------- Out list ----------------------------
@login_required
def out_list(request):
    """Out List"""
    queryset = models.Out.objects.all()
    context = {'queryset': queryset}
    return render(request, 'out/list.html', context)



# -------------- Out update --------------------------
@login_required
def out_update(request, id):
    """Out Update"""
    out = models.Out.objects.get(id=id)
    products = models.Product.objects.all()
    
    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        quantity = int(request.POST.get('quantity'))
        
        product = models.Product.objects.get(code=product_code)
        
        quantity_diff = quantity - out.quantity
        
        if product.count + out.quantity < quantity:
            messages.error(request, 'Yangilash uchun yetarli mahsulot mavjud emas.')
            return redirect('out_update', id=id)
        
        out.product = product
        out.quantity = quantity
        out.save()
        
        product.count -= quantity_diff
        product.save()
        
        if quantity_diff != 0:
            enter_records = models.Enter.objects.filter(product=product).order_by('-id')
            remaining_quantity = abs(quantity_diff)
            
            for enter in enter_records:
                if quantity_diff < 0:
                    if enter.quantity >= remaining_quantity:
                        enter.quantity -= remaining_quantity
                        enter.save()
                        break
                    else:
                        remaining_quantity -= enter.quantity
                        enter.quantity = 0
                        enter.save()
                else:
                    enter.quantity += remaining_quantity
                    enter.save()
                    break
        
        return redirect('out_list')
    
    context = {'out': out, 'products': products}
    return render(request, 'out/update.html', context)




# >>>>>>>>>>>>>>>>> Return : list create update <<<<<<<<<<<<<<<<<<<

# ----------- Return: create  ----------------
def return_create(request):
    outlays = models.Out.objects.filter(returned=False)
    if request.method == 'POST':
        outlay = models.Out.objects.get(id=request.POST.get('out_id'))
        models.Return.objects.create(
            out = outlay
        )
        return redirect('return_list')
    return render(request, 'return/create.html', {'outlays': outlays})

# -------------- Return list ----------------

def return_list(request):
    """Return List"""
    queryset = models.Return.objects.all()
    context = {'queryset': queryset}
    return render(request,'return/list.html', context)

# -------------- Return update ----------------

def return_update(request, id):
    """Return Update"""
    return_ = models.Return.objects.get(id=id)
    outlays = models.Out.objects.filter(returned=False)
    
    if request.method == 'POST':
        outlay = models.Out.objects.get(id=request.POST.get('out_id'))
        return_.out = outlay
        return_.save()
        return redirect('return_list')
    
    context = {'return_': return_, 'outlays': outlays}
    return render(request,'return/update.html', context)



# >>>>>>>>>>>>>>> profil <<<<<<<<<<<<<<<<<<

# -------------- profil ----------------

@login_required
def profil(request):
    """Profil"""
    user = request.user
    context = {'user': user}
    return render(request, 'auth/profile.html', context)

@login_required
def setting(request):
    """settings page"""
    if request.method == 'POST':
            user = request.user
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            messages.success(request, 'Profil  muvoffaqiyatli o`zgartirildi')
            user.save()
            return redirect('index')
    return render(request, 'auth/setting.html')



# >>>>>>>>>>>>>>>>>>>>> Login, logout, Error <<<<<<<<<<<<<<<


# -------------- login ---------------
def log_in(request):
    """Login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('error')

    return render(request, 'auth/login.html')

# -------------- logout ---------------
def log_out(request):
    """Logout"""
    logout(request)
    messages.success(request, 'logout success')
    return redirect('error')

# -------------- Error ---------------
def error(request):
    """ error message"""
    return render(request, 'auth/error.html')