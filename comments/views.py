from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product_Comment, Product_Recomment
from .forms import ProductCommentForm, ProductRecommentForm
from products.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse

# 상품 댓글 Read
def product_comment_detail(request, pk):
    product = Product.objects.get(pk=pk)
    product_comments = product.product_comments.all()
    product_comment_form = ProductCommentForm()
    product_recomment_form = ProductRecommentForm()

    ctx = {
        'product':product,
        'product_comments':product_comments,
        'product_comment_form':product_comment_form,
        'product_recomment_form':product_recomment_form,
    }

    return render(request, 'comments/product_comment.html', ctx)

# 상품 댓글 create
def product_comment_create(request, pk):
    product = Product.objects.get(pk=pk)
    product_comment_form = ProductCommentForm(request.POST, request.FILES)
    product_recomment_form = ProductRecommentForm(request.POST)

    if product_comment_form.is_valid():
        product_comment = product_comment_form.save(commit=False)
        product_comment.author = request.user
        product_comment.product = product
        product_comment.save()
    
    return redirect(reverse('comments:product_comment_detail', args=[pk]))

# 상품 댓글 update
def product_comment_update(request, pk):
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product

    if request.method =='POST':
        product_comment_form = ProductCommentForm(request.POST, request.FIELS, instance=product_comment)
        if product_comment_form.is_valid():
            product_comment = product_comment_form.save(commit=False) 
            product_comment.author = request.user
            product_comment.product = product
            return redirect(reverse('comments:product_comment_detail', kwargs={'pk':pk}))
    else:
        product_comment_form = ProductCommentForm(instance=product_comment)       

    return render(request, 'comments/product_comment.html', {'product_comment_form':product_comment_form})

#상품 댓글 delete(request)
def product_comment_delete(request,pk):
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product

    if request.method == 'POST':
        product_comment.delete()
        return redirect(product)
    else:
        return render(request, 'coments/product_comment.html')

# 상품 대댓글 Read
def product_recomment_detail(request, pk):
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product
    product_recomment_form = ProductRecommentForm()

    ctx = {
        'product_comment':product_comment,
        'product':product,
        'product_recomment_form':product_recomment_form,
    }    

    return render(request, 'comments/product_comment.html', ctx)

# 상품 대댓글 create
def product_recomment_create(request, pk):
    is_ajax = request.POST.get('is_ajax')
    print(is_ajax)
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product
    recomment_form = ProductRecommentForm(request.POST)
    if recomment_form.is_valid():
        print('valid')
        recomment = recomment_form.save(commit=False)
        recomment.author = request.user
        recomment.comment = product_comment
        recomment.save()

    if is_ajax:
        print("ajax성공")
        html = render_to_string('products/product_detail.html',{'recomment':recomment, 'username':request.user})
        return JsonResponse({'html':html})
    else:
        print("ajax실패")

    return redirect('products:product_detail', product.pk)
    
    # return redirect(reverse('products:product_detail', args=[pk]))

# 상품 대댓글 update
def product_recomment_update(request, pk):
    product_comment = Product.objects.get(pk=pk)
    product = product_comment.product
    product_recomment = product_comment__set()
    product_recomment_form = ProductRecommentForm(request.POST)

    if request.method =='POST':
        product_recomment_form = ProductRecommentForm(request.POST, instance=product_recomment)
        if product_recomment_form.is_valid():
            product_recomment = product_recomment_form.save(commit=False) 
            product_recomment.author = request.user
            product_recomment.product = product
            return redirect(reverse('commens:product_reomment_detail', kwargs={'pk':pk}))
    else:
        product_recomment_form = ProductRecommentForm(instance=product_recomment)       

    return render(request, 'comments/product_recomment.html', {'product_recomment_form':product_recomment_form})
