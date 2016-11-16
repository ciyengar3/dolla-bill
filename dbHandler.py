#!/usr/bin/python
'''
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

collection = MongoClient('mongodb://ciyengar3:crishna1@ds151697.mlab.com:51697/dollabill?authMode=scram-sha1&rm.tcpNoDelay=true')["DollaBill"]
print collection
todaydate='20161112'

def addTransaction(currTrans):
    # Connect to the DB
    transaction_collection = collection["transactions"]
    transaction_collection.insert(currTrans)


def totalCategoryCount(category, cost):
    total_cost_by_category = collection["total_cost_by_category"]
    print total_cost_by_category
    found_category = total_cost_by_category.find_one({"category":category})
    if found_category:
        total_cost_by_category.update(
            {
                "category": category
            },
            {
            "$set": {
                "total_spent": found_category['total_spent'] + cost,
            }
            }
        )
        return
    total_cost_by_category.insert(
        {
            "category": category,
            "total_spent": cost
        }
    )


def updatePersonalExpenses(person, cost, category, date):
    personal_spending = collection["personal_spending_category"]
    person_document = personal_spending.find_one({"p_id": person})
    if person_document:
        if category in person_document:
            category_cost = person_document[category] + cost
        else:
            category_cost = cost
        personal_spending.update(
            {
                "p_id" : person
            },
            {
                "$set": {
                    category : category_cost
                }
            }
        )
    else:
        personal_spending.insert(
            {
                "p_id": person,
                 category : cost
            }
        )


def within_last_month(date):
    if int(today_date) - int(date) <= 30:
        return True
    else:
        return False


def within_last_week(date):
    if int(today_date) - int(date) <= 7:
        return True
    else:
        return False

def update_spending_timeline(person, date, cost):
    timeline_collection = collection['timeline']
    if within_last_month(date):
        person_document = timeline_collection.find_one({"p_id": person})
        if within_last_week(date):
            if person_document:
                if 'withinMonth' in person_document and 'withinWeek' in person_document:
                    new_week = person_document['withinWeek'] + cost
                    new_month = person_document['withinMonth'] + cost
                elif 'withinMonth' in person_document:
                    new_week = cost
                    new_month = person_document['withinMonth'] + cost
                else:
                    new_week = cost
                    new_month = cost
                timeline_collection.update(
                    {
                        "p_id": person
                    },
                    {
                        "$set": {
                            "withinMonth": new_month,
                            "withinWeek": new_week
                        }
                    }
                )
            else:
                timeline_collection.insert(
                    {
                        "p_id": person,
                        "withinMonth": cost,
                        "withinWeek": cost
                    }
                )
        else:
            if person_document:
                if 'withinMonth' in person_document:
                    new_month = person_document['withinMonth']
                else:
                    new_month = cost
                timeline_collection.update(
                    {
                        "p_id": person
                    },
                    {
                        "$set": {
                            "withinMonth": new_month
                        }
                    }
                )
            else:
                timeline_collection.insert(
                    {
                        "p_id": person,
                        "withinMonth": cost
                    }
                )

def getTotalCategoryTable():
    catCol = collection['total_cost_by_category'].find()
    print '\n All data from Category Database \n'
    for category in catCol:
        print category
    return collection['total_cost_category']

def getPersonalExpenses(person):
    empCol = collection['personal_spending_category'].find()
    print '\n All data from Personal Category Database \n'
    for emp in empCol:
        print emp

    return collection['personal_spending_category']

def getTimelineTable(person):
    empCol = collection['timeline'].find()
    print '\n All data from Timeline Database \n'
    for emp in empCol:
        print emp
    return collection['timeline']

'''

