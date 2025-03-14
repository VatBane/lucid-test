from sqlalchemy import String, Integer, PrimaryKeyConstraint, UniqueConstraint, Text, ForeignKeyConstraint, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = 'user'

    id_: Mapped[int] = mapped_column('id', Integer)
    email: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(Text)

    __table_args__ = (PrimaryKeyConstraint('id', name='user_pkey'),
                      UniqueConstraint('email', name='user_email_uc'),
                      )


class PostOrm(Base):
    __tablename__ = 'post'

    id_: Mapped[int] = mapped_column('id', Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)

    __table_args__ = (PrimaryKeyConstraint('id', name='post_pkey'),
                      ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_fkey',
                                           ondelete='CASCADE', onupdate='CASCADE'))
