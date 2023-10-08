#! /usr/bin/python3
import os, web3
import json,sys
import urllib
from web3 import Web3
import requests, time
from bs4 import BeautifulSoup

rpcUrl = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(rpcUrl))
baseurl = "https://etherscan.io/find-similar-contracts?a="

def call(baseurl, addr, out):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    noHigh=False
    for p in range(1, 101):
        if noHigh:
            break
        url = baseurl + str(addr) + "&mt=1&m=low&ps=100&p="+str(p)
        print(url)
        r=requests.get(url, headers=headers)
        html = r.content.decode()
        parsed_html = BeautifulSoup(html, features="lxml")
        #print(parsed_html.body)
        res = parsed_html.body.find('tbody', attrs={'id':'ContentPlaceHolder1_tbodyTxnTable'}).text
        if len(res) > 100:
            res_list = res.split("   Decode Compare Diff")
            for item in res_list:
                if len(item) > 10:
                    #print(item)
                    txhash = item.split()[0].split("Ethereum")[1]
                    similarity = item.split()[1]
                    address = w3.eth.getTransactionReceipt(txhash)['contractAddress']
                    if similarity == "high":
                        print(addr, address, similarity)
                        out.write(addr+"\t"+address+"\t"+similarity+"\n")
                    else:
                        noHigh = True
                        break
            time.sleep(0.1)
        else:
            print(addr, p, "done")
            break

#### main ####
with open(sys.argv[1],"r") as f:
    with open("similar_contracts_addr_high.data", "a+") as out:
        lines = f.readlines()
        for line in lines:
            contract_addr = line.split()[0]
            if contract_addr in olds:
                continue
            print(contract_addr)
            call(baseurl,contract_addr, out)
