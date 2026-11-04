#说明：有两套代码，实现的功能是一样的，第一套代码简单，第二套代码复杂

#第一套代码：比CDA一级图书中的代码简单
###################################################################################################
#1、获取客户的性别和发卡时的年龄,注意年龄作为时点数据，根据取数窗口的设定，一定要取发卡时的年龄。S
#     以下语句中的“datediff(a.issued,c.birth_date)/365”就是计算“发卡时的年龄”
select a.*,c.sex,datediff(a.issued,c.birth_date)/365 as age from 
  kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_clients c on b.client_id=c.client_id;
  
###################################################################################################
#2、截止到开卡时的最后一次交易间隔和账户余额。这也是根据取数窗口设定的要求。
#分为两步：
#      第一步获取发卡前的交易流水数据，并且计算该笔交易距离发卡时点的天数，以下语句中的“a.issued>c.date”的意思是只保留发卡前的交易；

create table kdd99.rfm_balance1 as 
select a.*,c.date as trans_date,datediff(a.issued,c.date) as last_days,c.balance 
  from kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_Trans c on b.account_id=c.account_id and a.issued>c.date
  order by a.card_id,c.date;

#      第二步从上一步得到的表中，获取交易时间最大的那条记录。
    #注意，以下代码得到的数据会出现重复，原因是有些账户最后一天有多笔交易，因此数据量是1175，而不是892。不过本数据交易时间只能精确到日，也只能这样了。
select * from kdd99.rfm_balance1 a
  inner join (select card_id,max(trans_date) as max_date
                     from kdd99.rfm_balance1 group by  card_id) b on a.card_id=b.card_id and a.trans_date=b.max_date;

###################################################################################################
#3、客户开卡半年内现金交易笔数、半年内总入账、半年内总出账、半年内出账/平均资产额、半年内出/入账比例
#   以下语句中的“a.issued>c.date and c.date>a.issued-180”表示获取发卡前180天以内的交易数据，这也是根据取数窗口设定的要求。
select a.card_id,a.disp_id,a.type,count(trans_id) as trans_count,
       sum(if(c.type='借',amount,0)) as trans_in_count,
       sum(if(c.type='贷',amount,0)) as trans_out_count,
       sum(if(c.type='贷',amount,0))/avg(c.balance) as out_ratio,
       sum(if(c.type='贷',amount,0))/sum(if(c.type='借',amount,0)) as out_in_ratio
  from kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_Trans c on b.account_id=c.account_id and a.issued>c.date and c.date>a.issued-180
  group by a.card_id,a.disp_id,a.type;




#第二套代码：以下代码是CDA一级图书配套代码，难度较高
##########################################################################################################
#1、获取客户的性别和发卡时的年龄
create table kdd99.var1 as
select a.*,c.sex,datediff(a.issued,c.birth_date)/365 as age from 
  kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_clients c on b.client_id=c.client_id;
  
  
  #2、截止到开卡时的最后一次交易间隔和账户余额
#以下时是分步操作
#第一步:获取信用卡发卡前对应账户交易流水的数据
create table kdd99.var2_1 as 
select a.*,c.date as trans_date,datediff(a.issued,c.date) as last_days,c.balance 
  from kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_Trans c on b.account_id=c.account_id and a.issued>c.date
  order by a.card_id,c.date;
#第二步:仅保留对应账户交易流水的开信用卡前最后一笔交易数据 
create table kdd99.var2 as 
select a.card_id,a.disp_id,a.issued,a.type,a.trans_date,a.last_days,avg(a.balance) as balance from kdd99.var2_1 a
  inner join (select card_id,max(trans_date) as max_date
                     from kdd99.var2_1 group by  card_id) b 
		on a.card_id=b.card_id and a.trans_date=b.max_date
        group by a.card_id,a.disp_id,a.issued,a.type,a.trans_date,a.last_days;
        
#3、全年内现金交易笔数、全年内总入账、全年内总出账、全年内出/入账比例
create table kdd99.var3 as 
select a.card_id,a.disp_id,count(trans_id) as trans_count,
       sum(if(c.type='借',amount,0)) as trans_in_amount,
       sum(if(c.type='贷',amount,0)) as trans_out_amount,
       sum(if(c.type='贷',amount,0))/avg(c.balance) as out_ratio,
       sum(if(c.type='贷',amount,0))/sum(if(c.type='借',amount,0)) as out_in_ratio
  from kdd99.kdd99_card a
  left join kdd99.kdd99_disp b on a.disp_id=b.disp_id
  left join kdd99.kdd99_Trans c on b.account_id=c.account_id and datediff(a.issued,c.date)>0 and datediff(a.issued,c.date)<365
  group by a.card_id,a.disp_id;
  
  #4、最后关联var1、var2和var3表，得到我们制作信用卡用户画像所需要所有数据
  create table kdd99.Creditcard as 
  select a.*,b.last_days,b.balance,c.trans_count,c.trans_in_amount,
c.trans_out_amount,c.out_ratio,c.out_in_ratio
    from kdd99.var1 as a 
    left join kdd99.var2 as b on a.card_id=b.card_id
    left join kdd99.var3 as c on a.card_id=c.card_id
order by a.card_id;
