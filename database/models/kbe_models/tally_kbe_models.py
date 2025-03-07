from sqlalchemy import MetaData, Column, Integer, String, Date, BigInteger, Float, DateTime, func, DECIMAL
from database.models.base import KBEBase


metadata = MetaData()

class TallySales(KBEBase):
    __tablename__ = 'tally_sales'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallySalesReturn(KBEBase):
    __tablename__ = 'tally_sales_return'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchase(KBEBase):
    __tablename__ = 'tally_purchase'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchaseReturn(KBEBase):
    __tablename__ = 'tally_purchase_return'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPayment(KBEBase):
    __tablename__ = 'tally_payments'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyReceipts(KBEBase):
    __tablename__ = 'tally_receipts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyJournal(KBEBase):
    __tablename__ = 'tally_journal'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyAccounts(KBEBase):
    __tablename__ = 'tally_accounts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    ledger_name = Column(String(250), nullable= False)
    alias_code = Column(String(100), nullable= True)
    under = Column(String(100), nullable= False)
    state = Column(String(50), nullable=True)
    gst_registration_type = Column(String(100), nullable= True)
    gst_no = Column(String(100), nullable=True)
    opening_balance = Column(BigInteger, nullable=True)
    busy_name = Column(String(250), nullable= True)
    dealer_code = Column(String(100), nullable= True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyItems(KBEBase):
    __tablename__ = 'tally_items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    item_name = Column(String(250), nullable= False)
    under = Column(String(100), nullable= False)
    units = Column(String(50), nullable= False)
    opening_qty = Column(DECIMAL(10,2), nullable= False)
    rate = Column(DECIMAL(10,2), nullable= False)
    per = Column(String(50), nullable= False)
    opening_balance = Column(DECIMAL(10,2), nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())


