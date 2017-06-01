# README

## About chatbot

bot username

+ @miuwa_bot

功能

+ 回覆訊息

+ 傳圖片

+ 設置keyboard方便使用 

+ 使用資料庫記帳及管理帳目資料 

+ 抓取兩則熱門體育新聞 [TSNA專業體育新聞](https://www.google.com.tw/search?client=safari&rls=en&q=www.tsna.com.tw&ie=UTF-8&oe=UTF-8&gfe_rd=cr&ei=J9EvWeWmO_D88we6yL-gAw)

+ example :

    ![](https://i.imgur.com/ccLd4oA.jpg =250x450)
    
    ![](https://i.imgur.com/8EAzZao.jpg =250x450)


## Finite State Machine

![](https://i.imgur.com/j6IrRh1.jpg)

## Run code 

```sh
./ngrok http 5000
```

* have database
* need to run dbhelper.py first to set up  the table

```sh
python3 dbhelper.py

python3 app.py
```

## Interact with my chatbot


The initial state : `user`

從`user`出發有三條state，由 advance 觸發，完成transition後 `go_back` 或 `back` 回 `user`

在所有state中，輸入文字back也可以回 `user`

開始使用時可輸入/start到`user`state
*****

``` 
user -> state11 -> state12 -> state13 -> user 
                            | state11 -> state12 -> state13 ->user    
```                          

1. 記帳功能

+ `user`  

    input : 1
    
    + `state11` 
     
        input : 固定格式文字(日期 項目 金額)  ex: 6/1 晚餐 200 -----> 中間需空一格
        
        + `state12` 
       
          *設置keyboard
          
          input : yes (到state13)  /  no (回到state11) 
          
            + `state13`  
             
                將資料存入database
                
                reply圖片和 '登記成功囉！'後自動跳回user

           
*****
```
user -> state2 -> check1 -> check2 -> user
                | delete1 -> deleteall -> user
                           | deleteday1 -> deleteday2 ->user
```

2. 查詢或刪除帳目

+ `user`  

    input : 2
    
    + `state2` 
     
        *設置keyboard
        
         input : delete (到`delete1`刪除)  /  check1 (回到`check1`查詢) 
        
        + `check1` 
       
          列出database所有資料後，跳至`check2`
          
            + `check2`
            
              回覆'再接再厲'，自動跳回`user`
            
        + `delete1`
        
            *設置keyboard
           
            input : all (跳至`deleteall`刪除所有資料) / day (跳至`deleteday1`刪除固定筆)
            
            + `deleteall` 
                
                刪除database裡所有資料後跳回`user`
            
            + `deleteday1`
                
                會先印出所有資料方便使用者選擇
                
                input : 資料庫裡的某天日期
                
                + `deleteday2`
 
                 該天資料會被刪除，回覆已刪除後，跳回`user`
                

*****

```
user -> state3 -> state3yes -> user
                | state3no -> state3yes -> user
```

3. 抓取體育新聞

+ `user`  

    input : 3
    
    + `state3` 
     
        *設置keyboard
        
         input : yes (到state3yes)  /  no (回到state3no) 
        
        + `state3no` 
       
          回覆'我才不理你哩'後自動跳至`state3yes`
          
        + `state3yes`  
             
          抓取網路體育新聞資料後，自動跳回`user`  

*****


## Module

```sh
Flask
transitions
pygraphviz
python-telegram-bot
BeautifulSoup
requests
sqlite3
```