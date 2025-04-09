from app import db

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    
    # 关系
    users = db.relationship('User', back_populates='group')
    
    # 预定义的用户组
    SUPER_ADMIN = '超级管理员'
    ADMIN = '管理员'
    USER = '普通用户'
    
    def has_permission(self, permission):
        """
        简单的权限检查
        TODO: 实现更复杂的权限系统
        """
        if self.name == self.SUPER_ADMIN:
            return True
        if self.name == self.ADMIN:
            return permission in ['edit_user', 'add_user']
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_count': len(self.users)
        } 