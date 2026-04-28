from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

db = SQLAlchemy()


class Process(db.Model):
    __tablename__ = 'processes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class FilterModel(db.Model):
    __tablename__ = 'filter_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(100))
    process_id = db.Column(db.Integer, db.ForeignKey('processes.id'))
    max_usage_count = db.Column(db.Integer, default=0)
    max_sterilization_count = db.Column(db.Integer, nullable=True)
    max_days = db.Column(db.Integer, nullable=True)
    use_location = db.Column(db.String(100))
    production_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_imported = db.Column(db.Boolean, default=False)
    # 飞书多维表格同步字段
    unit = db.Column(db.String(50))
    supplier = db.Column(db.String(200))
    feishu_record_id = db.Column(db.String(100))

    process = db.relationship('Process', backref='filter_models')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'spec': self.spec,
            'process_id': self.process_id,
            'process_name': self.process.name if self.process else '',
            'max_usage_count': self.max_usage_count,
            'max_sterilization_count': self.max_sterilization_count,
            'max_days': self.max_days,
            'use_location': self.use_location or '',
            'production_date': self.production_date.strftime('%Y-%m-%d') if self.production_date else '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else '',
            'is_imported': self.is_imported,
            'unit': self.unit or '',
            'supplier': self.supplier or '',
            'feishu_record_id': self.feishu_record_id or ''
        }


class Filter(db.Model):
    __tablename__ = 'filters'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False, unique=True)
    model_id = db.Column(db.Integer, db.ForeignKey('filter_models.id'))
    current_usage_count = db.Column(db.Integer, default=0)
    current_sterilization_count = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, default=lambda: datetime.now().date())
    status = db.Column(db.String(20), default='normal')
    use_location = db.Column(db.String(100))
    production_date = db.Column(db.Date)
    operator = db.Column(db.String(50))
    receivers = db.Column(db.String(500))
    use_process_name = db.Column(db.String(100))
    record_max_sterilization = db.Column(db.Integer, nullable=True)
    is_usage_record = db.Column(db.Boolean, default=False)
    last_sterilization_alert_at = db.Column(db.DateTime)
    last_expiry_alert_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    feishu_record_id = db.Column(db.String(100))

    model = db.relationship('FilterModel', backref='filters')

    def to_dict(self):
        expire_date = None
        days_left = None
        if self.model and self.model.max_days and self.model.max_days > 0:
            # 有效期计算优先基于 production_date，其次 start_date
            base_date = self.production_date or self.start_date
            if base_date:
                expire_date = base_date + timedelta(days=self.model.max_days)
                days_left = (expire_date - datetime.now().date()).days

        usage_ratio = 0
        if self.model and self.model.max_usage_count and self.model.max_usage_count > 0:
            usage_ratio = self.current_usage_count / self.model.max_usage_count

        sterilization_ratio = 0
        if self.model and self.model.max_sterilization_count and self.model.max_sterilization_count > 0:
            sterilization_ratio = self.current_sterilization_count / self.model.max_sterilization_count

        return {
            'id': self.id,
            'code': self.code,
            'model_id': self.model_id,
            'model_name': self.model.name if self.model else '',
            'spec': self.model.spec if self.model else '',
            'process_name': self.model.process.name if self.model and self.model.process else '',
            'current_usage_count': self.current_usage_count,
            'max_usage_count': self.model.max_usage_count if self.model else 0,
            'usage_ratio': round(usage_ratio * 100, 1),
            'current_sterilization_count': self.current_sterilization_count,
            'max_sterilization_count': self.model.max_sterilization_count if self.model else None,
            'sterilization_ratio': round(sterilization_ratio * 100, 1),
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'expire_date': expire_date.strftime('%Y-%m-%d') if expire_date else '',
            'days_left': days_left,
            'max_days': self.model.max_days if self.model else None,
            'unit': self.model.unit if self.model else '',
            'supplier': self.model.supplier if self.model else '',
            'use_location': self.use_location or '',
            'production_date': self.production_date.strftime('%Y-%m-%d') if self.production_date else '',
            'operator': self.operator or '',
            'receivers': self.receivers or '',
            'use_process_name': self.use_process_name or '',
            'record_max_sterilization': self.record_max_sterilization,
            'is_usage_record': self.is_usage_record,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else '',
            'feishu_record_id': self.feishu_record_id or ''
        }

    def get_warnings(self):
        warnings = []
        if not self.model:
            return warnings

        # 读取系统预警配置
        cfg = Config.query.first()
        alert_days = cfg.alert_days if cfg else 7
        alert_sterilization_remaining = cfg.alert_sterilization_remaining if cfg else 0

        # 有效期（优先基于 production_date）
        if self.model.max_days and self.model.max_days > 0:
            base_date = self.production_date or self.start_date
            if base_date:
                expire_date = base_date + timedelta(days=self.model.max_days)
                days_left = (expire_date - datetime.now().date()).days
                if days_left <= 0:
                    warnings.append(f'已到效期 ({expire_date.strftime("%Y-%m-%d")})')
                elif days_left <= alert_days:
                    warnings.append(f'即将达到效期 ({expire_date.strftime("%Y-%m-%d")})')

        # 灭菌次数（基于剩余次数预警）
        if self.model.max_sterilization_count and self.model.max_sterilization_count > 0:
            remaining = self.model.max_sterilization_count - self.current_sterilization_count
            if remaining <= 0:
                warnings.append(f'灭菌次数已达上限 ({self.current_sterilization_count}/{self.model.max_sterilization_count})')
            elif remaining <= alert_sterilization_remaining:
                warnings.append(f'灭菌次数即将超限 ({self.current_sterilization_count}/{self.model.max_sterilization_count})')

        return warnings

    def update_status(self):
        warnings = self.get_warnings()
        # 判断是否已超限（expired）
        is_expired = False
        is_warning = False
        for w in warnings:
            if '已达上限' in w or '已到效期' in w:
                is_expired = True
                break
            else:
                is_warning = True
        if is_expired:
            self.status = 'expired'
        elif is_warning:
            self.status = 'warning'
        else:
            self.status = 'normal'
        db.session.commit()
        return self.status


class UsageRecord(db.Model):
    __tablename__ = 'usage_records'
    id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, db.ForeignKey('filters.id'))
    usage_date = db.Column(db.DateTime, default=datetime.now)
    note = db.Column(db.String(200))

    filter_obj = db.relationship('Filter', backref='usage_records')

    def to_dict(self):
        return {
            'id': self.id,
            'filter_code': self.filter_obj.code if self.filter_obj else '',
            'filter_model': self.filter_obj.model.name if self.filter_obj and self.filter_obj.model else '',
            'process_name': self.filter_obj.model.process.name if self.filter_obj and self.filter_obj.model and self.filter_obj.model.process else '',
            'usage_date': self.usage_date.strftime('%Y-%m-%d %H:%M') if self.usage_date else '',
            'note': self.note or ''
        }


class SterilizationRecord(db.Model):
    __tablename__ = 'sterilization_records'
    id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, db.ForeignKey('filters.id'))
    sterilization_date = db.Column(db.DateTime, default=datetime.now)
    note = db.Column(db.String(200))

    filter_obj = db.relationship('Filter', backref='sterilization_records')

    def to_dict(self):
        return {
            'id': self.id,
            'filter_code': self.filter_obj.code if self.filter_obj else '',
            'filter_model': self.filter_obj.model.name if self.filter_obj and self.filter_obj.model else '',
            'process_name': self.filter_obj.model.process.name if self.filter_obj and self.filter_obj.model and self.filter_obj.model.process else '',
            'sterilization_date': self.sterilization_date.strftime('%Y-%m-%d %H:%M') if self.sterilization_date else '',
            'note': self.note or ''
        }


class Config(db.Model):
    __tablename__ = 'configs'
    id = db.Column(db.Integer, primary_key=True)
    feishu_webhook = db.Column(db.String(500), default='')
    alert_days = db.Column(db.Integer, default=7)
    alert_sterilization_remaining = db.Column(db.Integer, default=0)
    # 全局预警看板飞书推送配置
    alert_push_enabled = db.Column(db.Boolean, default=False)
    alert_push_time = db.Column(db.String(10), default='08:00')
    alert_push_receivers = db.Column(db.String(500), default='')
    # 飞书扫码登录配置
    feishu_app_id = db.Column(db.String(100), default='')
    feishu_app_secret = db.Column(db.String(200), default='')
    # 飞书多维表格同步配置
    feishu_bitable_app_token = db.Column(db.String(100), default='')
    feishu_bitable_table_id = db.Column(db.String(100), default='')
    feishu_bitable_sync_enabled = db.Column(db.Boolean, default=False)
    feishu_bitable_sync_interval = db.Column(db.Integer, default=5)

    def to_dict(self):
        return {
            'feishu_webhook': self.feishu_webhook,
            'alert_days': self.alert_days,
            'alert_sterilization_remaining': self.alert_sterilization_remaining,
            'alert_push_enabled': self.alert_push_enabled,
            'alert_push_time': self.alert_push_time,
            'alert_push_receivers': self.alert_push_receivers or '',
            'feishu_app_id': self.feishu_app_id,
            'feishu_app_secret': self.feishu_app_secret,
            'feishu_bitable_app_token': self.feishu_bitable_app_token or '',
            'feishu_bitable_table_id': self.feishu_bitable_table_id or '',
            'feishu_bitable_sync_enabled': self.feishu_bitable_sync_enabled,
            'feishu_bitable_sync_interval': self.feishu_bitable_sync_interval or 5
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    real_name = db.Column(db.String(50))
    role = db.Column(db.String(20), default='operator')  # admin / operator
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 飞书登录绑定
    feishu_open_id = db.Column(db.String(100), unique=True, nullable=True)
    feishu_union_id = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'real_name': self.real_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'feishu_open_id': self.feishu_open_id or ''
        }


class FilterReplacementRecord(db.Model):
    __tablename__ = 'filter_replacement_records'
    id = db.Column(db.Integer, primary_key=True)
    filter_id = db.Column(db.Integer, db.ForeignKey('filters.id'))
    old_start_date = db.Column(db.Date)
    new_start_date = db.Column(db.Date)
    old_usage_count = db.Column(db.Integer, default=0)
    old_sterilization_count = db.Column(db.Integer, default=0)
    replaced_at = db.Column(db.DateTime, default=datetime.now)
    replaced_by = db.Column(db.String(50))
    note = db.Column(db.String(200))

    filter_obj = db.relationship('Filter', backref='replacement_records')

    def to_dict(self):
        return {
            'id': self.id,
            'filter_code': self.filter_obj.code if self.filter_obj else '',
            'filter_model': self.filter_obj.model.name if self.filter_obj and self.filter_obj.model else '',
            'process_name': self.filter_obj.model.process.name if self.filter_obj and self.filter_obj.model and self.filter_obj.model.process else '',
            'old_start_date': self.old_start_date.strftime('%Y-%m-%d') if self.old_start_date else '',
            'new_start_date': self.new_start_date.strftime('%Y-%m-%d') if self.new_start_date else '',
            'old_usage_count': self.old_usage_count,
            'old_sterilization_count': self.old_sterilization_count,
            'replaced_at': self.replaced_at.strftime('%Y-%m-%d %H:%M') if self.replaced_at else '',
            'replaced_by': self.replaced_by or '',
            'note': self.note or ''
        }
