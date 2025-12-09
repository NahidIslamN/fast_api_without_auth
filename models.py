from sqlalchemy import Column, String,Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

###### write your model here

reaction_tables = Table(
    'reaction_tables',
    Base.metadata,
    Column("twit_id",Integer, ForeignKey('twits.id'), primary_key=True),
    Column("react_id",Integer, ForeignKey('reacts.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)

    frist_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    username = Column(String(100), unique=True)
    password = Column(String(100))

    twits = relationship("Twit", back_populates='creator')
    reacts = relationship("React", back_populates='creator')


class React(Base):
    __tablename__ = 'reacts'

    id = Column(Integer, primary_key=True, index=True)

    react_emuji = Column(String(10))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', back_populates='reacts')

    twits = relationship("Twit", secondary=reaction_tables, back_populates='reacts')



class Twit(Base):
    __tablename__ = 'twits'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(String(100))
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship("User", back_populates='twits')

    reacts = relationship("React", secondary=reaction_tables, back_populates='twits')