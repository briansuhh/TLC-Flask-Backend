from api.extensions import db
from api.models.branches import Branch

class BranchService:
    @staticmethod
    def create_branch(name, address):
        new_branch = Branch(
            name=name,
            address=address
        )
        db.session.add(new_branch)
        db.session.commit()
        return new_branch

    @staticmethod
    def get_all_branches():
        return Branch.query.all()

    @staticmethod
    def get_branch_by_id(branch_id):
        return db.session.get(Branch, branch_id)

    @staticmethod
    def update_branch(branch_id, data):
        branch = db.session.get(Branch, branch_id)
        if not branch:
            return None
        
        for key, value in data.items():
            setattr(branch, key, value)
        
        db.session.commit()
        return branch

    @staticmethod
    def delete_branch(branch_id):
        branch = db.session.get(Branch, branch_id)
        if not branch:
            return False
        
        db.session.delete(branch)
        db.session.commit()
        return True
