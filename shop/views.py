from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
import datetime
import sqlite3
import csv
from ftplib import FTP
from django.contrib.auth.decorators import login_required
from django.db.models import Q
#import json
from django.core import serializers
from django.http import HttpResponse
#from django.http import JsonResponse

from django.utils.decorators import method_decorator
import simplejson as simplejson
from django.views import generic
from django_datatables_view.base_datatable_view import BaseDatatableView



@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    order_by = request.GET.get('order_by', 'id')
    products = Product.objects.filter(available=True).order_by(order_by)
    last_products = Product.objects.filter(available=True).order_by('-updated')[:5]
    sales = Product.objects.filter(sale=True).order_by('-updated')[:5]
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__contains=query) |
            Q(sap__contains=query) |
            Q(ean__exact=query) |
            Q(manufacturer=query) |
            Q(model__icontains=query) |
            Q(search_field__icontains=query) |
            Q(size__icontains=query)
            ).distinct()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products, 'cart_product_form': cart_product_form, 'last_products': last_products, 'sales': sales})

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

#class jsonlist(BaseDatatableView):
#    model = Product
#    columns = ['image', 'manufacturer', 'name', 'sap', 'ean','dot', 'price', 'pk', 'size']
#    order_columns = columns
#
#    @method_decorator(login_required(login_url='/login/'))
#    def dispatch(self, request, *args, **kwargs):
#        return super(jsonlist, self).dispatch(request, *args, **kwargs)
#
#    def get_initial_queryset(self, **kwargs):
#        query = Product.objects.filter(available=True)
#        return query
#
#    def render_column(self, row, column):
#        # i recommend change 'flat_house.house_block.block_name' to 'address'
#        if column == 'image':
#            return format(row.image.image);
#        else:
#            return super(jsonlist, self).render_column(row, column)

# pobieranie stanów
def get_stan(request):

    serverG = "178.217.140.125"
    directoryG = "/"
    filenameG = "PlatformaOpon.csv"

    ftpG = FTP(serverG) #Set server address
    ftpG.login("stany_mag", "GlobeTyre$#")  # Connect to server
    ftpG.cwd(directoryG) # Move to the desired folder in server
    ftpG.retrbinary('RETR ' + filenameG,open(filenameG, 'wb').write) # Download file from server
    ftpG.close() # Close connection

    old_products = Product.objects.all().update(available = False)

    # Create the database
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()

    # cursor.execute('DELETE FROM shop_product')
    # cursor.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="shop_product"')

    # Load the CSV file into CSV reader
    csvfile = open('PlatformaOpon.csv', 'rt')
    creader = csv.reader(csvfile, delimiter=';', quotechar='|')

    # Iterate through the CSV reader, inserting values into the database
    next(creader)
    for row in creader:
        category_id = 1
        name = row[1] + ' ' + row[5] + ' ' + row[2] + ' ' + row[7] + '' + row[6]
        slug = row[3]
        image_id = 1
        sap = row[3]
        ean = row[4]
        manufacturer = row[1]
        model = row[2]
        size = row[5]
        speed_index = row[6]
        load_index = row[7]
        rolling_resistance = row[8]
        adhesion = row[9]
        noise = row[10]
        dot = '20'+row[15][-2:]
        stock = row[11]
        price = row[12].replace(',','.')
        price_ue = row[16].replace(',','.')
        available = True
        created = datetime.datetime.now()
        updated = datetime.datetime.now()
        search_field = 'SAP'+sap+'EAN'+ean+''+manufacturer+''+model.replace(' ','')+''+size.replace('/','').replace('R','')+''+load_index+''+speed_index+'DOT'+dot

        cursor.execute('INSERT OR IGNORE INTO shop_product (name, slug, image_id, sap, ean, manufacturer, model, size, speed_index, load_index, rolling_resistance, adhesion, noise, dot, price, stock, available, created, updated, category_id, price_ue, search_field) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, slug,image_id , sap, ean, manufacturer, model, size, speed_index, load_index, rolling_resistance, adhesion, noise, dot, price, stock, available, created, updated, category_id, price_ue, search_field))
        cursor.execute('UPDATE shop_product SET stock=? WHERE sap=?', (stock,sap))
        cursor.execute('UPDATE shop_product SET price=? WHERE sap=?', (price,sap))
        cursor.execute('UPDATE shop_product SET name=? WHERE sap=?', (name,sap))
        cursor.execute('UPDATE shop_product SET ean=? WHERE sap=?', (ean,sap))
        cursor.execute('UPDATE shop_product SET model=? WHERE sap=?', (model,sap))
        cursor.execute('UPDATE shop_product SET dot=? WHERE sap=?', (dot,sap))
        cursor.execute('UPDATE shop_product SET updated=? WHERE sap=?', (updated,sap))
        cursor.execute('UPDATE shop_product SET price_ue=? WHERE sap=?', (price_ue,sap))
        cursor.execute('UPDATE shop_product SET available=? WHERE sap=?', (available,sap))
        cursor.execute('UPDATE shop_product SET search_field=? WHERE sap=?', (search_field,sap))

    # Close the csv file, commit changes, and close the connection
    csvfile.close()
    connection.commit()
    connection.close()
    return render(request, 'shop/product/get.html')
