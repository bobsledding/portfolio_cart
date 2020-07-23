# portfolio_cart
購物車網站試做


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
