from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Book

# --- LOGIC BÀI 1: QUẢN LÝ SÁCH ---
def book_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        if title and author and price:
            Book.objects.create(title=title, author=author, price=price)
            return redirect('book_list') # Reset lại trang sau khi lưu dữ liệu thành công

    all_books = Book.objects.all()
    expensive_books = Book.objects.filter(price__gt=100) # Lọc giá > 100
    total_books = all_books.count() # Đếm tổng số lượng sách

    return render(request, 'main_app/book_list.html', {
        'all_books': all_books,
        'expensive_books': expensive_books,
        'total_books': total_books
    })

# --- LOGIC BÀI 2: XÁC THỰC USER ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') # Chặn user chưa đăng nhập, tự động đá về trang login
def dashboard_view(request):
    return render(request, 'main_app/dashboard.html')