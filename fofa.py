"""
Author         : Sp4ce
Date           : 2021-04-28 17:04:51
LastEditors    : Sp4ce
LastEditTime   : 2021-04-29 14:49:15
Description    : Challenge Everything.
"""

import requests
import json
import base64
import urllib.parse
import time

API_KEY = ""  # API KEY
FOFA_EMAIL = ""  # Account

VERIFY_API = "https://fofa.so/api/v1/info/my?email={FOFA_EMAIL}&key={API_KEY}"
SEARCH_API = "https://fofa.so/api/v1/search/all?email={FOFA_EMAIL}&key={API_KEY}&qbase64={B64_DATA}&size=100&page={page}"


FULL_FILE = "result-{time}.txt".format(
    time=time.strftime("%Y%m%d%H%M%S", time.localtime())
)
IP_FILE = "IP-{time}.txt".format(time=time.strftime("%Y%m%d%H%M%S", time.localtime()))

HEADERS = {}
HEADERS[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

TIMEOUT = 10


class Fofa:
    def __init__(self):
        self.API_KEY = API_KEY
        self.FOFA_EMAIL = FOFA_EMAIL
        self.TIMEOUT = TIMEOUT

    def printBanner(self):
        print(
            """
$$$$$$$$\\  $$$$$$\\  $$$$$$$$\\  $$$$$$\\         $$$$$$\\            $$\\       $$\\                     
$$  _____|$$  __$$\\ $$  _____|$$  __$$\\       $$  __$$\\           \\__|      $$ |                    
$$ |      $$ /  $$ |$$ |      $$ /  $$ |      $$ /  \\__| $$$$$$\\  $$\\  $$$$$$$ | $$$$$$\\   $$$$$$\\  
$$$$$\\    $$ |  $$ |$$$$$\\    $$$$$$$$ |      \\$$$$$$\\  $$  __$$\\ $$ |$$  __$$ |$$  __$$\\ $$  __$$\\ 
$$  __|   $$ |  $$ |$$  __|   $$  __$$ |       \\____$$\\ $$ /  $$ |$$ |$$ /  $$ |$$$$$$$$ |$$ |  \\__|
$$ |      $$ |  $$ |$$ |      $$ |  $$ |      $$\\   $$ |$$ |  $$ |$$ |$$ |  $$ |$$   ____|$$ |      
$$ |       $$$$$$  |$$ |      $$ |  $$ |      \\$$$$$$  |$$$$$$$  |$$ |\\$$$$$$$ |\\$$$$$$$\\ $$ |      
\\__|       \\______/ \\__|      \\__|  \\__|$$$$$$\\______/ $$  ____/ \\__| \\_______| \\_______|\\__|      
                                        \\______|        $$ |                                        
                                                        $$ |                                        
                                                        \\__|     
                            Author:Sp4ce
                            Github:github.com/NS-Sp4ce                                   
        """
        )

    def checkValid(self):
        self.infoMsg("Now check for account validate.")
        res = requests.get(
            VERIFY_API.format(
                API_KEY=API_KEY, FOFA_EMAIL=urllib.parse.quote(FOFA_EMAIL)
            ),
            headers=HEADERS,
        )
        resData = json.loads(res.text)
        if "error" not in resData:
            self.successMsg("Account Confirmed.")
            self.successMsg(
                "Hello "
                + resData["username"].upper()
                + " "
                + " Email: "
                + resData["email"]
            )
            return True
        else:
            self.errorMsg(resData["errmsg"])
            return False

    def searchData(self):
        try:
            res = requests.get(
                SEARCH_API.format(
                    FOFA_EMAIL=self.FOFA_EMAIL,
                    API_KEY=self.API_KEY,
                    B64_DATA=self.inputData.decode("utf8"),
                    page=1,
                ),
                headers=HEADERS,
            )
            self.infoMsg(
                "Your full search url: "
                + SEARCH_API.format(
                    FOFA_EMAIL=self.FOFA_EMAIL,
                    API_KEY=self.API_KEY,
                    B64_DATA=self.inputData.decode("utf8"),
                    page=1,
                )
            )
            result = json.loads(res.text)
            self.successMsg("Searching Text: " + result["query"])
            self.successMsg("Searching Mode: " + result["mode"])
            self.successMsg("Searching Records: " + str(result["size"]))
            confirm = input("Want to SAVE DATA? (Y/N)")
            if "y".upper() in confirm or "y".lower() in confirm:
                self.successMsg(
                    "OK now save {counts} FULL result data(s) as result.txt, IP as ip.txt.".format(
                        counts=str(result["size"])
                    )
                )
                self.saveData(res.text, str(result["size"]))
            else:
                self.infoMsg("OK Bye~")
        except:
            self.errorMsg("Something Error.")

    def saveData(self, result, range):
        jsonData = json.loads(result)
        self.resultsData = jsonData["results"]
        if len(self.resultsData) % int(range) == 0:
            page = 1
            self.writeFile(self.resultsData, page)
        else:
            pageCount = int(range) / 100
            self.getMorePageData(int(pageCount))
        self.successMsg("Save {counts} datas success.".format(counts=range))

    def getMorePageData(self, pages):
        for page in range(pages + 1):
            res = requests.get(
                SEARCH_API.format(
                    FOFA_EMAIL=self.FOFA_EMAIL,
                    API_KEY=self.API_KEY,
                    B64_DATA=self.inputData.decode("utf8"),
                    page=page + 1,
                ),
                headers=HEADERS,
            )
            jsonData = json.loads(res.text)
            self.resultsData = jsonData["results"]
            self.writeFile(self.resultsData, page + 1)

    def writeFile(self, resultsData, page):
        self.infoMsg("Now processing page {page}.".format(page=page))
        for data in resultsData:
            with open(
                FULL_FILE,
                "a+",
            ) as f:
                f.write(data[0] + "\n")
            with open(
                IP_FILE,
                "a+",
            ) as f:
                f.write(data[1] + "\n")

    def run(self):
        self.printBanner()
        if self.checkValid():
            data = input("Input your search data: ")
            self.data = data
            self.inputData = base64.b64encode(bytes(self.data, encoding="utf-8"))
            self.searchData()

    def errorMsg(self, msg):
        print("[!] Error: " + msg)

    def infoMsg(self, msg):
        print("[*] " + msg)

    def successMsg(self, msg):
        print("[+] " + msg)


if __name__ == "__main__":
    main = Fofa()
    main.run()
