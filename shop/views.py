from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
import datetime
import sqlite3
import csv
from ftplib import FTP
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.utils.decorators import method_decorator
import simplejson as simplejson
from django.views import generic
from django_datatables_view.base_datatable_view import BaseDatatableView

from moneyed import Money
from djmoney_rates.utils import convert_money


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

# pobieranie stanów
def get_stan(request):

    serverG = "178.217.140.125"
    directoryG = "/"
    filenameG = "stan_gt_.csv"

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
    csvfile = open('stan_gt_.csv', 'rt', encoding="utf8")
    creader = csv.reader(csvfile, delimiter=';', quotechar='|')

    # Iterate through the CSV reader, inserting values into the database
    next(creader)
    for row in creader:
        category_id = 1
        name = row[11] + ' ' + row[3].replace(' ','R') + ' ' + row[4] + ' ' + row[6] + '' + row[7] + ' ' + row[8] + ' ' + row[14] + ' ' + row[15]
        slug = row[1]
        image_id = 1
        sap = row[1]
        ean = row[5]
        manufacturer = row[11]
        model = row[4]
        size = row[3].replace(' ','R')
        speed_index = row[7]
        load_index = row[6]
        rolling_resistance = row[12]
        adhesion = row[13]
        noise = row[14] + ' ' + row[15]
        dot = '20'+row[26][-2:]
        stock = int(row[20]) + int(row[21]) + int(row[22]) + int(row[23])
        price = float(row[19][:-4].replace(',','.').replace('\xa0',''))
        price_ue = float(row[27][:-4].replace(',','.').replace('\xa0',''))
        additional_marking = row[8]
        season = row[10]
        typ = row[9]
        available = True
        sale = False
        created = datetime.datetime.now()
        updated = datetime.datetime.now()
        search_field = 'SAP'+sap+'EAN'+ean+''+manufacturer+''+model.replace(' ','')+''+season+size.replace('/','').replace('R','')+''+load_index+''+speed_index+'DOT'+dot+season[:1]+size.replace('/','').replace('R','')+typ

        if stock > 0 and price > 0:
            cursor.execute('INSERT OR IGNORE INTO shop_product (name, slug, sap, ean, manufacturer, model, size, speed_index, load_index, rolling_resistance, adhesion, noise, dot, price, price_ue, stock, available, created, updated, category_id, image_id, sale, search_field, additional_marking, season, typ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, slug, sap, ean, manufacturer, model, size, speed_index, load_index, rolling_resistance, adhesion, noise, dot, price, price_ue, stock, available, created, updated, category_id, image_id, sale, search_field, additional_marking, season, typ))
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

def stany_mag(request):

	with open('b2b_stany_mag.csv', "w", newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter=';')
		writer.writerow(['Nazwa', 'SAP', 'EAN', 'Producent', 'Rozmiar', 'Model', 'Sezon', 'Typ', 'DOT', 'PLN [Netto]', 'Ilość'])
		products = Product.objects.all().values_list('name', 'sap', 'ean', 'manufacturer', 'size', 'model', 'season', 'typ', 'dot', 'price', 'stock').order_by('sap').filter(available=True)

		for product in products:
			writer.writerow([product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10]])

    # Upload plików
	serverG = "178.217.140.125"
	directoryG = "/"
	filenamePL = "b2b_stany_mag.csv"

	ftpG = FTP(serverG)  # Set server address
	ftpG.login("stany_ph", "1qazxsW@")  # Connect to server
	ftpG.cwd(directoryG)  # Move to the desired folder in server
	ftpG.storbinary('STOR ' + filenamePL, open(filenamePL, 'rb'))  # Download file from server
	ftpG.close()  # Close connection

	return render(request, 'shop/product/get.html')

def stany_mag_ue(request):

	with open('b2b_stocks.csv', "w", newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter=';')
		writer.writerow(['Name', 'SAP', 'EAN', 'Manufacturer', 'Size', 'Model', 'Season', 'Type', 'DOT', 'EUR [Netto]', 'Stock'])
		products = Product.objects.all().values_list('name', 'sap', 'ean', 'manufacturer', 'size', 'model', 'season', 'typ', 'dot', 'price', 'stock').order_by('sap').filter(available=True)

		for product in products:
			price_eur = convert_money(product[9], "PLN", "EUR")
			writer.writerow([product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], price_eur, product[10]])

    # Upload plików
	serverG = "178.217.140.125"
	directoryG = "/"
	filenameUE = "b2b_stocks.csv"

	ftpG = FTP(serverG)  # Set server address
	ftpG.login("stany_ph", "1qazxsW@")  # Connect to server
	ftpG.cwd(directoryG)  # Move to the desired folder in server
	ftpG.storbinary('STOR ' + filenameUE, open(filenameUE, 'rb'))  # Download file from server
	ftpG.close()  # Close connection

	return render(request, 'shop/product/get.html')
