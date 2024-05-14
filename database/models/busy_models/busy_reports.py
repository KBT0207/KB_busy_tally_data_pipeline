from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func
from database.models.base import Base


metadata = MetaData()


class SalesKBBIO(Base):
    __tablename__ = 'busy_sales'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    party_type = Column(String(255), nullable= False)
    dealer_code = Column(String(255), nullable= True)
    state = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    product_group = Column(String(255), nullable= False)
    product_print_name = Column(String(255), nullable= False)
    gst_no = Column(String(15), nullable= True)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    mfg_date =  Column(String(10), nullable= True)
    exp_date =  Column(String(10), nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Float, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Float, nullable= False) 
    alt_qty = Column(Float, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    mrp = Column(Float, nullable=False)
    discount_perc = Column(Float, nullable=True)
    discount_amt = Column(Float, nullable=True)
    tax_amt = Column(Float, nullable=False, default= 0)
    bill_amt = Column(Float, nullable=False, default= 0)
    dc_no = Column(String(255), nullable= True)
    dc_date = Column(Date, nullable= True)
    e_invoice = Column(BigInteger, nullable= True)
    salesman = Column(String(255), nullable= True)
    sales_order_no = Column(String(255), nullable= True)
    sales_order_date = Column(String(255), nullable= True)
    e_way_bill = Column(BigInteger, nullable= True)
    transporter_name = Column(String(255), nullable= True)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())


class SalesReturnKBBIO(Base):
    __tablename__ = 'busy_sales_return'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
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
    mfg_date =  Column(String(10), nullable= True)
    exp_date =  Column(String(10), nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Float, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Float, nullable= False) 
    alt_qty = Column(Float, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    mrp = Column(Float, nullable=False)
    discount_perc = Column(Float, nullable=True)
    discount_amt = Column(Float, nullable=True)
    tax_amt = Column(Float, nullable=False, default= 0)
    bill_amt = Column(Float, nullable=False, default= 0)
    grn_no = Column(String(255), nullable= True)
    grn_date = Column(Date, nullable= True)
    e_invoice = Column(BigInteger, nullable= True)
    salesman = Column(String(255), nullable= True)
    sales_order_no = Column(String(255), nullable= True)
    sales_order_date = Column(String(255), nullable= True)
    e_way_bill = Column(BigInteger, nullable= True)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())



class SalesOrderKBBIO(Base):
    __tablename__ = 'busy_sales_order'

    id = Column(Integer, primary_key= True, index= True, autoincrement= True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index= True)
    particulars = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Float, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Float, nullable= False) 
    alt_qty = Column(Float, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    tax_amt = Column(Float, nullable=False, default= 0)
    order_amt = Column(Float, nullable=False, default= 0)
    salesman = Column(String(255), nullable= True)
    salesman_id = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())



class MITPKBBIO(Base):
    __tablename__ = 'busy_mitp'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False)
    party_type = Column(String(255), nullable= False)
    particulars = Column(String(255), nullable= False)
    product_group = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= True)
    mfg_date =  Column(String(10), nullable= True)
    exp_date =  Column(String(10), nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Float, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Float, nullable= False) 
    alt_qty = Column(Float, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    tax_rate = Column(Float, nullable=False)
    cgst_amt = Column(Float, nullable=True, default=0)
    sgst_amt = Column(Float, nullable=False, default=0)
    igst_amt = Column(Float, nullable=False, default= 0)
    narration = Column(String(255), nullable= True)
    sales_order_no = Column(String(255), nullable= True)
    salesman = Column(String(255), nullable= True)
    territory = Column(String(255), nullable= True)
    transporter = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())



class MRFPKBBIO(Base):
    __tablename__ = 'busy_mrfp'

    id = Column(Integer, primary_key= True, index= True, autoincrement=True)
    date = Column(Date, nullable= False)
    voucher_no = Column(String(255), nullable= False, index=True)
    particulars = Column(String(255), nullable= False)
    item_details = Column(String(255), nullable= False)
    batch_no = Column(String(255), nullable= True)
    batch_qty = Column(Float, nullable= True)
    mfg_date =  Column(String(10), nullable= True)
    exp_date =  Column(String(10), nullable= True)
    material_centre = Column(String(255), nullable= False)
    main_qty = Column(Float, nullable= False)
    main_unit = Column(String(255), nullable= False)
    main_price = Column(Float, nullable= False) 
    alt_qty = Column(Float, nullable= False)
    alt_unit = Column(String(255), nullable= False)
    alt_price = Column(Float, nullable= False)
    amount = Column(Float, nullable=False)      #Alt Qty * Alt Price
    tax_rate = Column(Float, nullable=False)
    cgst_amt = Column(Float, nullable=True, default=0)
    sgst_amt = Column(Float, nullable=False, default=0)
    igst_amt = Column(Float, nullable=False, default= 0)
    narration = Column(String(255), nullable= True)
    created_at = Column(DateTime, server_default=func.now())
