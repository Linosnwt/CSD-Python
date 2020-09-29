 --KYC table
CREATE TABLE  KYC (
    Firstname VARCHAR2(25) NOT NULL ENABLE,
    Lastname VARCHAR2(25) NOT NULL ENABLE,
	LOCATION_ADDRESS VARCHAR2(15) NOT NULL ENABLE, 
	DIGITAL_ADDRESS VARCHAR2(25) NOT NULL ENABLE, 
	CONTACT_NUMBER VARCHAR2(13) NOT NULL ENABLE, 
	EMAIL VARCHAR2(30) NOT NULL ENABLE, 
	GENDER VARCHAR2(7) NOT NULL ENABLE, 
	AGE NUMBER(3,0), 
	MARITAL_STATUS VARCHAR2(6), 
	NAME_OF_SPOUSE VARCHAR2(25), 
	OCCUPATION VARCHAR2(15) NOT NULL ENABLE, 
	EMPLOYER VARCHAR2(25) NOT NULL ENABLE,
    AnnualSalary NUMBER NOT NULL ENABLE,
    CLIENT_ID VARCHAR2(10)Primary Key,
    Pass_word VARCHAR2(10)  NOT NULL,
    Re_type_Password VARCHAR2(10) NOT NULL
   ) ;

--Loan number sequence
CREATE SEQUENCE  Loan_seq 
MINVALUE 1 
MAXVALUE 9999999 
INCREMENT BY 1 
START WITH 1 NOCACHE  
ORDER  NOCYCLE ;

--Loan_Applications Table
CREATE TABLE  Loan_Applications(
    Loan_Num Number PRIMARY KEY,
    APPLYDATE DATE DEFAULT SYSDATE,
    CLIENT_ID VARCHAR2(15), 
    LOAN_TYPE VARCHAR2(20) DEFAULT 'Personal Loan', 
    GURANTOR_FULL_NAME VARCHAR2(30), 
    AMOUNT_REQUESTED NUMBER(10) NOT NULL ENABLE, 
    LOAN_TENOR NUMBER(2) NOT NULL ENABLE, 
    LOAN_STATUS VARCHAR2(10) DEFAULT 'Pending'
   ) ;

 --Insert into Loan_Applications(CLIENT_ID,GURANTOR_FULL_NAME,AMOUNT_REQUESTED,LOAN_TENOR) VALUES('MAX','Maxwell',2000,2)
--Trigger to insert Loan seq before inserting into loan Application


--CREATE OR REPLACE TRIGGER Loannapp_on_insert
--  BEFORE INSERT ON Loan_Applications
--  FOR EACH ROW
--BEGIN
--  SELECT Loan_seq.nextval
--  INTO :new.Loan_Num
--  FROM dual;
--END;

--GUARANTORS  Table
CREATE TABLE  GUARANTORS ( 
	FULL_NAME VARCHAR2(30) NOT NULL ENABLE, 
	EMAIL VARCHAR2(30) NOT NULL ENABLE, 
	PHONE NUMBER(10) NOT NULL ENABLE, 
	LOACTION_ADDRESS VARCHAR2(30) NOT NULL ENABLE, 
	RELATIONSHIP VARCHAR2(10), 
	BANK VARCHAR2(25), 
	ACCOUNT_NUMBER NUMBER(20), 
	ACCOUNT_NAME VARCHAR2(25), 
    BRANCH VARCHAR2(15)
   ) ; 

--RECEIVABLES table
CREATE TABLE  PROPOSED_RECEIVABLES(
    Loan_Num  Number,
    CLIENT_ID  VARCHAR2(10) NOT NULL ENABLE, 
	LOAN_TYPE VARCHAR2(20) DEFAULT 'Personal Loan', 
	AMOUNT_DISBURSED NUMBER(10,2) NOT NULL ENABLE, 
	INTEREST_RATE NUMBER(2,2) DEFAULT 0.1,
    Total_Amount_Paid number(10,2) default 0,
	DATE_DISBURSED TIMESTAMP, 
	REPAYMENT_DATE DATE DEFAULT SYSTIMESTAMP,
    LOAN_STATUS VARCHAR2(10)
   ) ;

--insert into Loan values('Linos',2000,1);
--insert into Loan values('Maxone1',2000,2);
--insert into Loan values('Maxone2',3000,2);
--insert into Loan values('Maxone3',4000,1);


--Receivable Triger
/*
create or replace TRIGGER Triger_Receivable
    AFTER INSERT ON Loan_Applications
    FOR EACH ROW
BEGIN
Insert INTO PROPOSED_RECEIVABLES(LOAN_NUM,CLIENT_ID,LOAN_TYPE,AMOUNT_DISBURSED,LOAN_STATUS ) 
Values(:new.Loan_Num,:new.CLIENT_id,:new.LOAN_TYPE,:new.AMOUNT_REQUESTED,:new.LOAN_STATUS );
END;
*/


--Log In  Validation   
Create or replace Procedure login (C_id varchar2,pword Varchar2) 
as VClientid VARCHAR(20);
Vpassword varchar(20);
BEGIN
Select client_id,pass_word Into VClientid,Vpassword 
from KYC where client_id=C_id and pass_word=pword;
DBMS_Output.put_line(VClientid||' '||Vpassword);
END;

EXECUTE login('Linos','Linos2020');

--Loan Repayment table
CREATE TABLE  loan_repayments(
    Loan_Num Number,
    CLIENT_ID VARCHAR2(10) NOT NULL ENABLE, 
	AMOUNT_PAID NUMBER(10,2) NOT NULL ENABLE, 
	DATE_PAID TIMESTAMP  DEFAULT SYSDATE
   ) ;

    --Packages
/*
Create or replace Package Repayment_amt as
    Function  
    Calculate_Interest_amount(Amt number,rate number,Dura Number)
    Return Number;
    FUNCTION 
    Calculate_Repayment_amount(Amt number, int_amt number)
Return Number;
END Repayment_amt;


CREATE OR REPLACE PACKAGE BODY Repayment_amt AS
    Function  
    Calculate_Interest_amount(Amt Number,rate number,Dura Number)
    Return Number
    IS
    interest_amt Number(10);
Begin 
    interest_amt:=Amt*rate*Dura;
    Return Interest_amt;
End Calculate_Interest_amount;
FUNCTION
    Calculate_Repayment_amount(Amt number, int_amt number)
    Return Number 
    is  
    repayment_amount Number(10);
Begin
    repayment_amount:=Amt+int_amt;
    Return repayment_amount;
END Calculate_Repayment_amount;
END Repayment_amt;
*/
--*****************************************************************************************************************************

--Computing Total Amount Paid by Client
create or replace TRIGGER  "UPDATE_receivables"
after insert or update or delete on loan_repayments

begin
update PROPOSED_RECEIVABLES set Total_Amount_paid =
  (select sum(Amount_paid) from loan_repayments
    where PROPOSED_RECEIVABLES.loan_num = loan_repayments.loan_num)
    where Loan_num = (select loan_num from ACTUAL_RECEIVABLE_DETAIL where loan_num  = PROPOSED_RECEIVABLES.loan_num);
                                            
end;


    --views for RECEIVABLE
Create or Replace view ACTUAL_RECEIVABLE_DETAIL AS
select rec.Loan_num,rec.client_id,Amount_disbursed AMOUNT,
(CASE app.LOAN_TYPE
    when 'Special loan' then (0.1*Loan_Tenor)-0.05
    ELSE interest_rate
    END)
Interest_rate,
Loan_Tenor,

--getting INTEREST_AMOUNT;
REPAYMENT_AMT.CALCULATE_INTEREST_AMOUNT(Amount_disbursed,Interest_rate,Loan_Tenor) AS INTEREST_AMOUNT,

--getting REPAYMENT_AMOUNT;
Repayment_Amt.Calculate_Repayment_Amount(Amount_disbursed,
    REPAYMENT_AMT.CALCULATE_INTEREST_AMOUNT(Amount_disbursed,Interest_rate,Loan_Tenor)) AS REPAYMENT_AMOUNT,

Total_Amount_paid,

--Getting BALANCE;
REPAYMENT_AMT.CALCULATE_REPAYMENT_AMOUNT(Amount_disbursed,
    REPAYMENT_AMT.CALCULATE_INTEREST_AMOUNT(Amount_disbursed,Interest_rate,Loan_Tenor))-TOTAL_AMOUNT_PAID AS BALANCE,

Date_disbursed,ADD_MONTHS(Date_disbursed,Loan_tenor) AS Repayment_date
--END_DATE
FROM PROPOSED_RECEIVABLES rec
join Loan_Applications app
on rec.Loan_num = app.Loan_num
where rec.LOAN_STATUS = 'Approved';

--Creat loan Schedule
create table loan_schedule(
    repayment_date date,
    Loan_num Number,
    client_id VARCHAR2(10),
    Monthly_repay NUMBER(10,2),
    Amount_paid NUMBER(10,2) Default 0,
    Date_paid DATE )


--Get equal installment Amount
/*
Create or replace Procedure Calculate_installments(ln_num in number,clt_id in varchar2,dura in number)
is
    repay_date date; 
    ln_number Number;
    username VARCHAR2(10);
    Installment_Amount Number;
BEGIN
--vAmount :=2000/4;
    SELECT date_disbursed,Loan_num,Client_id,(Repayment_amount/dura)
    INTO repay_date,ln_number,username,Installment_Amount
    FROM ACTUAL_RECEIVABLE_DETAIL
    WHERE Loan_num = ln_num and client_id=clt_id;
FOR i IN 1..3 LOOP
        INSERT INTO loan_schedule(repayment_date,loan_num,client_id,Monthly_repay)
        VALUES(add_months(repay_date,i),ln_number,username,Installment_Amount);
END LOOP;
END;
*/


EXECUTE Calculate_installments(22,'Maxone',2)

select * from loan_schedule 
where client_id ='Maxone'

--DELETE FROM loan_schedule ;
SELECT REPAYMENT_DATE,TO_CHAR(REPAYMENT_DATE,'Mon fmDD,YYYY'),MONTHLY_REPAY,AMOUNT_PAID,NVL(TO_CHAR(DATE_PAID, 'fmDD Month YYYY'),'-') DATE_PAID
from loan_schedule where CLIENT_ID = 'Maxone'
order BY REPAYMENT_DATE asc
--****************************************************************************************************************************

CREATE TABLE  JOBS 
   (JOB_ID VARCHAR2(10) PRIMARY KEY, 
	JOB_TITLE VARCHAR2(25) NOT NULL
   ); 

--drop table JOBS;
Insert into JOBS values('FIN_ACC','Financial Accountant');
Insert into JOBS values('LN_OFF','Loan Officer');
Insert into JOBS values('MGR','Manager');
Insert into JOBS values('CUST_CARE','Customer Care');

--******************************************************************************************************************************
CREATE TABLE  B_EMPLOYEES(
   EMPLOYEE_ID VARCHAR2(10) UNIQUE, 
	FIRST_NAME VARCHAR2(13) NOT NULL ENABLE, 
	LAST_NAME VARCHAR2(13) NOT NULL ENABLE, 
	SALARY NUMBER(6,0), 
	COMMISSION NUMBER(3,0), 
	JOB_ID VARCHAR2(10) NOT NULL ENABLE, 
	LOG_IN_PASSWORD VARCHAR2(8) NOT NULL ENABLE
   ) ;

--Procedure to insert into employees table
Create or replace Procedure create_employee(empid in varchar2,sal in number,comm in varchar2,jobid in varchar2)
is
    varCLIENT_ID VARCHAR2(10); 
    varFIRSTNAME VARCHAR2(25);
    varLASTNAME VARCHAR2(25);
    varPASS_WORD VARCHAR2(10);
BEGIN
    SELECT FIRSTNAME,LASTNAME,PASS_WORD
    INTO varFIRSTNAME,varLASTNAME,varPASS_WORD
    FROM KYC
    WHERE client_id=empid;

    INSERT INTO B_EMPLOYEES(EMPLOYEE_ID,FIRST_NAME,LAST_NAME,SALARY,COMMISSION,JOB_ID,LOG_IN_PASSWORD)
    VALUES(empid,varFIRSTNAME,varLASTNAME,sal,comm,jobid,varPASS_WORD);

END;

EXECUTE create_employee('Linos',2000.00,20.00,'FIN_ACC');
EXECUTE create_employee('Godsway',2000.00,20.00,'LN_OFF');
EXECUTE create_employee('Sylvie',2000.00,20.00,'MGR');
EXECUTE create_employee('Linos',2000.00,20.00,'CUST_CARE');



create or replace view Employees_details as
Select Employee_id,FIRST_NAME||' '||LAST_NAME as Full_Name,SALARY,COMMISSION,LOCATION_ADDRESS,
DIGITAL_ADDRESS,CONTACT_NUMBER,EMAIL,GENDER,JOB_TITLE,LOG_IN_PASSWORD
from B_Employees emp
join KYC
on emp.Employee_id = kyc.CLIENT_ID
join JOBS jb
on jb.job_id=emp.job_id;

--WORKKERS LOGIN PROCEDURE
Create or replace Procedure admlogin(empid varchar2,pword Varchar2,title in VARCHAR2) 
as Vempid VARCHAR(20);
Vpassword varchar(20);
Vtitle varchar(20);
BEGIN
Select EMPLOYEE_ID,LOG_IN_PASSWORD,JOB_TITLE Into Vempid,Vpassword,Vtitle
from Employees_details where EMPLOYEE_ID=empid and LOG_IN_PASSWORD=pword and JOB_TITLE=title;
DBMS_Output.put_line(Vempid||' '||Vpassword);
END; 


--INSERT INTO employees_details SELECT 'Linos', 'Linos Nouwoto', 5000,1.5, 'Sunyani', 'P500','0556623388','lnouwoto@gmail.com','mmale', 'Manager', 'Linos2020';

--Execute admlogin('LinosOne','LinosOne2020','Financial Accountant');

--TRANSACTION NAMES
CREATE table TRANSACTIONS (
    TXN_ID     VARCHAR2(6) primary keY,
    TXN_NAME  VARCHAR2(15) NOT NULL
);

INSERT into transactions values('EXP_MC','MoMo Charges');
--*******************************************************************************************************************************

CREATE SEQUENCE  LF_seq 
MINVALUE 1 
MAXVALUE 9999999 
INCREMENT BY 1 
START WITH 1 
NOCACHE  
ORDER  NOCYCLE ;

      
    --CASHBOOK
CREATE table CASHBOOK (
     LF  NUMBER(4,0) primary key,
     Txn_Id Varchar2(6) ,
    Txn_DATE TIMESTAMP NOT NULL,     
    DETAILS  VARCHAR2(30) NOT NULL,
    CREDIT   NUMBER(7,2),
    DEBIT    NUMBER(7,2),
    Balance   NUMBER(7,2)
);


--Get LAst_value from cashbook

/*
Create or replace Function Get_cbLast_bal
Return Number as
LAST_Bal cashbook.balance%type;
V_LAST_BAl cashbook.balance%type;
Begin
Select NVL(Balance,0) Into V_LAST_Bal
from cashbook
WHERE LF=(SELECT MAX(LF) FROM cashbook);
LAST_Bal:=V_LAST_Bal;
return LAST_Bal;
End;
*/


create or replace procedure INSERT_CashBook    
    (Txn_id varchar2,Txn_date TIMESTAMP,details varchar2,Credit number, Debit Number)  
is  
begin    
insert into CashBook
values(LF_SEQ.NEXTVAL,Txn_id,Txn_date,details,credit,Debit,(NVL(Get_cbLast_bal,0)+(credit)-(debit)));    
end;

EXECUTE INSERT_CashBook('EXP_MC',sysdate,'Interest on Loan',0,50);
EXECUTE INSERT_CashBook('EXP_MC',sysdate,'Interest on Loan',50,0);
*/

create or replace view CashBookview as
    select * from cashbook order by 1;
 

Create or replace FUNCTION Managerial_role
return Varchar2
    AS
--DECLARE
--    v_empid B_employees.employee_id%TYPE;
    v_job_title Employees_details.job_title%TYPE;
CURSOR Management_cursor IS
    SELECT job_title FROM Employees_details
    WHERE job_title ='Manager' or job_title ='Financial Accountant';
BEGIN
OPEN  Management_cursor;
    LOOP
        FETCH Management_cursor INTO  v_job_title;
        EXIT WHEN Management_cursor%NOTFOUND;
--        DBMS_OUTPUT.PUT_LINE(v_empid||' '||v_job_title);
         DBMS_OUTPUT.PUT_LINE(v_job_title);
         return v_job_title;
    END LOOP;
    CLOSE Management_cursor;
END;  


--Statistics display
Create or replace Procedure count_customers(No_of_Customers out number)
as 
BEGIN
Select COUNT(*) Into No_of_Customers
from KYC;
dbms_output.put_line(No_of_Customers);
END; 

Execute count_customers(0);
--select * from loan_repayments;

Create or replace Procedure Total_repayments(repays out number)
as 
BEGIN
Select SUM(AMOUNT_PAID) Into repays
from loan_repayments;
dbms_output.put_line(repays);
END; 

Create or replace Procedure Total_receivables(owings out number)
as 
BEGIN
Select SUM(BALANCE) Into owings
from ACTUAL_RECEIVABLE_DETAIL;
dbms_output.put_line(owings);
END; 

--select * from ACTUAL_RECEIVABLE_DETAIL;

Create or replace Procedure totalloans(loans out number)
as 
BEGIN
Select SUM(Repayment_amount) Into loans
from ACTUAL_RECEIVABLE_DETAIL;
dbms_output.put_line(loans);
END; 

