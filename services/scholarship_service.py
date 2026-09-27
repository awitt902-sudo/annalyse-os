from models.scholarship import ScholarshipModel


def get_scholarships(db, skip: int = 0, limit: int = 100):
    return db.query(ScholarshipModel).offset(skip).limit(limit).all()
