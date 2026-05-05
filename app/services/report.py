from .order import order_service
from datetime import datetime
import csv
import io

class ReportService:
    async def generate_orders_csv(self) -> str:
        """
        Generates a CSV string of all orders for administrative reporting.
        Handles data transformation and formatting on the server side.
        """
        orders = await order_service.get_all()
        
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        
        # Write Headers
        headers = ['Order ID', 'Customer Name', 'Phone Number', 'Medicine', 'Price', 'Status', 'Date', 'Delivery Address']
        writer.writerow(headers)
        
        # Write Data
        for order in orders:
            order_id = f"#{str(order.get('id') or order.get('_id'))[:8]}"
            order_date = order.get('order_date')
            if isinstance(order_date, datetime):
                formatted_date = order_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                formatted_date = "N/A"
                
            writer.writerow([
                order_id,
                order.get('customer_name'),
                order.get('phone_number'),
                order.get('medicine_name'),
                order.get('medicine_price'),
                order.get('status'),
                formatted_date,
                order.get('address')
            ])
            
        return output.getvalue()

report_service = ReportService()
