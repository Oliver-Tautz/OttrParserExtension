import argparse
import logging
import textwrap
from pathlib import Path
import json
import subprocess
import configparser
from urllib.parse import urlparse, urljoin
import json
from stOttrWikiTranslater import parse_stottr_string, write_stottr_to_mediawiki_xml, _find_ottr_tag, _find_ottr_instance
from datetime import datetime
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import requests
from ottrServerUtils import *
from includes.ottrToSmwPython.Settings import API_QUERY_LIMIT
import logging

### App and template setup

app = Flask(__name__)

api = Api(app, version='0.1', title='OttrApi',
          description='An api to interact with the Otter-SemanticMediaWiki.',
          )

ottr_namespace_server = api.namespace('ottr_server',
                                      description="Server related functions, e.g. change server settings and ping to see if it is up")
ottr_namespace_get = api.namespace('ottr_get', description="request .stottr files from the wiki.")
ottr_namespace_post = api.namespace('ottr_post', description="post your .stottr files into the wiki.")

### Model Docs
stottr_file = api.model('stottr_input_file', {
    'data': fields.String(OTTR_EXAMPLE,
                          description='.stottr file in utf8 string encoding. Can contain templates, instances and prefixes.'),
    'template_namespace': fields.String('Template',
                                        description='namespace added in front of the template pages in OttrWiki \n can be empty.'),
    'instance_namespace': fields.String('',
                                        description='namespace added in front of the instance pages in OttrWiki \n can be empty.'),
    'overwrite': fields.Boolean(True,
                                description='Overwrite existing pages. If this is set to False only new pages will be created. Prefixes are added regardless'),

})

stottr_output = api.model('stottr_output', {
    'templates': fields.String(description="templates from wiki parsed to .stottr syntax."),
    'instances': fields.String(description="instances from wiki parsed to .stottr syntax."),
    'prefixes': fields.String(description="prefixes from wiki parsed to .stottr syntax.")
})

mediawiki_edit_result = api.model('mediawiki_edit_result', {
    'result': fields.String(),
    'pageid': fields.Integer(),
    'title': fields.String(),
    "nochange": fields.String(),
    "watched": fields.String(),
})

mediawiki_edit = api.model('mediawiki_edit', {
    'edit': fields.Nested(mediawiki_edit_result)

})

mediawiki_edits = api.model('mediawiki_edits', {
    'edits': fields.List(fields.Nested(mediawiki_edit))

})


## Helper Functions.

def _parse_config(path):
    cfparser = configparser.ConfigParser()
    cfparser.read(path)
    params = {}

    params['port'] = int(cfparser['SERVER']['port'])
    params['wikiurl'] = urlparse(str(cfparser['WIKI']['wikiurl'])).geturl()
    params['bot_user_name'] = str(cfparser['WIKI']['bot_user_name'])
    params['bot_user_password'] = str(cfparser['WIKI']['bot_user_password'])
    params['logfile_path'] = str(cfparser['SERVER']['logfile_path'])

    return params


def split(list, sublist_size):
    sublists = []
    for i in range(0, len(list), sublist_size):
        sublists.append(list[i:i + sublist_size])
    return sublists


def get_all_pagetexts(titles, S, URL):
    titles_split = split(titles, API_QUERY_LIMIT)

    pages = []
    for titles in titles_split:
        pages.extend(get_page_texts(titles, S, URL)['query']['pages'].values())
    return pages


## Server Functions GET

@ottr_namespace_server.route("/api/ping", methods=['GET'])
class Ping(Resource):
    @api.response(200, 'Sucess')
    @api.doc(body=None)
    def get(self):
        """
        return friendly string if the server is up :)

        """

        return jsonify(f"Hello. The Ottr Server is up :) Go to {request.host_url} for documentation.")  #


@ottr_namespace_get.route("/api/get_instances", methods=['GET'])
class get_stottr_instances(Resource):
    @api.response(200, 'Sucess', stottr_output)
    @api.response(500, 'Sucess')
    @api.doc(body=None)
    def get(self):
        """
        return all instances in the wiki in stottr format.

        bodyless request.

        """
        S = requests.Session()
        URL = urljoin(server_cfg['wikiurl'], 'api.php')

        # This tops out at 500... what to do about that?
        # Use cmsort by timestamp and then cmstart. Only need to see when its finished???!!!
        # Could also use cmcontinue!

        PARAMS = {'action': 'query', 'cmtitle': 'Category:OTTR Instance', 'cmlimit': 'max', 'list': 'categorymembers',
                  'format': 'json'}
        R = S.get(url=URL, params=PARAMS)

        DATA = R.json()

        titles = [x['title'] for x in DATA['query']['categorymembers']]

        while 'continue' in DATA.keys():
            PARAMS = {'action': 'query', 'cmtitle': 'Category:OTTR Instance', 'cmlimit': 'max',
                      'list': 'categorymembers',
                      'format': 'json', 'cmcontinue': DATA['continue']['cmcontinue']}
            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()
            titles = titles + [x['title'] for x in DATA['query']['categorymembers']]

        pages = get_all_pagetexts(titles, S, URL)

        pagetexts = [x['revisions'][0]['*'] for x in pages]
        # print(pagetexts)

        texts = []
        for text in pagetexts:
            tag = _find_ottr_tag(text)
            if tag:
                texts.append(tag)
            else:
                inst = _find_ottr_instance(text)
                if inst:
                    texts.append(inst)

        return jsonify({'templates': None, 'prefixes': None, 'instances': '\n'.join(texts)})


@ottr_namespace_get.route("/api/get_templates", methods=['GET'])
class get_stottr_templates(Resource):
    @api.response(200, 'Sucess', stottr_output)
    @api.doc(body=None)
    def get(self):
        """
        return all templates in the wiki in stottr format.


        bodyless request.
        """
        S = requests.Session()
        URL = urljoin(server_cfg['wikiurl'], 'api.php')
        # This tops out at 500... what to do about that?
        PARAMS = {'action': 'query', 'cmtitle': 'Category:OTTR Template', 'cmlimit': 'max', 'list': 'categorymembers',
                  'format': 'json'}
        R = S.get(url=URL, params=PARAMS)

        DATA = R.json()
        titles = [x['title'] for x in DATA['query']['categorymembers']]

        while 'continue' in DATA.keys():
            PARAMS = {'action': 'query', 'cmtitle': 'Category:OTTR Template', 'cmlimit': 'max',
                      'list': 'categorymembers',
                      'format': 'json', 'cmcontinue': DATA['continue']['cmcontinue']}
            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()
            titles = titles + [x['title'] for x in DATA['query']['categorymembers']]

        pages = get_all_pagetexts(titles, S, URL)

        pagetexts = []

        for page in pages:
            try:
                pagetexts.append(page['revisions'][0]['*'])
            except KeyError:
                logging.warning('page \'{}\' has no usable text, skipping.'.format(page['title']))
            except Exception as e:
                logging.warning('Unexpected error while parsing page \'{}\', {}:{}'.format(page, type(e), e))
        #        pagetexts = [x['revisions'][0]['*'] for x in pages]
        # print(pagetexts)

        texts = []
        for text in pagetexts:
            tag = _find_ottr_tag(text)
            if tag:
                texts.append(tag)
            else:
                inst = _find_ottr_instance(text)
                if inst:
                    texts.append(inst)

        return jsonify({'templates': '\n'.join(texts), 'prefixes': None, 'instances': None})


@ottr_namespace_get.route("/api/get_prefixes", methods=['GET'])
class get_stottr_prefixes(Resource):
    @api.response(200, 'Sucess', stottr_output)
    @api.doc(body=None)
    def get(self):
        """
        return all prefixes in the wiki in stottr format.


        bodyless request.
        """
        S = requests.Session()
        URL = urljoin(server_cfg['wikiurl'], 'api.php')

        PARAMS_GET = {'action': 'query', 'prop': 'revisions', 'titles': OTTR_PREFIX_PAGENAME, 'format': 'json',
                      'rvprop': 'content'}

        R = S.get(url=URL, params=PARAMS_GET)
        DATA = R.json()
        wikitext = DATA['query']['pages'][list(DATA['query']['pages'].keys())[0]]['revisions'][0]['*']

        prefixes, _ = parse_stottr_string(wikitext)

        return jsonify({'templates': None, 'instances': None, 'prefixes': ''.join(prefixes)})


@ottr_namespace_get.route("/api/get_all", methods=['GET'])
class get_stottr_all(Resource):
    @api.response(200, 'Sucess', stottr_output)
    @api.doc(body=None)
    def get(self):
        """
        return all templates, instances  and prefixes in the wiki in stottr format.



        bodyless request.


        """

        template_class = get_stottr_templates()
        instance_class = get_stottr_instances()
        prefix_class = get_stottr_prefixes()

        templates_json = template_class.get().json
        instances_json = instance_class.get().json
        prefix_json = prefix_class.get().json

        return jsonify(
            {'templates': templates_json['templates'], 'instances': instances_json['instances'],
             'prefixes': prefix_json['prefixes']})


@ottr_namespace_post.route("/api/stottr_file", methods=['POST'])
class stottr_file(Resource):

    @api.doc(body=stottr_file, responses={201: "Created Stottr Pages Sucessful", 400: "Bad Request"})
    def post(self):
        """
        Import stottr file.

        Send full text of .stotter File and parse all prefixes, templates and instances in it.

        Template pages will be created in the passed template namespace and named like the template.
        **WARNING:** Duplicates will overwrite existing pages!

        Instance pages will be created in the passed instance namespace and named by the called template followed by a unique 10 char hash.

        Prefixes will be added to the page 'Ottr:OttrPrefixes' in the wiki , skipping duplicates.


        Python example usage:

        ```
        import requests
        file = open('stottr_file.stotter')
        data = file.read()
        file.close()

        body = {"data": data,
                "template_namespace": "Template",
                "instance_namespace": "",
                "overwrite":"True"
        }

        r = requests.post("http://127.0.0.1:5000/ottr_post/api/stottr_file",json=body)

        print(r.text)


        ```



        """
        json_data = request.json
        ottr_string = json_data['data']
        overwrite = json_data['overwrite']
        template_namespace = json_data['template_namespace']
        instance_namespace = json_data['instance_namespace']

        prefixes, things = parse_stottr_string(ottr_string)

        template_titles = []
        instance_titles = []
        templates = []
        instances = []
        # iterate over copy to change original
        for thing in things:
            if is_template(thing):
                title = get_template_name_from_template_string(thing)
                template_titles.append(f"{template_namespace}:{title}")
                templates.append(thing)
            # assuming instance here ...
            else:
                title = f"{get_template_name_from_instance_string(thing)}_I{hash_instance(thing, 10)}"
                instance_titles.append(f"{instance_namespace}:{title}")
                instances.append("\n{0}\n{1}".format(f'# {title}', thing))

        # titles = [f"testimport_{x}" for x in range(len(things))]

        # add ottr tag
        templates = [f"<ottr>{thing}</ottr>" for thing in templates]
        instances = [f"<ottr>{thing}</ottr>" for thing in instances]

        titles = instance_titles + template_titles
        things = instances + templates

        pages,timestamps = edit_or_create_page(mediawiki_url=server_cfg['wikiurl'], titles=titles,
                                    texts=things,
                                    bot_user_name=server_cfg['bot_user_name'],
                                    bot_user_password=server_cfg['bot_user_password'],
                                    append=False, create_only=not overwrite)

        prefix_edit = append_to_prefixes(prefixes=prefixes, mediawiki_url=server_cfg['wikiurl'],
                                         bot_user_name=server_cfg['bot_user_name'],
                                         bot_user_password=server_cfg['bot_user_password'])

        # printable mediawiki edit columns
        pageedits = ''.join(
            [f"|-\n| {p['edit']['title']} || {p['edit']['result']} || {timestamp}\n" for (p,timestamp) in
             zip(pages,timestamps)])

        S = requests.Session()
        current_edit_text = get_pagetext_single("Template:Ottr:ApiEdits", S, server_cfg['wikiurl'] + 'api.php').split(
            '\n')
        last_line = current_edit_text[-1]
        current_edit_text = '\n'.join(current_edit_text[:-1])

        new_edit_text = current_edit_text + pageedits + '\n' + last_line

        edit_or_create_page(mediawiki_url=server_cfg['wikiurl'], titles=["Template:Ottr:ApiEdits"],
                            texts=[new_edit_text],
                            bot_user_name=server_cfg['bot_user_name'],
                            bot_user_password=server_cfg['bot_user_password'],
                            append=False, create_only=False)

        return pages, 201


# This is loaded once on server startup from the .cfg file. For changes the server needs to be restarted.
global server_cfg

if __name__ == '__main__':
    # TODO implement https?
    # TODO implement choose port
    # TODO implement argparse etc.

    parser = argparse.ArgumentParser(
        prog='OttrServer',
        description='An api to send and receive .stottr files to and from mediawiki with OttrParserExtension')
    parser.add_argument('--config', type=str, default="ottrServerExampleConfig.cfg",
                        help="path to config file. Copy example and change values as desired.")
    parser.add_argument('--base-url', type=str, default=None,
                        help="mediawiki base url. Overwrites config")

    args = parser.parse_args()

    if not Path(args.config).is_file():
        logging.critical("Config path does not exist!")
        exit(-1)

    try:
        server_cfg = _parse_config(
            args.config)

        logging.basicConfig(filename=server_cfg['logfile_path'], level=logging.DEBUG, filemode='a')
        logging.info(f" ----- Config parsed sucessfully :) Starting Server at {datetime.now()} ----- ")



    except KeyError as key:
        logging.critical(f"Could not find or parse config. Missing required key {key} ")
        exit(-1)
    except Exception as e:
        logging.critical("Could not find or parse config. Please check!")
        print(type(e))
        exit(-1)

    if args.base_url:
        server_cfg['wikiurl'] = args.base_url

    app.run(port=server_cfg['port'], host="0.0.0.0", debug=True, threaded=False)
