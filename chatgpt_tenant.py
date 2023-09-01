# -*- coding: utf-8 -*-

import os
import re
import json
import argparse
import random
from tqdm import tqdm


import openai


openai.api_key = "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"


his = """
tentant Q: Can I book a viewing for the property at 56 Mortimer road tomorrow at 3pm?
Agent: OK, let me check some information first. Do you intend to rent a property with your kids?
tentant Q: yes
Agent: Do you keep any pets
Tenant: Yes, we have a dog.
"""

his1 = """
tentant Q:"Is the property of 56 Mortimer road, BS34, Bristol £2300 per month available?"
A:"Yes, the property of 56 Mortimer Road, BS34,£2300 per month is available. Do you intend to rent a property with your kids?"
Tentant Q: yes
Agent: Do you keep any pets
Tenant: Yes, we have a dog.
"""


#data = {'dialogue':his,'intent':'', 'sql':'','generated_reply':''}

#with open('tenant_data.json','w') as f:
#  f.write(json.dumps(data))

class Tenant_ask():
  def __init__(self,dialogue_history):
    #with open('tenant_data.json','r') as f:
    self.data = {'dialogue':dialogue_history,'intent':'', 'sql':'','generated_reply':''}

  def generation(self):


    ## ------------------------------------------------

    # user intent understanding

    ## ------------------------------------------------
    instruction = """

    Here is the dialogue between the potential tenant and agent, the agent wants to check the avalibility of the house and reply the tenant. Now you need to understand the tent query by fill the json form first

    dialogue is
    """

    instruction_dialogue = """

    json form:

    intent = {
    'address' : '',
    'guarantor' : '',
    'monthly_rent' : '',
    'family_friend' : '',
    'max_tenants number' : '',
    'minimum_tenancy number?' : '',
    'pet_friend' : '',
    'bills' : ''
    }

    if the tenant mentioned the detailed information, just fill the original information in the corresponding slot, if just the asking intent, fill 'asked'. Otherwise, fill None in the slot. Remember, just fill the form, do say anyother words

    only give me the json response and don't say any other words 
    """


    prompt = [
            {'role':'user','content':instruction+self.data['dialogue']+instruction_dialogue}
            ]

    flag = 0
    count = 0
    while True:
      if flag ==1 or count >5:
        break
      try:
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=prompt,
          temperature = 0,
          max_tokens=2000
        )
      except Exception as e:
        print(e)
      flag = 1
      count += 1

    if flag == 0:
      return 'error happen when accessing LLM'

    response = response['choices'][0]['message']['content']
    #print(response)

    self.data['intent'] = response


    ## ------------------------------------------------

    # sql generation

    ## ------------------------------------------------


    sql_instruction = """
    generate the sql only based on the intent json. for 'family_friend', 'guarantor','pet_friend' and 'bills'. if the value is not None. Check whether the database value is 1. For monthly_rent, max_tenants number and minimum_tenancy number, filter the record which meet these specific requirement. The db table is db.tenancy.findOne.

    I mean if these slot in json is None, you don't need to consider it when generate the sql. otherwise, should filter the record with these slot and its value is 1
    """

    sql_prompt = [{'role':'user','content':sql_instruction+ self.data['intent'] + 'only give me the sql for mongodb directly and do not say any other unrelated words'}]

    flag = 0
    count = 0
    while True:
      if flag ==1 or count >5:
        break
      try:
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=sql_prompt,
        temperature = 0,
        max_tokens=2000
        )
      except Exception as e:
        print(e)

      flag = 1
      count += 1

    if flag == 0:
      return 'error happen when accessing LLM'

    response = response['choices'][0]['message']['content']
    #print(response)
    self.data['sql'] = response

    


    ## ------------------------------------------------

    # mimic the db result

    ## ------------------------------------------------

    db_result_simulate_instruction = """

    mimic the below db result example based on the dialogue history

    """

    db_example = """

    "information search from db":{
    "_id": "649a2c8f39240c2af2c1d756",
    "chatbot_company_uuid": "0892e397-2682-4030-9482-248b983d5dd7",
    "source_id": 1,
    "available_from": "2017-09-02T00:00:00.000Z",
    "bills": 0,
    "check_in_date": "2017-09-02T00:00:00.000Z",
    "complete_time": null,
    "council_tax": "Unknown",
    "created_at": "2019-09-03T03:55:16.000Z",
    "deleted_at": null,
    "deposit": 1400,
    "description": "No Admin Fees and No Agent Fees ///STUDENT PROPERTY/// four bedrooms student house in Filton close to UWE, offered furnished\n",
    "dss": 0,
    "epc": "D",
    "expired": 1,
    "family_friend": 0,
    "fireplace": 0,
    "garden": 1,
    "guarantor": 0,
    "head_tenant": "c37f1baa-713d-4b86-bdad-9fb60a61749c",
    "holding_deposit": 20000,
    "live": 0,
    "live_in": 0,
    "max_tenants": 4,
    "minimum_tenancy": 12,
    "minimum_tenancy_days": 0,
    "monthly_rental": 1400,
    "occupied": 1,
    "on_shelf": 0,
    "parking": 1,
    "pay_rent_month_number": 1,
    "pet_friend": 0,
    "property_status": 3,
    "ref": "142771",
    "rent_step": 7,
    "rightmove_description": "",
    "smoker_friend": 0,
    "source": 1,
    "status": 1,
    "student_friend": 1,
    "tenancy_end_time": "2018-09-01T00:00:00.000Z",
    "tenancy_id": "69740037",
    "tenancy_start_time": "2017-09-02T00:00:00.000Z",
    "updated_at": "2022-09-07T14:16:12.000Z",
    "zoopla_description": ""
    }

    """

    db_mimic = [{'role':'user','content':db_result_simulate_instruction+ self.data['dialogue'] + '\n:\n' + db_example + 'only give me the final mimic example, do not say anyother unrelated words'}]

    flag = 0
    count = 0
    while True:
      if flag ==1 or count >5:
        break
      try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=db_mimic,
        temperature = 0,
        max_tokens=2000
        )
      print(e)

      flag = 1
      count += 1

    if flag == 0:
      return 'error happen when accessing LLM'

    response = response['choices'][0]['message']['content']
    #print(response)
    self.data['db_result'] = response


    ## ------------------------------------------------

    # reply generation

    ## ------------------------------------------------

    reply_generation_instruction = """
    Based on the result filterd from DB and the previous dialogue history, generate the reponse to tenant.

    """

    relpy_generation = [{'role':'user','content':reply_generation_instruction+ '\n' + self.data['db_result'] + '\ndialogue history' +self.data['dialogue'] + 'only give me the final reply, do not say anyother unrelated words'}]

    flag = 0
    count = 0
    while True:
      if flag ==1 or count >5:
        break
      try:
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=relpy_generation,
        temperature = 0,
        max_tokens=2000
        )
      except Exception as e:
        print(e)

      flag = 1
      count += 1

    if flag == 0:
      return 'error happen when accessing LLM'

    response = response['choices'][0]['message']['content']
    #print(response)
    self.data['generated_reply'] = response

    return self.data

#tenant_communication = Tenant_ask()

#result = tenant_communication.generation()

#with open('tenant_record.json','w') as f1:
#  f1.write(json.dumps(result))



