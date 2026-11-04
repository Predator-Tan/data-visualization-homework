/*********************************************************************************************/
/*SQL1数据查询与SQL语言简介*/

/*********************************************************************************************/
/*SQL2数据过滤与排序*/
/*选择表中指定列*/
   select year,market,sale,profit
      from kdd99.sale;
/*选择表中所有列*/
 select *
      from kdd99.sale;
/*删除重复的行*/
   select DISTINCT  year
      from kdd99.sale;
/*选择满足条件的行*/
   select *
      from kdd99.sale
      where year=2012;
/*对行进行排序*/
   select year,market,sale,profit
      from kdd99.sale
      order by year;
/*      order by 2;*/
/*单表查询案例1*/
SELECT t1.account_id, 
          t1.date, 
          t1.bank, 
          t1.amount
      FROM KDD99.KDD99_TRANS t1
      WHERE t1.date BETWEEN '1998-12-01'
            AND '1998-12-31'
            AND t1.k_symbol = '房屋贷款'
      ORDER BY t1.date,
               t1.account_id;

/*********************************************************************************************/
/*SQl3用表达式创建新列*/
/*创建新列*/
 select profit/sale as rate
      from kdd99.sale;

/*用计算得到的值筛选*/
select profit/sale as rate
      from kdd99.sale
      where profit/sale <0.07;

/*创建新列案例*/
SELECT t1.account_id, 
          t1.date, 
          t1.bank, 
          t1.amount,
          weekday(t1.date) as  weekday
      FROM KDD99.KDD99_TRANS t1
      WHERE t1.date BETWEEN '1998-12-01'
            AND '1998-12-31' 
            AND t1.k_symbol = '房屋贷款'
      ORDER BY t1.date,
               t1.account_id;

/*********************************************************************************************/
/*SQL4对列重编码*/
/*重新编码列*/
SELECT t1.account_id, 
          t1.date, 
          t1.bank, 
          t1.amount,
          weekday(t1.date) as  weekday,
          (CASE 
               WHEN 5 = weekday(t1.date) THEN '周末'
               WHEN 6 = weekday(t1.date) THEN '周末'
               WHEN weekday(t1.date) >= 0 AND weekday(t1.date) <= 4 THEN '工作日'
		 end) AS Weekday_2
      FROM KDD99.KDD99_TRANS t1
      WHERE t1.date BETWEEN '1998-12-01'
            AND '1998-12-31'  
            AND t1.k_symbol = '房屋贷款'
      ORDER BY t1.date,
               t1.account_id;

SELECT t1.account_id, 
          t1.date, 
          t1.bank, 
          t1.amount,
          weekday(t1.date) as  weekday,
          (CASE weekday(t1.date) 
               WHEN 5 THEN '周末'
               WHEN 6 THEN '周末'
               WHEN 0 THEN '工作日'
               WHEN 1 THEN '工作日'
               WHEN 2 THEN '工作日'
               WHEN 3 THEN '工作日'
               WHEN 4 THEN '工作日'
            END) AS Weekday_2
      FROM KDD99.KDD99_TRANS t1
      WHERE t1.date BETWEEN '1998-12-01'
            AND '1998-12-31'
            AND t1.k_symbol = '房屋贷款'
      ORDER BY t1.date,
               t1.account_id;


SELECT t1.account_id, 
          t1.date, 
          t1.bank, 
          t1.amount,
          weekday(t1.date) as  weekday,
          (CASE weekday(t1.date)
               WHEN 5 THEN '周末'
               WHEN 6 THEN '周末'
               ELSE '工作日'
            END) AS Weekday_2
      FROM KDD99.KDD99_TRANS t1
      WHERE t1.date BETWEEN '1998-12-01'
            AND '1998-12-31'
            AND t1.k_symbol = '房屋贷款'
      ORDER BY t1.date,
               t1.account_id;


/*********************************************************************************************/
/*SQL5在查询中对数据分组和汇总*/

 SELECT t1.date, 
          /* COUNT_of_account_id */
       (COUNT(t1.account_id))   AS COUNT_of_account_id, 
          /* MEAN_of_amount */
       (avg(t1.amount)) AS MEAN_of_amount, 
          /* SUM_of_amount */
       (SUM(t1.amount))  AS SUM_of_amount
      FROM KDD99.KDD99_TRANS t1
      GROUP BY t1.date
      HAVING COUNT_of_account_id > 300;


/*********************************************************************************************/
/*SQL6 横向连接表*/
/*笛卡尔积*/

select *  from kdd99.table1, kdd99.table2;

/*内连接*/

select *  from kdd99.table1, kdd99.table2
   Where table1.id= table2.id;

/*左连接*/

select * 
   from kdd99.Table1 
     left join kdd99.Table2
      on Table1.id = Table2.id;

/*右连接*/

select * 
   from kdd99.Table1 
     right join kdd99.Table2
      on Table1.id = Table2.id;

/*全连接
MYSQL没有实现该功能，运行程序会报错*/

select * 
   from kdd99.Table1 
     full join kdd99.Table2
      on Table1.id = Table2.id;

/*商业问题的实现语句*/

    SELECT t1.card_id, 
          t1.disp_id, 
          t1.issued, 
          t1.type, 
          t3.sex, 
          t3.birth_date, 
          t3.district_id
      FROM KDD99.KDD99_CARD t1
           LEFT JOIN KDD99.KDD99_DISP t2 ON (t1.disp_id = t2.disp_id)
           LEFT JOIN KDD99.KDD99_CLIENTS t3 ON (t2.client_id = t3.client_id);

/*********************************************************************************************/
/*非等值横向连接*/

     SELECT t1.loan_id, t1.account_id, t1.date,t1.amount, t1.duration, 
          t1.payments, t1.status, t2.trans_id, t2.date AS date1, 
          t2.type, t2.operation,t2.amount AS amount1, t2.balance, 
          t2.k_symbol, t2.bank, t2.account
      FROM KDD99.KDD99_LOANS t1
           LEFT JOIN KDD99.KDD99_TRANS t2 ON 
           (t1.account_id = t2.account_id AND (t1.date>t2.date AND 
          t1.date<=t2.date+365))
      ORDER BY t1.loan_id,
               t1.account_id,
               t1.date,
               t2.date;

/*********************************************************************************************/
/*SQL7 子查询*/
/*获取贷款违约客户的所有交易数据*/
create table all_loan as
select * from 
  kdd99.kdd99_trans 
  where account_id in
       (select account_id from kdd99.kdd99_loans where status="B" )
	order by account_id;

/*获取贷款违约客户的贷款之前的交易数据*/

create table before_loan as
select * from 
  kdd99.kdd99_trans as b
  where account_id in
       (select account_id from kdd99.kdd99_loans as a where status="B" and b.date< a.date)
	order by account_id;
/*********************************************************************************************/
/*SQL8  集合操作*/
/*http://www.jellythink.com/archives/940*/
/*通常来说，将联接操作看作是表之间的水平操作，因为该操作生成的虚拟表包含两个表中的列。而我这里总结的集合操作，
一般将这些操作看作是垂直操作。MySQL数据库支持两种集合操作：UNION DISTINCT和UNION ALL。
集合操作的两个输入必须拥有相同的列数，若数据类型不同，MySQL数据库自动将进行隐式转换。同时，结果列的名称由左输入决定。*/
/*UNION运算符*/
/*UNION DISTINCT组合两个输入，并应用DISTINCT过滤重复项，一般可以直接省略DISTINCT关键字，直接使用UNION。*/
select *
   from kdd99.one 
UNION 
select *
   from kdd99.two;
/*带有ALL的UNION运算符*/
select *
   from kdd99.one 
UNION all
select *
   from kdd99.two;

/*MY不支持INTERSECT和EXCEPT操作，参考该网站http://www.tuicool.com/articles/Abe2ui*/


/*SQL9  生成表和视图*/
/*创建表*/
create table test1 as
select * from kdd99.sale 
  where year in (2010,2011);
/*创建视图*/
create view aa as 
select * from kdd99.sale;
/*描述视图*/
