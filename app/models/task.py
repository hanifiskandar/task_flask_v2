from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.Text, nullable = True)
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='medium')  # low, medium, high
    status = db.Column(db.Integer, nullable=False, default=1)  # 1=To Do, 2=Doing, 3=Done
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority.capitalize(),
            "status": {1: "To Do", 2: "Doing", 3: "Done"}.get(self.status, "Unknown"),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    