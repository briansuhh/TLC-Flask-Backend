from api.extensions import db
from api.models.branchstockcount import BranchStockCount

class BranchStockCountService:
    @staticmethod
    def create_branch_stock_count(branch_id, item_id, in_stock, ordered_qty):
        new_stock_count = BranchStockCount(
            branch_id=branch_id,
            item_id=item_id,
            in_stock=in_stock,
            ordered_qty=ordered_qty
        )
        db.session.add(new_stock_count)
        db.session.commit()
        return new_stock_count

    @staticmethod
    def get_all_branch_stock_counts():
        return BranchStockCount.query.all()

    @staticmethod
    def get_branch_stock_count_by_ids(branch_id, item_id):
        return BranchStockCount.query.filter_by(branch_id=branch_id, item_id=item_id).first()

    @staticmethod
    def update_branch_stock_count(branch_id, item_id, data):
        stock_count = BranchStockCount.query.filter_by(branch_id=branch_id, item_id=item_id).first()
        if not stock_count:
            return None
        
        for key, value in data.items():
            setattr(stock_count, key, value)
        
        db.session.commit()
        return stock_count

    @staticmethod
    def delete_branch_stock_count(branch_id, item_id):
        stock_count = BranchStockCount.query.filter_by(branch_id=branch_id, item_id=item_id).first()
        if not stock_count:
            return False
        
        db.session.delete(stock_count)
        db.session.commit()
        return True
