from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from database.sql_connector import db_connector, db_engine


metadata = MetaData()
base = declarative_base(metadata=metadata)


class SalesKBBIO(base):
    __tablename__ = 'busy_sales'

    id = Column(Integer, primary_key= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False)
    party_type = Column(String(255), nullable= False)
    dealer_code = Column(String(255), nullable= True)
    state = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    product_group = Column(String(255), nullable= False)
    product_print_name = Column(String(255), nullable= False)
    gst_no = Column(String(15), nullable= True)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    mfg_date =  Column(Date, nullable= True)
    exp_date =  Column(Date, nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Integer, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Integer, nullable= False) 
    alt_qty = Column(Integer, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Integer, nullable= False)
    amount = Column(Integer, nullable=False)      #Alt Qty * Alt Price
    mrp = Column(Integer, nullable=False)
    discount_perc = Column(Integer, nullable=True)
    discount_amt = Column(Integer, nullable=True)
    tax_amt = Column(Integer, nullable=False, default= 0)
    bill_amt = Column(Integer, nullable=False, default= 0)
    dc_no = Column(String(255), nullable= True)
    dc_date = Column(Date, nullable= True)
    e_invoice = Column(Integer, nullable= True)
    salesman = Column(String(255), nullable= True)
    sales_order_no = Column(String(255), nullable= True)
    sales_order_date = Column(Date, nullable= True)
    e_way_bill = Column(Integer, nullable= True)
    transporter_name = Column(String(255), nullable= True)
    narration = Column(String(255), nullable= True)



class SalesReturnKBBIO(base):
    __tablename__ = 'busy_sales_return'

    id = Column(Integer, primary_key= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False)
    party_type = Column(String(255), nullable= False)
    state = Column(String(255), nullable= False)
    dealer_code = Column(String(255), nullable= True)
    particulars = Column(String(255), nullable= False)
    product_group = Column(String(255), nullable= False)
    product_print_name = Column(String(255), nullable= False)
    gst_no = Column(String(15), nullable= True)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    mfg_date =  Column(Date, nullable= True)
    exp_date =  Column(Date, nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Integer, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Integer, nullable= False) 
    alt_qty = Column(Integer, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Integer, nullable= False)
    amount = Column(Integer, nullable=False)      #Alt Qty * Alt Price
    mrp = Column(Integer, nullable=False)
    discount_perc = Column(Integer, nullable=True)
    discount_amt = Column(Integer, nullable=True)
    tax_amt = Column(Integer, nullable=False, default= 0)
    bill_amt = Column(Integer, nullable=False, default= 0)
    grn_no = Column(String(255), nullable= True)
    grn_date = Column(Date, nullable= True)
    e_invoice = Column(Integer, nullable= True)
    salesman = Column(String(255), nullable= True)
    sales_order_no = Column(String(255), nullable= True)
    sales_order_date = Column(Date, nullable= True)
    e_way_bill = Column(Integer, nullable= True)
    narration = Column(String(255), nullable= True)



class SalesOrderKBBIO(base):
    __tablename__ = 'busy_sales_order'

    id = Column(Integer, primary_key= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Integer, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Integer, nullable= False) 
    alt_qty = Column(Integer, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Integer, nullable= False)
    amount = Column(Integer, nullable=False)      #Alt Qty * Alt Price
    # discount_perc = Column(Integer, nullable=True)
    # discount_amt = Column(Integer, nullable=True)
    tax_amt = Column(Integer, nullable=False, default= 0)
    bill_amt = Column(Integer, nullable=False, default= 0)
    salesman = Column(String(255), nullable= True)
    salesman_id = Column(String(255), nullable= True)
