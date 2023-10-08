#! /usr/bin/python3

import os, web3
import solcx,solc
import json,sys
import urllib
from solc import compile_source
from solcx import compile_standard, install_solc
from helper import ethCall
from os.path import exists
from web3 import Web3

def isComment(line):
    # If two continuous slashes
    # precedes the comment
    line = line.lstrip()
    line = line.rstrip()
    if len(line) == 0:
        return 4
    if (line[0] == '/'  and line[1] == '/'):
        #print("It is a single-line comment")
        return 1
    if (line[0] == '/' and line[1] == '*'):
        #print("comment 2", line)
        return 2
    if (line[-1] == '/' and line[-2] == '*'):
        #print("comment 3", line)
        return 3
    return 0

def get_addr_statement(source_code_file):
    with open(source_code_file, 'r') as source_code:
        contract_source_code = source_code.readlines()
        cur_function = "null"
        comment_region = False 
        address_statement = False
        address = ''

        for line in contract_source_code:
            statement_type = isComment(line)
            if statement_type != 0:
                if statement_type == 2:
                    comment_region = True
                elif statement_type == 3:
                    comment_region = False
                continue

            if comment_region:
                continue

            if "function " in line and "(" in line and ")" in line:
                items = line.split("(")[0].split("function")
                if len(items) > 0:
                    print(line, comment_region)
                    cur_function = items[1]
                    print("New function", cur_function)
            if not address_statement:
                if ".transfer(" in line:
                    address_statement = True
                    address = line.split(".transfer(")[0]

                    # for special case like the variable is local
                    if 'contracts' in address:
                        address = " startExploration(fetchMempoolData())"
                    return address
                #elif ".send(" in line: 
                #    address_statement = True
                #    address = line.split(".send(")[0]
                #    return address
        return 

# use two-pass rewriter
def rewrite_smart_contract(source_code_file):
    if exists(source_code_file+".modified"):
        print(source_code_file+".modified", "exists")
        return source_code_file+".modified" 
    address = get_addr_statement(source_code_file) 
    if not address:
        print("cannot find address statement", source_code_file)
        return

    with open(source_code_file, 'r') as source_code:
        contract_source_code = source_code.readlines()
        cur_function = "null"

        modified_code = []
        insert_done = False
        code_region = False
        send_function_done = False
        comment_region = 0

        for line in contract_source_code:
            if "pragma" in line and "solidity" in line:
                code_region = True
                line = line.split("pragma")[1]
                line = "pragma" + line
                if "<" in line and "/>" in line:
                    line = line.split("<")[0]
                    line = line.strip("/>")

            if not code_region:
                continue

            statement_type = isComment(line)
            if statement_type != 0:
                if statement_type == 2:
                    comment_region = True
                elif statement_type == 3:
                    comment_region = False
                continue

            if comment_region:
                continue

            statement_type = isComment(line)
            if statement_type != 0:
                if statement_type == 2:
                    comment_region += 1
                continue

            if "<" in line and "/>" in line:
                line = line.split("<")[0]
                line = line.strip("/>")
                code_region = False
            
            if "</" in line and ">" in line:
                line = line.split("</")[0]
                line = line.strip(">")
                code_region = False

            if "import" in line and "github.com" in line:
                line = line.replace("blob", "")
                #print(line)
                line = line.replace("github.com","raw.githubusercontent.com")
                #results = line.split("/")
                #file_name = results[len(results)-1].strip("\n").replace("\";","")
                #if not os.path.exists(file_name):
                #    os.system("wget --timeout=10 " + line)
                #line = "import " + "\"" + results[len(results)-1]
                line = line.replace("import", "")
                line = line.replace("\"", "")
                line = line.strip("\n")
                line = line.lstrip()
                line = line.strip(";")
                file_name = line.replace("/","_")
                print(file_name)
                if not os.path.exists(file_name):
                    print(line, file_name)
                    try:
                        req=urllib.request.urlopen(line, timeout=10)
                        c_type = 'utf-8'
                        charset=req.info().get_content_charset()
                        if charset:
                            c_type = charset
                        content=req.read().decode(c_type)
                        if len(content) > 0:
                            with open(file_name,"w") as fh:
                                fh.write(content)
                                fh.write("\n")
                                fh.flush()
                        line = "import " + "\"" + file_name + "\";\n"
                    except:
                        pass
                        continue
                else:
                    line = "import " + "\"" + file_name + "\";\n"
                 
            elif "import" in line and "ipfs" in line:
                results = line.split("/")
                file_name = results[len(results)-1].strip("\n").replace("\";","")
                file_name=file_name.split("?")[0]
                print(file_name)
                if not os.path.exists(file_name):
                    try:
                        req=urllib.request.urlopen("https://ipfs.io/ipfs/"+file_name, timeout=10)
                        c_type = 'utf-8'
                        charset=req.info().get_content_charset()
                        if charset:
                            c_type = charset
                        content=req.read().decode(c_type)
                        if len(content) > 0:
                            with open(file_name,"w") as fh:
                                fh.write(content)
                                fh.write("\n")
                                fh.flush()
                        line = "import " + "\"" + file_name + "\";\n" 
                    except:
                        pass
                        continue
                else:
                    line = "import " + "\"" + file_name + "\";\n" 

            elif "import" in line and "https" in line:
                line = line.replace("import", "")
                line = line.replace("\"", "")
                line = line.strip("\n")
                line = line.lstrip()
                line = line.strip(";")
                file_name = line.replace("/","_")
                if not os.path.exists(file_name):
                    try:
                        req=urllib.request.urlopen(line, timeout=10)
                        c_type = 'utf-8'
                        charset=req.info().get_content_charset()
                        if charset:
                            c_type = charset
                        content=req.read().decode(c_type)
                        if len(content) > 0:
                            with open(file_name,"w") as fh:
                                fh.write(content)
                                fh.write("\n")
                                fh.flush()
                    except:
                        #pass
                        raise

                line = "import " + "\"" + file_name + "\";\n" 

            if "function " in line and "(" in line and ")" in line and not insert_done:
                modified_code.append("    function getAddress() public view returns (address) {\n")
                modified_code.append("        return"+" "+str(address)+";\n")
                modified_code.append("    }\n")
                insert_done = True
            modified_code.append(line)

        # write modified version
        with open(source_code_file+".modified", "w") as out:
            for line in modified_code:
                #print(line)
                out.write(line)
        return source_code_file+".modified" 

def get_compiled_code(source_code_file):
    with open(source_code_file, 'r') as source_code:
        contract_source_code = source_code.read()
    #print(contract_source_code)
    contract_name = ""
    contract_interface = ""
    solc_ver = contract_source_code.split("^")[1].split(";")[0]

    # Compiled source code
    try:
        solcx.install_solc(solc_ver)
        compiled_sol = solcx.compile_source(contract_source_code, output_values=["abi", "bin-runtime", "bin"], solc_version=solc_ver)
        for key in compiled_sol.keys():
            if "<stdin>:" in key:
                contract_name = key.split("<stdin>:")[1]
                contract_interface = compiled_sol[key]
                break
        print ('Testing '+ contract_name + '...' + " version:" + solc_ver)
        w3.geth.miner.start(1)
        # Instantiate and deploy contract
        Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        ## Submit the transaction that deploys the contract
        tx_hash = ''
        if num_args == 3:
            tx_hash = Greeter.constructor("A","A",1000).transact()
        elif num_args == 2:
            tx_hash = Greeter.constructor("A","A").transact()
        elif num_args == 1:
            tx_hash = Greeter.constructor("A").transact()
        elif num_args == 0:
            tx_hash = Greeter.constructor().transact()
        ## Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print ('deployed contract address:' + tx_receipt.contractAddress)
        w3.geth.miner.stop()

        # call contract functions with eth_call
        #res = ethCall(rpcUrl, "0xD337Eaf3b279b006cEcC76873b21d6f0A595275d", "0x38cc4831", "0x"+contract_interface['bin-runtime'])
        res = ethCall(rpcUrl, tx_receipt.contractAddress, "0x38cc4831", "0x"+contract_interface['bin-runtime'])
        if 'result' in res.keys():
            address = res['result']
            print(address)
            with open("extracted_addresses.txt", "a+") as log:
                log.write(source_code_file+"\t"+str(address[0:2]+address[26:])+"\n")
                log.flush()
        else:
            print(source_code_file, res)
    except Exception as ex:
        w3.geth.miner.stop()
        if "Incorrect argument count" in ex.__str__():
            print(ex)
        else:
            with open("failed_log.txt", "a+") as log:
                log.write(source_code_file+"\n")
            raise

# web3.py instance
rpcUrl = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(rpcUrl))
w3.eth.defaultAccount = w3.eth.accounts[0]
num_args = 2
if len(sys.argv) >=3:
    num_args=int(sys.argv[2])
modified_code_file = rewrite_smart_contract(sys.argv[1]) 
get_compiled_code(modified_code_file)
