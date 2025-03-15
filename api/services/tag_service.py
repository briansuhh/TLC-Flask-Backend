from api.extensions import db
from api.models.tags import Tag

class TagService:
    @staticmethod
    def create_tag(name):
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    @staticmethod
    def get_all_tags():
        return Tag.query.all()

    @staticmethod
    def get_tag_by_id(tag_id):
        return db.session.get(Tag, tag_id)

    @staticmethod
    def update_tag(tag_id, data):
        tag = db.session.get(Tag, tag_id)
        if not tag:
            return None

        for key, value in data.items():
            setattr(tag, key, value)

        db.session.commit()
        return tag

    @staticmethod
    def delete_tag(tag_id):
        tag = db.session.get(Tag, tag_id)
        if not tag:
            return False

        db.session.delete(tag)
        db.session.commit()
        return True
