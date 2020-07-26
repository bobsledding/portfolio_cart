# portfolio_cart
購物車網站試做

https://bobsledding-cart.herokuapp.com/


環境說明:

    push到heroku，並且利用newrelic持續ping以防free dyno睡著。
    
    deploy到heroku的設定參照django girls(https://djangogirlstaipei.herokuapp.com/tutorials/deploy-to-heroku/?os=windows)
    
    並且參照newrelic的官方的說明進行微調(https://docs.newrelic.com/docs/agents/python-agent/hosting-services/python-agent-heroku)
    
    聽說在heroku用sqlite3可能會出事，所以在production_settings.py改用heroku的postgresql的add-on。
    
    暫時找不到理想的圖片存取方案，就先全塞在media/product_image裡，全丟給heroku。
    

專案重點:

    1.串金流(ECPay):
    
        ecpay的sdk放在portfolio_cart/order/
        
        不過deploy時遇到module path的問題，用pathlib解決。
        
        
    2.我再想想


其它:

    1.我懶得多一個table來寫分類，所以用context_processor取distinct的分類。
    
    
    2.更新商品照片自動刪除的部分在把media files換到S3時就壞掉了，還在找方法當中。
    
    
    3.前台UI部分我從https://www.free-css.com/free-css-templates/page201/shopper 抓的。


警告:

    ※loaddata會觸發signal
        在連得上AWS S3的時候進行loaddata會觸發Image的post_save，導致所有圖片被delete。
        同樣的情況也會發生在Order，導致Product.stock被多扣。
        (已解決，官方有教，在signal的handler判斷kwargs['raw']是否為True)
