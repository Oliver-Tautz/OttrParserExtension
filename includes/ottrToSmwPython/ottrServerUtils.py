# Switch to something from wiki doc!
# or even simpler ....
import hashlib
import base64
import requests
import urllib
from stOttrWikiTranslater import parse_stottr_string
import logging
from datetime import datetime
import time


OTTR_EXAMPLE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .
@prefix ex: <http:example.com/ns#> .

ex:NamedPizzaTemplate[owl:Class ?pizza, ? owl:NamedIndividual ?country, NEList<ottr:IRI> ?toppings, ?test] :: {
  ax:SubClassOf(?pizza, ex:NamedPizza),
  ax:SubObjectHasValue(?pizza, ex:hasCountryOfOrigin, ?country),
  ax:SubObjectAllValuesFrom(?pizza, ex:hasTopping, _:toppingsUnion),
  rstr:ObjectUnionOf(_:toppingsUnion, ?toppings),
  ottr:Triple(?pizza,ex:test,"Hallo Welt!"^^xsd:string),
  cross | ax:SubObjectSomeValuesFrom(?pizza, ex:hasTopping, ++?toppings)
} .

ex:NamedPizzaTemplate(ex:Margherita, ex:Italy, (ex:Mozzarella, ex:Tomato)) .
"""

OTTR_EXAMPLE_TEMPLATE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .
@prefix ex: <http:example.com/ns#> .

ex:NamedPizzaTemplate[owl:Class ?pizza, ? owl:NamedIndividual ?country, NEList<ottr:IRI> ?toppings, ?test] :: {
  ax:SubClassOf(?pizza, ex:NamedPizza),
  ax:SubObjectHasValue(?pizza, ex:hasCountryOfOrigin, ?country),
  ax:SubObjectAllValuesFrom(?pizza, ex:hasTopping, _:toppingsUnion),
  rstr:ObjectUnionOf(_:toppingsUnion, ?toppings),
  ottr:Triple(?pizza,ex:test,"Hallo Welt!"^^xsd:string),
  cross | ax:SubObjectSomeValuesFrom(?pizza, ex:hasTopping, ++?toppings)
} .

"""

OTTR_EXAMPLE_INSTANCE = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .
@prefix ex: <http:example.com/ns#> .

ex:NamedPizzaTemplate(ex:Margherita, ex:Italy, (ex:Mozzarella, ex:Tomato)) .

"""


OTTR_EXAMPLE_PREFIXES = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ax: <http://tpl.ottr.xyz/owl/axiom/0.1/> .
@prefix ex: <http:example.com/ns#> .
"""


OTTR_PREFIX_PAGENAME = 'Ottr:OttrPrefixes'


def _clean_comments(ottr_thing):
    lines = ottr_thing.split('\n')
    # remove comments before deciding
    remove_ix = []

    for i in range(len(lines)):
        if lines[i] != '' and lines[i][0] == '#':
            remove_ix.append(i)
        elif '#' in lines[i]:
            lines[i] = lines[i].split('#')[0]


    for i in remove_ix:
        lines.pop(i)

    # rejoin
    text = '\n'.join(lines)
    return text


def is_template(ottr_thing):
    text = _clean_comments(ottr_thing)
    # template if contains {}
    if '{' in text and '}' in text:
        return True
    else:
        return False


def get_template_name_from_template_string(template_string):
    template_string = _clean_comments(template_string)
    return template_string.split('[')[0].strip()


def get_template_name_from_instance_string(instance_string):
    instance_string = _clean_comments(instance_string)
    return instance_string.split('(')[0].strip()


def hash_instance(string, length=10):
    byt = bytes(string, 'utf-8')
    hash = hashlib.md5(byt)
    hash = base64.urlsafe_b64encode(hash.digest())

    # truncate hash ... this is safe as far as I know
    hash = hash[:length]
    return hash.decode('utf8')


def get_page_texts(titles,session,url):
    S = session
    URL=url

    #for i in range(0,len(titles),QUERY_LIMIT):


    PARAMS_GET= {'action':'query','prop':'revisions','titles':'|'.join(titles),'format':'json','rvprop':'content'}
    R = S.get(url=URL,params=PARAMS_GET)
    DATA =R.json()

    return DATA

def get_pagetext_single(title,session,url):
    """
    Oh No :(
    """

    return list(get_page_texts([title],session,url)['query']['pages'].values())[0]['revisions'][0]['*']

def wikiapi_login(Session, URL, bot_user_name, bot_user_password):
    S = Session

    # Step 1: GET request to fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: POST request to log in. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        "action": "login",
        "lgname": bot_user_name,
        "lgpassword": bot_user_password,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: GET request to fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()
    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

    return CSRF_TOKEN

def append_to_prefixes(prefixes, mediawiki_url, bot_user_name, bot_user_password):
    # special case, apopend to page with <ottr> tag inside ottr tag!
    S = requests.Session()

    # use urlparse or similar here!
    urllib.parse.urljoin(mediawiki_url, 'api.php')
    URL = f"{mediawiki_url}/api.php"


    CSRF_TOKEN = wikiapi_login(S, URL, bot_user_name, bot_user_password)

    # Get current page text

    #titles='Ottr:OttrPrefixes'
    PARAMS_GET= {'action':'query','prop':'revisions','titles':OTTR_PREFIX_PAGENAME,'format':'json','rvprop':'content'}

    R = S.get(url=URL,params=PARAMS_GET)
    DATA =R.json()


    wikitext = DATA['query']['pages'][list(DATA['query']['pages'].keys())[0]]['revisions'][0]['*']
    old_prefixes, _ = parse_stottr_string(wikitext)
    # combine lists and strip all whitespaces to single ' ' per line and then remove duplicates

    old_prefixes.extend(prefixes)
    prefixes = set([" ".join(foo.split()) for foo in old_prefixes])



    # Step 4: POST request to edit a page

    new_text = "Put here all your prefixes used in ottr templates.\n<ottr>\n{0}\n</ottr>".format('\n'.join(prefixes))

    PARAMS_3 = {
        "action": "edit",
        "title": OTTR_PREFIX_PAGENAME,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": new_text
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()
    logging.info(DATA)

    return dict(DATA)


def edit_or_create_page(titles, texts, mediawiki_url, bot_user_name, bot_user_password, append=False, create_only=False):
    # TODO ERROR HANDLING

    # TODO BATCH PROCESSING ...
    # I dont think its supported by the mediawiki api ...
    S = requests.Session()

    # use urlparse or similar here!
    #URL  = urllib.parse.urljoin(mediawiki_url, 'api.php')
    #print(URL)
    URL = f"{mediawiki_url}/api.php"


    CSRF_TOKEN = wikiapi_login(S, URL, bot_user_name, bot_user_password)

    datas = []
    timestamps = []


    for title, text in zip(titles, texts):
        timer = time.time()
        # Step 4: POST request to edit a page
        if not append:
            PARAMS_3 = {
                "action": "edit",
                "title": title,
                "token": CSRF_TOKEN,
                "format": "json",
                "text": text
            }
        else:
            PARAMS_3 = {
                "action": "edit",
                "title": title,
                "token": CSRF_TOKEN,
                "format": "json",
                "appendtext": text
            }

        if create_only:
            PARAMS_3 = {
                "action": "edit",
                "title": title,
                "token": CSRF_TOKEN,
                "format": "json",
                "text": text,
                'createonly': True
            }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        timestamps.append(datetime.now().strftime("%d-%m-%y %H:%M:%S"))
        logging.info(DATA)

        datas.append(dict(DATA))


    return datas, timestamps
