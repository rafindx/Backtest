UI Input Field:-
		Portfolio Name*:XYZ
		Index Currency:USD
		Identifier:FSYM_ID
		Spin-Off ADJ:MARKETCAP ADJUSTMENT
		Index Value:1000
		Market Value:100000
		Portfolio* : file of xlsx
		Tax Rate FileNo file of xlsx
		Download Constituents File : Complete Download

Portfolio file  Inout:
		Period
		ISIN
		Weights
		Start date	
		End date	
		Country	
		RIC

for calculation perpose we are using 

SERVER=65.0.33.214;
DATABASE=FDS_Datafeeds;
UID=sa;PWD=Indxx@1234

SERVER=3.7.99.191;
DATABASE=TR_Datafeeds;
UID=sa;
PWD=Indxx@1234

Django database saving port folio
 'NAME': 'Backtest',
        'USER': 'sa',
        'PASSWORD': 'Indxx@1234',
        'HOST': '15.207.231.163',


we are calculating below things:
		Get_PRICE
		Get_Currency
		Get_CA
		Delisting_Check
		Check_Ric
		Get_TAX
		Set_TR_Price
		Get_TR_PRICE

OutPut back test:
       Index Value file:
		 	SNo	
		 	Date
		 	Index Value PR 
		 	Index Value TR
		 	Index Value NTR
		 	
	Constitue file:
			S.No	
			Date
			Index Value PR	
			Market CAP PR	
			Divisor PR	
			Index Value TR	
			Market CAP TR	
			Divisor TR	
			Index Value NTR	
			Market CAP NTR	
			Divisor NTR	
			ISIN	
			Currency	
			Country	
			TAX	
			Share PR	
			Share TR	
			Share NTR	
			Local Price	
			Index PRICE	
			MCAP PR	
			MCAP TR	
			MCAP NTR	
			Currency Price	
			Price Date	
			Weight PR	
			Weight TR	
			Weight NTR	
			Dividend	
			Special Dividend
			Split
			Spin

    

Backtest Server credential details.

Server IP: 15.206.224.193
Password: QBkkz9$M$DEV+x9pYgf*mnq-    



    