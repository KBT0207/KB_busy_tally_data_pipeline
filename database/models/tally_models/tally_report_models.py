from sqlalchemy import Column, Integer, String, DECIMAL, Float, Date, DateTime, BigInteger, func
from database.models.base import Base



class TallySales(Base):
    __tablename__ = 'tally_sales'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallySalesReturn(Base):
    __tablename__ = 'tally_sales_return'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchase(Base):
    __tablename__ = 'tally_purchase'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPurchaseReturn(Base):
    __tablename__ = 'tally_purchase_return'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_type = Column(String(100), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    debit = Column(Float, nullable= False, default=0)
    credit = Column(Float, nullable= False, default=0)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyPayment(Base):
    __tablename__ = 'tally_payment'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyReceipts(Base):
    __tablename__ = 'tally_receipts'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyJournal(Base):
    __tablename__ = 'tally_journal'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    date = Column(Date, nullable= False)
    particulars = Column(String(255), nullable= False)
    voucher_no = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    amount_type = Column(String(10), nullable=True)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())



class TallyAccounts(Base):
    __tablename__ = 'tally_accounts'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    ledger_name = Column(String(250), nullable= False)
    alias_code = Column(String(100), nullable= True)
    under = Column(String(100), nullable= False)
    state = Column(String(50), nullable=True)
    gst_registration_type = Column(String(100), nullable= True)
    gst_no = Column(String(15), nullable=True)
    opening_balance = Column(DECIMAL(10,2), nullable=True)
    busy_name = Column(String(250), nullable= True)
    dealer_code = Column(String(100), nullable= False)
    material_centre = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())