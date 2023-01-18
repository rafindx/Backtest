def DeteToStr(date):
    return date.strftime("%Y-%m-%d")

def Query_Price(IDentifier,isinlist,sd,ed):
    Query=""
    LIST = str(isinlist)[1:-1]
    S_DATE = DeteToStr(sd)
    E_DATE = DeteToStr(ed)
    if IDentifier=='ISIN':
        Query= "select  b.isin,a.p_date as date,a.p_price,a.currency from fp_v2.fp_basic_prices a with (nolock) inner join sym_v1.sym_coverage c with (nolock) on a.fsym_id=c.fsym_regional_id inner join sym_v1.sym_isin b with (nolock) on c.fsym_id=b.fsym_id WHERE b.isin in ("+LIST +") AND  a.p_date between '"+S_DATE+"' and '"+E_DATE+"' "
    else:
        Query= "select a.fsym_id,a.p_date as date,a.p_price,a.currency from fp_v2.fp_basic_prices a with (nolock) WHERE a.fsym_id in  ("+LIST +")  AND  a.p_date between '"+S_DATE+"' and '"+E_DATE+"'  ORDER BY a.fsym_id, a.p_date asc"
    #print(Query)
    return Query

def Query_Divident(IDentifier,isinlist,sd,ed):
    Query=""
    LIST = str(isinlist)[1:-1]
    S_DATE = DeteToStr(sd)
    E_DATE = DeteToStr(ed)
    if IDentifier=='ISIN':
        Query= "SELECT ISN.isin ,DIV.p_divs_pd,DIV.p_divs_s_spinoff,DIV.currency,DIV.p_divs_pd_type_code,DIV.p_divs_exdate as date FROM FDS_DataFeeds.fp_v2.fp_basic_dividends AS DIV  with (nolock) inner join [sym_v1].[sym_coverage] c with (nolock)  on DIV.fsym_id = c.fsym_regional_id inner join [sym_v1].[sym_isin]   ISN with (nolock)  on c.fsym_id=ISN.fsym_id WHERE ISN.isin in ("+LIST +") AND DIV.p_divs_s_spinoff !='1' and  DIV.p_divs_exdate between '"+S_DATE+"' and '"+E_DATE+"'  ORDER BY ISN.isin, DIV.p_divs_exdate"
    else:
        Query= "SELECT div.fsym_id,DIV.p_divs_pd,DIV.p_divs_s_spinoff,DIV.currency,DIV.p_divs_pd_type_code,DIV.p_divs_exdate as date FROM FDS_DataFeeds.fp_v2.fp_basic_dividends AS DIV with (nolock) WHERE DIV.fsym_id in ("+LIST +") AND DIV.p_divs_s_spinoff!='1' and DIV.p_divs_exdate between '"+S_DATE+"' and '"+E_DATE+"'  ORDER BY DIV.fsym_id, DIV.p_divs_exdate"
    #print(Query)
    return Query

def Query_Spin(IDentifier,isinlist,sd,ed):
    Query=""
    LIST = str(isinlist)[1:-1]
    S_DATE = DeteToStr(sd)
    E_DATE = DeteToStr(ed)
    if IDentifier=='ISIN':
        Query= "SELECT ISN.isin ,DIV.p_divs_pd,DIV.p_divs_s_spinoff,DIV.currency,DIV.p_divs_pd_type_code,DIV.p_divs_exdate as date FROM FDS_DataFeeds.fp_v2.fp_basic_dividends AS DIV with (nolock) inner join [sym_v1].[sym_coverage] c with (nolock) on DIV.fsym_id = c.fsym_regional_id inner join [sym_v1].[sym_isin] ISN with (nolock) on c.fsym_id=ISN.fsym_id WHERE ISN.isin in ("+LIST +") AND  DIV.p_divs_s_spinoff='1' and DIV.p_divs_exdate between '"+S_DATE+"' and '"+E_DATE+"' ORDER BY ISN.isin, DIV.p_divs_exdate"
    else:
        Query= "SELECT div.fsym_id,DIV.p_divs_pd,DIV.p_divs_s_spinoff,DIV.currency,DIV.p_divs_pd_type_code,DIV.p_divs_exdate as date FROM FDS_DataFeeds.fp_v2.fp_basic_dividends AS DIV  with (nolock) WHERE DIV.fsym_id in ("+LIST +") AND  DIV.p_divs_s_spinoff='1' and DIV.p_divs_exdate between '"+S_DATE+"' and '"+E_DATE+"'  ORDER BY DIV.fsym_id, DIV.p_divs_exdate"
    #print(Query)
    return Query

def Query_Split(IDentifier,isinlist,sd,ed):
    Query=""
    LIST = str(isinlist)[1:-1]
    S_DATE = DeteToStr(sd)
    E_DATE = DeteToStr(ed)
    if IDentifier=='ISIN':
        Query= "SELECT b.isin,a.p_split_date,p_split_factor FROM [fp_v2].[fp_basic_splits] a with (nolock) inner join [sym_v1].[sym_coverage] c with (nolock) on a.fsym_id=c.fsym_regional_id inner join [sym_v1].[sym_isin] b  with (nolock) on c.fsym_id=b.fsym_id WHERE b.isin in ("+LIST +") AND  a.p_split_date between '"+S_DATE+"' and '"+E_DATE+"' ORDER BY b.isin, a.p_split_date"
    else:
        Query= "SELECT a.* FROM [fp_v2].[fp_basic_splits] a  with (nolock) WHERE a.fsym_id in ("+LIST +") AND  a.p_split_date between '"+S_DATE+"' and '"+E_DATE+"' ORDER by a.fsym_id, a.p_split_date "
    #print(Query)
    return Query

def Query_TR_Price(riclist,date):
    LIST = str(riclist)[1:-1]
    Date = DeteToStr(date)    
    #with cte  AS ( select distinct File_code,columnname, colvalue,Quote_ID,RIC,Trade_date from (select * from EQU_Price ) src unpivot (colvalue for columnname in ( offi_close_price,last_trade_price,p_close_price,bid_price,ask_price,alt_close_price,open_price,high_price,low_price,mid_price)) AS pvt WHERE Quote_ID IN( SELECT quote_id FROM TR_Equity WHERE ric in ('600085.SS','600556.SS','4113.TWO') AND valid_flag=1) AND Trade_Date ='2021-01-06' and Valid_flag=1) select c.Quote_ID,c.RIC,c.Trade_Date,c.colvalue AS price from tabl t join cte c on t.Code=c.File_code AND t.Column_ref=c.columnname    
    Query="with cte  AS ( select distinct File_code,columnname, colvalue,Quote_ID,RIC,Trade_date from (select * from EQU_Price with (nolock)) src unpivot (colvalue for columnname in ( offi_close_price,last_trade_price,p_close_price,bid_price,ask_price,alt_close_price,open_price,high_price,low_price,mid_price)) AS pvt WHERE Quote_ID IN("+LIST +") AND Trade_Date ='"+Date+"' and Valid_flag=1) select c.Quote_ID,c.RIC,c.Trade_Date,c.colvalue AS price from tabl t  join cte c on t.Code=c.File_code AND t.Column_ref=c.columnname"
    #print(Query)
    return Query;

def Query_TR_Equity(riclist):
    LIST = str(riclist)[1:-1]
    Query ="SELECT ric,quote_id FROM TR_Equity  with (nolock) WHERE ric in ("+LIST +") AND valid_flag=1"
    #print(Query)
    return Query;

def Query_UpdatedISIN():
    Query = "SELECT I2.ISIN AS OLD_ISIN,I1.ISIN AS  NEW_ISIN FROM SYM_V1.SYM_ISIN I1 LEFT JOIN SYM_V1.SYM_ISIN_HIST I2 ON I1.FSYM_ID = I2.FSYM_ID WHERE I2.ISIN IN ("+LIST +")"
    return Query
