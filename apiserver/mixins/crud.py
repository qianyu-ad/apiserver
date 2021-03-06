from apiserver.extends import db
from datetime import datetime


class CRUDMixin(object):

    @classmethod
    def get_first(cls, **kw):
        instance = cls.get(**kw).first()
        return instance

    @classmethod
    def get(cls, **kw):
        instance_list = cls.query.filter_by(**kw)
        return instance_list

    @classmethod
    def create(cls, **kw):
        instance = cls(**kw)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, **kw):
        for k, v in kw.items():
            if getattr(self, k) != v:
                setattr(self, k, v)
        else:
            self.update_time = datetime.now()
        db.session.commit()

    def delete(self, force=False):
        if not force:
            self.update(soft_del=True)
        else:
            db.session.delete(self)
            db.session.commit()