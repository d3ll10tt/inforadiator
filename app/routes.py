from flask import render_template, request
from app import app
import os
import json
import re
from app import ansible_facts
from pprint import pprint


@app.route('/')
@app.route('/index')
def index():
    directory = './data/facts_cache/'
    all_platform_facts = ansible_facts.AnsibleFacts(directory)
    try:
        environments = all_platform_facts.get_environment_names()
        tables = []
        for env in environments:
            tables.append({env: all_platform_facts.return_table_data(env)})
    except ansible_facts.AnsibleException as e:
        print(e)

    return render_template('index.html', title='Home', tables=tables, env_names=all_platform_facts.get_environment_names())

@app.route('/rpm_inventory')
def rpm_inventory():
    directory = './data/facts_cache/'
    all_platform_facts = ansible_facts.AnsibleFacts(directory)
    try:
        environments = all_platform_facts.get_environment_names()
        tables = []
        for env in environments:
            tables.append({env: all_platform_facts.return_table_data(env)})
    except ansible_facts.AnsibleException as e:
        print(e)

    return render_template('rpm_inventory.html', title='Home', tables=tables,
                           env_names=all_platform_facts.get_environment_names())

@app.route('/rpm_inventory_searchable', methods=['GET', 'POST'])
def rpm_inventory_searchable():
    directory = './data/facts_cache/'
    all_platform_facts = ansible_facts.AnsibleFacts(directory)
    selected_items = []

    if request.method == "POST":
        if request.form['action'] == 'Update Package List':
            print("update")
            selected_items = request.form.getlist("test")
        elif request.form['action'] == 'Deselect All':
            print("Deselect")
            selected_items = []
        elif  request.form['action'] == 'Select All':
            print("select")
            selected_items = all_platform_facts.get_all_packages()

    else:
        print("first time landing")
        pprint(selected_items)


    try:
        environments = all_platform_facts.get_environment_names()
        tables = []
        for env in environments:
            tables.append({env: all_platform_facts.return_table_data(env, selected_items)})
    except ansible_facts.AnsibleException as e:
        print(e)

    return render_template('rpm_inventory_searchable.html', title='Home', tables=tables,
                           env_names=all_platform_facts.get_environment_names(),
                           pkg_names=all_platform_facts.get_all_packages(), selected_items=selected_items)