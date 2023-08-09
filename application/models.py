from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, VARCHAR, DateTime, text
from sqlalchemy.orm import relationship

from application.database import Base


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=True)
    password = Column(VARCHAR(255), nullable=True)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                         comment='更新时间')
    remark = Column(String(255, 'utf8mb4_general_ci'), comment='备注')


class Tweets(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=True)
    screen_name = Column(VARCHAR(255), nullable=True)
    tweets_time = Column(Integer, nullable=True)
    full_text = Column(String)
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                         comment='更新时间')
    remark = Column(String(255, 'utf8mb4_general_ci'), comment='备注')
