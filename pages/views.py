from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from .models import Product, Cart, Comment
from django import forms 
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView
from .forms import ProductForm
from .models import Product
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

# Create your views here.
class HomePageView(TemplateView):
    template_name='pages/home.html'

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs) 
         context.update({
              "title": "About us - Online Store",
              "subtitle": "About us",
              "description": "This is an about page sale of products",
              "author": "Developed by: Katherin Allin",
         })
         return context
    
#class Product:
#     products = [
#           {"id":"1", "name":"TV", "description":"Best TV"},
#           {"id":"2", "name":"iPhone", "description":"Best iPhone"},
#           {"id":"3", "name":"Chromecast", "description":"Best Chromecast"},
#           {"id":"4", "name":"Glasses", "description":"Best Glasses"}
#] 
     
class ProductIndexView(View):
     model = Product
     template_name = "products/index.html"  
     context_object_name = "products"
     
     def get(self, request):
         viewData = {}
         viewData["title"] = "Products - Online Store"
         viewData["subtitle"] = "List of products" 
         viewData["products"] = Product.objects.all()
         
         return render(request, self.template_name, viewData)

#class ProductIndexView(ListView):
 #   model = Product
 #   template_name = "products/index.html"  
 #   context_object_name = "products" 
     
class ProductShowView(View):
     model = Product
     template_name = 'products/show.html'
     context_object_name = 'product'
     
     def get(self, request, id):
         # Check if product id is valid
         try: 
             product_id = int(id)
             if product_id < 1: 
               raise ValueError("Product id must be 1 or greater") 
             product = get_object_or_404(Product,pk=product_id) 
         except (ValueError, IndexError):
             # If the product id is not valid, redirect to the home page 
             return HttpResponseRedirect(reverse('home'))
         
         viewData = {}
         product = get_object_or_404(Product,pk=product_id)
         viewData["title"] = product.name + " - Online Store"
         viewData["subtitle"] = product.name + " - Product information" 
         viewData["product"] = product 
         
         return render(request, self.template_name, viewData)
     

#class ProductShowView(DetailView):
 #   model = Product
 #   template_name = 'pages/product_detail.html'
 #   context_object_name = 'product'

class ProductForm(forms.ModelForm):
     name = forms.CharField(required=True) 
     price = forms.FloatField(required=True)
     class Meta:
        model = Product
        fields = ['name','price']


     def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    #def clean_price(self):
     #   price = self.cleaned_data.get('price')
      #  if price is not None and price <= 0:
       #    raise ValidationError('Price must be greater than zero.')
        #return price


class ProductCreateView(CreateView):
     model = Product
     form_class = ProductForm
     template_name = 'products/create.html' 
     success_url = '/products/'
     #'/products/'
     
     def get(self, request): 
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product" 
        viewData["form"] = form
        return render(request, self.template_name, viewData)
        
     def post(self, request): 
        form = ProductForm(request.POST)
        if form.is_valid():
             #form.save()
             return redirect(form)
        else: viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
     
class ProductListView(ListView):
      model = Product
      template_name = 'product_list.html'
      context_object_name = 'products' # This will allow you to loop through 'products' in your template
      
      def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['title'] = 'Products - Online Store'
           context['subtitle'] = 'List of products' 
           return context

class CartView(View): 
      template_name = 'cart/index.html' 
      
      def get(self, request):
           products = {} 
           products[121] = {'name': 'Tv samsung', 'price': '1000'}
           products[11] = {'name': 'Iphone', 'price': '2000'} 
           
           cart_products = {} 
           cart_product_data = request.session.get('cart_product_data', {}) 
           
           for key, product in products.items(): 
                if str(key) in cart_product_data.keys():
                     cart_products[key] = product 
                     
           view_data = {
                'title': 'Cart - Online Store',
                'subtitle': 'Shopping Cart',
                'products': products, 
                'cart_products': cart_products
                 
                } 
           
           return render(request, self.template_name, view_data)
      

      def post(self, request, product_id):
           cart_product_data = request.session.get('cart_product_data', {})
           cart_product_data[product_id] = product_id
           request.session['cart_product_data'] = cart_product_data
           
           return redirect('cart_index') 
      
      def cart_view(request):
           return render(request, 'pages/cart.html')  # Asegúrate de que el template existe
      
class CartRemoveAllView(View): 
      def post(self, request):
           if 'cart_product_data' in request.session:
                del request.session['cart_product_data']
           return redirect('cart_index')
      
def some_view(request):
    from .models import Cart
    # Usa Cart dentro de la función

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = image_storage.url(request)
            request.session['image.url'] = image_url
            return redirect('image_index')
    return ImageView

def upload_image(request):
    if request.method == 'POST':
        print("📸 Recibida petición POST")
        if 'image' in request.FILES:  # Verifica que se haya subido un archivo
            image = request.FILES['image']
            file_path = default_storage.save(f'uploads/{image.name}', image)
            return render(request, 'pages/image.html', {'image_url': file_path})
        else:
            print("⚠️ No se encontró una imagen en la petición")
    return render(request, 'pages/image.html')

    #image_url = None

    #if request.method == "POST" and request.FILES.get("image"):
    #    image = request.FILES["image"]
        #filename = default_storage.save(f"uploads/{image.name}", ContentFile(image.read()))
        #image_url = default_storage.url(filename)
     #   file_path = os.path.join("uploads", image.name)  # Ruta relativa dentro de media/
        
        # Guardar la imagen
     #   default_storage.save(file_path, ContentFile(image.read()))

        # Construir URL correctamente
     #   image_url = f"{settings.MEDIA_URL}{file_path}"

    #return render(request, "pages/upload_image.html", {"image_url": image_url})

class ImageView(View):
    def get(self, request):
        return render(request, 'pages/image.html')  # Usa la plantilla corregida

class ImageViewNoDI(View):
      template_name = 'images/index.html' 
      
      def get(self, request):
           image_url = request.session.get('image_url', '')
           
           return render(request, self.template_name, {'image_url': image_url})
           
      def post(self, request): 
           image_storage = ImageLocalStorage() 
           image_url = image_storage.store(request) 
           request.session['image_url'] = image_url 
           
           return redirect('image_index')