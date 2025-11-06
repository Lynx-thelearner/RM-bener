from sqlalchemy import Column, Integer, String, DATE, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.core.database import Base
import enum
from datetime import date
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Time
from sqlalchemy import DateTime
from sqlalchemy.sql import func

metadata = Base.metadata

#Enum buat user role
class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    reservationStaff = "reservationStaff"
    waiter = "waiter"
    customer = "customer"


    
class User(Base):
    __tablename__ = "user"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    nama = Column(String, nullable=False)
    no_telp = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    
    reservations = relationship("Reservation", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")

class Meja(Base):
    __tablename__ = "meja"
    
    meja_id = Column(Integer, primary_key=True, index=True)
    kode_meja = Column(String, unique=True, index=True, nullable=False)
    kapasitas = Column(Integer, nullable=False)
    lokasi = Column(String, nullable=False)
    
    reservations = relationship("Reservation", back_populates="meja")

class ReservationStatus(enum.Enum):
    menunggu = "menunggu"
    berhasil = "berhasil"
    dibatalkan = "dibatalkan"
    
class Reservation(Base):
    __tablename__ = "reservation"
    
    reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    meja_id = Column(Integer, ForeignKey("meja.meja_id"), nullable=False)
    tanggal_reservasi = Column(DATE, default=date.today, nullable=False)
    jam_reservasi = Column(Time, nullable=False)
    jumlah_orang = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.menunggu, nullable=False)
    
    user = relationship("User", back_populates="reservations")
    meja = relationship("Meja", back_populates="reservations")
    payment = relationship("Payment", back_populates="reservation")
    
class PaymentStatus(enum.Enum):
    menunggu = "menunggu"
    berhasil = "berhasil"
    gagal = "gagal"

class Payment(Base):
    __tablename__ = "payment"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservation.reservation_id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_date = Column(DateTime(timezone=True), server_default=func.now(), default=date.today, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.menunggu, nullable=False)
    
    reservation = relationship("Reservation", back_populates="payment")

class Feedback(Base):
    __tablename__ = "feedback"
    
    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservation.reservation_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)
    feedback_date = Column(DATE, default=date.today, nullable=False)
    
    user = relationship("User", back_populates="feedbacks")
    reservation = relationship("Reservation", back_populates="feedbacks")
