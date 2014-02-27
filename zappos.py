#This current version of the application is working with 'shirts', 'kitchen','accessories'
#as the alternate fields since the variety in prices can support a relatively wide range of prices.

import urllib2,json,operator

input_price = 250
input_no_items = 3
item = 'accessories'
API_KEY = 'a73121520492f88dc3d33daf2103d7574f1a3166'

def searchurl(item,price,key,sort,limit,page):
    return 'http://api.zappos.com/Search?term='+item+'&filters={"priceFacet":["'+price+'"]}&sort={"price":"'+sort+'"}&limit='+str(limit)+'&page='+str(page)+'&key='+key

def readjson(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

prices = {50:'$50.00 and Under',100:'$100.00 and Under',200:'$200.00 and Under',201:'$200.00 and Over'}

def gift(input_price,input_no_items, final_list, products, product_prices, f_price,sort1,prev_page,page):
    if input_no_items == 0 or input_price<=0:
        return final_list
    else:
        average = input_price/input_no_items
        avgprice = []
        for p,t in prices.iteritems():
            avgprice.append(p - average)

        f_price_key = min(avgprice, key=lambda v: (abs(v - 0), v < 0))+average
        filter_price = prices[f_price_key]

        min_price = float(readjson(searchurl(item,filter_price,API_KEY,'asc',1,page))['results'][0]['price'][1:])
        if average > (f_price_key + min_price)/2:
            sort = 'desc'
        else:
            sort = 'asc'
        if len(products) == 0 or f_price_key!= f_price or sort!=sort1 or prev_page!=page:
            #print searchurl(item,filter_price,API_KEY,sort,100,page)
            json_data = readjson(searchurl(item,filter_price,API_KEY,sort,100,page))['results']
            products = {}
            product_prices = []
            for r in json_data:
                if r['productName'] not in products.keys():
                    product_prices.append( float(r['price'][1:]))
                    products[r['productName']] = product_prices[-1]


        if average > (max(product_prices)+min(product_prices))/2:
            rev = True
        else:
            rev = False
        sorted_product_list = sorted(products.iteritems(), key=operator.itemgetter(1),reverse=rev)
        added = False
        for p in sorted_product_list:
            if p[0] not in final_list.keys():
                    if input_price - p[1]>0 or (input_price-p[1]==0 and input_no_items==1):
                        final_list[p[0]]=p[1]
                        input_no_items-=1
                        input_price-=p[1]
                        added = True
                        break
        if added == False:
            prev_page=page
            page+=2
        gift(input_price,input_no_items,final_list,products,product_prices,f_price_key,sort,prev_page,page)
    return final_list

if input_no_items <= 0 or input_price <= 0:
    print "inputs have to be greater than zeros"
else:
    print gift(input_price,input_no_items,{},{},[],0,'desc',1,1)