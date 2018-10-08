#!/usr/bin/python
import os
#import urllib2 library for making url requests. Note this library must be installed before use.
import urllib2
#import etree library for parsing xml responses. Note this library must be installed before use.
from lxml import etree
#NOTE: Written for Python 2.7

"""Creates list of transaction values which will be used as keys in dictionaries
This design stipulates that the transaction must be part of this list in order to have
an output file location created when the script is run.
"""
transactions = ["login",
                "logout",
                "clear",
                "session",
                "listdir",
                "getdir",
                "putdir",
                "mkdir",
                "gettab",
                "tabinfo",
                "puttab",
                "query",
                "getdata",
                "querydata",
                "savefile",
                "savetable",
                "upload",
                "merge",
                "droptable",
                "dropdir",
                "drop",
                "move",
                "order"]

startinputloc = "inputFiles/"
endinputloc = "In.xml"
startoutputloc = "outputFiles/"
endoutputloc = "Out.xml"
inputfiledict = {}
outputfiledict = {}

#populate dictionaries with the input and the output file paths. Note: input files must be created before used
for transaction in transactions:
    inputfiledict[transaction] = startinputloc + transaction + endinputloc
    outputfiledict[transaction] = startoutputloc + transaction + endoutputloc

def post(url=None, body=None):
    return urllib2.urlopen(urllib2.Request(url, body, headers={'Content-Type': 'text/xml'})).read().decode('utf-8')

#create a 1010data session, capture the encrypted password and SID, then return a session URL that can be used for subsequent transactions
def createsession(username,password):
    url = "https://www2.1010data.com/cgi-bin/prod-stable/gw.k?protocol=xml-rpc&apiversion=3&uid=" + username
    response = post(url + "&pswd=" + password + "&api=login&kill=possess")
    tree = etree.fromstring(response)
    session = {}
    for child in tree:
        session[child.tag] = child.text
    sessionurl = url + "&pswd=" + session['pswd'] + "&sid=" + session['sid'] + "&api="
    return sessionurl

#Generalized function for calling any transaction (except login, because it's used in createsession function)
def calltransaction(transName, sessionurl, inputfile=None):
    #some transactions don't need/want input files, so ignore this parameter if no input file is passed to function call
    if inputfile is None:
        transactionResponse=post(sessionurl + transName)
    else:
        input=open(inputfiledict[transName], "r").read()
        transactionResponse=post(sessionurl + transName, input)
    return transactionResponse

"""
In __main__, a session URL is created using the createsession() function. Valid
credentials must be passed to this function for the session to be created.
The calltransaction function is called twice, once to apply a query to a table
using the query transaction, then again to retrieve the results of the query
using the getdata transaction. Results of the second call are written to an
output file.
"""
if __name__ == '__main__':
    sessionurl = createsession() #enter valid user credentials as arguments (strings)
    calltransaction("query", sessionurl, inputfiledict['query'])
    response = calltransaction("getdata", sessionurl, inputfiledict['getdata'])
    fp = open(outputfiledict['getdata'],'w') #note the use of the transaction name as the key to the output file dictionary.
    fp.write(response)
    fp.close()
    calltransaction("logout", sessionurl)
