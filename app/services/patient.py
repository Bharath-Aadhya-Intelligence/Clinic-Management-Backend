from .base import BaseService
from datetime import datetime, date, timedelta
from typing import List, Dict

class PatientService(BaseService):
    def __init__(self):
        super().__init__("patients")

    async def create_patient(self, data: dict):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        
        # Extract treatment dates if provided
        second_date = data.pop("second_treatment_date", None)
        third_date = data.pop("third_treatment_date", None)
        
        # Initialize 3 appointments
        # Appointment 1 uses the main visit_date
        visit_date = data.get("visit_date")
        if isinstance(visit_date, date):
            visit_date = datetime.combine(visit_date, datetime.min.time())
            
        data["appointments"] = [
            {"appointment_number": 1, "date": visit_date, "status": "Scheduled"},
            {"appointment_number": 2, "date": datetime.combine(second_date, datetime.min.time()) if second_date else None, "status": "Scheduled"},
            {"appointment_number": 3, "date": datetime.combine(third_date, datetime.min.time()) if third_date else None, "status": "Scheduled"}
        ]
        return await self.create(data)

    async def update_patient(self, id: str, data: dict):
        data["updated_at"] = datetime.utcnow()
        return await self.update(id, data)

    async def get_patients_by_visit_date(self, visit_date: date):
        # Note: MongoDB stores dates as datetime. We need to match the date part.
        start = datetime.combine(visit_date, datetime.min.time())
        end = start + timedelta(days=1)
        return await self.get_all({"visit_date": {"$gte": start, "$lt": end}})

    async def get_today_visit_count(self):
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = start + timedelta(days=1)
        return await self.collection.count_documents({"visit_date": {"$gte": start, "$lt": end}})

    async def get_monthly_visit_count(self):
        today = date.today()
        start = datetime(today.year, today.month, 1)
        if today.month == 12:
            end = datetime(today.year + 1, 1, 1)
        else:
            end = datetime(today.year, today.month + 1, 1)
        return await self.collection.count_documents({"visit_date": {"$gte": start, "$lt": end}})

    async def get_monthly_visit_breakdown(self):
        today = date.today()
        start = datetime(today.year, today.month, 1)
        if today.month == 12:
            end = datetime(today.year + 1, 1, 1)
        else:
            end = datetime(today.year, today.month + 1, 1)
            
        pipeline = [
            {"$match": {"visit_date": {"$gte": start, "$lt": end}}},
            {"$group": {
                "_id": {"$dayOfMonth": "$visit_date"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=31)

    async def get_reminders_for_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
        tomorrow_end = tomorrow_start + timedelta(days=1)
        
        # Check all 3 appointments for tomorrow's date
        query = {
            "$or": [
                {"appointments.0.date": {"$gte": tomorrow_start, "$lt": tomorrow_end}},
                {"appointments.1.date": {"$gte": tomorrow_start, "$lt": tomorrow_end}},
                {"appointments.2.date": {"$gte": tomorrow_start, "$lt": tomorrow_end}}
            ]
        }
        return await self.get_all(query)

patient_service = PatientService()
