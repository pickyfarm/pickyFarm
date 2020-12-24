from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product_Comment, Product_Recomment
from .forms import ProductCommentForm, ProductRecommentForm
from products.models import Product
# from django.http import JsonResponse

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
            return redirect(reverse('commens:product_comment_detail', kwargs={'pk':pk}))
    else:
        product_comment_form = ProductCommentForm(instance=product_comment)       

    return render(request, 'comments/product_comment.html', {'product_comment_form':product_comment_form})


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
    product_comment = Product_Comment.objects.get(pk=pk)
    product = product_comment.product
    product_recomment_form = ProductRecommentForm(request.POST)

    if product_recomment_form.is_valid():
        product_recomment = product_recomment_form.save(commit=False)
        product_recomment.author = request
        product_recomment.comment = product_comment
    
    return redirect(reverse('comments:product_recomment_detail', args=[pk]))