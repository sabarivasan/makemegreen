import urllib2
import bs4
import json
import re
import boto3

def get_html(url):
    hdr = {
           'User-Agent': 'Mozilla/5.0',
           "Connection": "keep-alive"
           }
    req = urllib2.Request(url,headers=hdr)
    page = urllib2.urlopen(req)
    return bs4.BeautifulSoup(page, 'html.parser')

def get_max_id(products):
    if len(products)>0:
        return max([p['id'] for p in products])
    else:
        return 0

def convert_to_num_rating(character_rating):
    switcher = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
    }
    return switcher.get(character_rating, 0)

def get_children_tags(tag):
    children_tags = []
    for child in tag:
        if isinstance(child, bs4.element.Tag):
            children_tags.append(child)
    return children_tags

def get_subcateory_urls():
    ctg_soup = get_html(BASE_URL+'/guides/cleaners/content/top_products')
    ctgs = ctg_soup.find(id="home_product_toc_ul").contents
    categories = []
    for ctg in ctgs:
        if isinstance(ctg,bs4.element.Tag):
            ctg_url = ctg.find('a')['href']
            sub_ctg_soup = get_html(BASE_URL+ctg_url)
            sub_ctgs = sub_ctg_soup.find(id="home_product_toc_items_ul").contents
            for sub_ctgs in sub_ctgs:
                if isinstance(sub_ctgs,bs4.element.Tag):
                    sub_ctg_url = sub_ctgs.find('a')['href']
                    categories.append(sub_ctg_url)
    return categories


def get_product_detail(url):
    detail_soup = get_html(url)
    detail = {}
    prodnames = detail_soup.find_all(id='prodname_name')
    detail['brand'] = re.sub('[B|b]rand: ','',prodnames[1].text)
    if detail['brand'].endswith('...'):
        brand_url = BASE_URL+prodnames[1].parent['href']
        brand_soup = get_html(brand_url)
        detail['brand'] = brand_soup.find(id='productname').text.replace('\n','')
    # detail['category'] = prodnames[0].text.lower()
    return detail

def pascal_case_to_spaces(word):
    return ''.join(map(lambda x: x if x.islower() else " "+x.lower(), word)).strip()

def scrap_products(url,all_prod):
    print(url)
    soup = get_html(url)
    products = soup.find(id='products').find("div","innertab").contents
    prod_id = get_max_id(all_prod)
    children_products = get_children_tags(products)
    category = pascal_case_to_spaces(re.search("\d+-(\w+)\?page=\d+",url).group(1))
    for prod in children_products:
        prod_dict = {}
        prod_info = prod.find_all('a')
        if len(prod_info)>0:
            prod_id = prod_id +1
            prod_info_block = prod_info[1]
            prod_dict['name'] = prod_info_block.text
            prod_detail_page = prod_info_block['href']
            prod_detail = get_product_detail(BASE_URL+prod_detail_page)
            prod_dict['seller'] = prod_detail['brand']
            prod_dict['category'] = category
            prod_dict['rating'] = convert_to_num_rating(prod_info[2].text)
            prod_dict['id'] = prod_id
            prod_dict['source'] = 'https://www.ewg.org'
            all_prod.append(prod_dict)
    return all_prod

BASE_URL = 'https://www.ewg.org'
categories = get_subcateory_urls()
all_prod = []
for category_url in categories:
    soup = get_html(BASE_URL+category_url)
    next_page = soup.find('a','next_page')
    last_page_num = 1
    if isinstance(next_page,bs4.element.Tag):
        last_page = next_page.previous_sibling
        while isinstance(last_page,bs4.element.NavigableString):
            last_page = last_page.previous_sibling

        last_page_num = int(last_page.text)

    for page in range(1,last_page_num+1):
        page_url = BASE_URL+category_url+'?page='+str(page)
        all_prod = scrap_products(page_url,all_prod)

# page_url = 'https://www.ewg.org/guides/categories/1-AirFresheners?page=1'
# all_prod = scrap_products(page_url,all_prod)

with open('green_products.json', 'w') as fp:
    json.dump(all_prod, fp, indent=4)