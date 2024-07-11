from sqlalchemy import Column, Integer, String, Float, DateTime, func
from Database.models.base  import Base
from sqlalchemy import event


class BusyPricingKBBIO(Base):
    __tablename__ = 'busy_pricing_kbbio'

    id = Column(Integer, primary_key= True, autoincrement= True, index= True)
    item_name = Column(String(255), index= True, nullable=False)
    customer_type = Column(String(50), nullable= False, index=True) 
    mrp = Column(Float, nullable= False, default=0)
    selling_price = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())


        # Define a validation function to check for duplicate item_name and customer_type
# def validate_distinct_item_customer(target, value, oldvalue, initiator):
#     # Query the database to check if there is any existing row with the same item_name and customer_type
#     existing_row = target.query.filter_by(item_name=value.item_name, customer_type=value.customer_type).first()
    
#     if existing_row and existing_row.id != value.id:
#         raise ValueError("Item name and customer type combination must be unique.")

# # Attach the validation function to the 'before_insert' and 'before_update' events of BusyPricingKBBIO
# event.listen(BusyPricingKBBIO, 'before_insert', validate_distinct_item_customer)
# event.listen(BusyPricingKBBIO, 'before_update', validate_distinct_item_customer)