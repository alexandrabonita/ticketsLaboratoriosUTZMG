from datetime import datetime
import enum
from database import Base  # <--- IMPORTAR LA BASE DE DATABASE.PY
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class EstadoEquipo(str, enum.Enum):
  OPERATIVO = "Operativo"
  EN_MANTENIMIENTO = "En Mantenimiento"
  FUERA_DE_SERVICIO = "Fuera de Servicio"
  PRESTADO = "Prestado"


class PrioridadTicket(str, enum.Enum):
  BAJA = "Baja"
  MEDIA = "Media"
  ALTA = "Alta/Paro de Práctica"


class EstatusTicket(str, enum.Enum):
  ABIERTO = "Abierto"
  EN_REVISION = "En Revisión"
  RESUELTO = "Resuelto"


class Laboratorio(Base):
  __tablename__ = "laboratorios"
  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(100), nullable=False)
  edificio = Column(String(50))
  encargado = Column(String(100))
  correo_encargado = Column(String(100))

  equipos = relationship("Equipo", back_populates="laboratorio")
  consumibles = relationship("Consumible", back_populates="laboratorio")


class Equipo(Base):
  __tablename__ = "equipos"
  id_codigo_qr = Column(String(50), primary_key=True, index=True)
  laboratorio_id = Column(Integer, ForeignKey("laboratorios.id"))
  nombre = Column(String(120), nullable=False)
  marca = Column(String(60))
  modelo = Column(String(60))
  num_serie = Column(String(60))
  estatus = Column(
      Enum(EstadoEquipo), default=EstadoEquipo.OPERATIVO, nullable=False
  )
  manual_pdf_url = Column(String(255), nullable=True)

  laboratorio = relationship("Laboratorio", back_populates="equipos")
  tickets = relationship("TicketIncidencia", back_populates="equipo")
  mantenimientos = relationship(
      "HistorialMantenimiento", back_populates="equipo"
  )


class Consumible(Base):
  __tablename__ = "consumibles"
  id_codigo_qr = Column(String(50), primary_key=True, index=True)
  laboratorio_id = Column(Integer, ForeignKey("laboratorios.id"))
  descripcion = Column(String(150), nullable=False)
  categoria = Column(String(60))
  stock_actual = Column(Integer, default=0)
  stock_minimo = Column(Integer, default=5)
  unidad_medida = Column(String(30))

  laboratorio = relationship("Laboratorio", back_populates="consumibles")
  despachos = relationship("DespachoConsumible", back_populates="consumible")


class DespachoConsumible(Base):
  __tablename__ = "despachos_consumibles"
  id = Column(Integer, primary_key=True, index=True)
  consumible_id = Column(String(50), ForeignKey("consumibles.id_codigo_qr"))
  fecha_hora = Column(DateTime, default=datetime.utcnow)
  cantidad = Column(Integer, nullable=False)
  matricula_solicitante = Column(String(30), nullable=False)
  docente_a_cargo = Column(String(100), nullable=False)

  consumible = relationship("Consumible", back_populates="despachos")


class TicketIncidencia(Base):
  __tablename__ = "tickets_incidencia"
  id = Column(Integer, primary_key=True, index=True)
  equipo_id = Column(String(50), ForeignKey("equipos.id_codigo_qr"))
  fecha_reporte = Column(DateTime, default=datetime.utcnow)
  matricula_reporta = Column(String(30), nullable=False)
  prioridad = Column(
      Enum(PrioridadTicket), default=PrioridadTicket.MEDIA, nullable=False
  )
  descripcion = Column(Text, nullable=False)
  evidencia_multimedia = Column(String(255), nullable=True)
  estatus = Column(
      Enum(EstatusTicket), default=EstatusTicket.ABIERTO, nullable=False
  )

  equipo = relationship("Equipo", back_populates="tickets")


class HistorialMantenimiento(Base):
  __tablename__ = "historial_mantenimientos"
  id = Column(Integer, primary_key=True, index=True)
  equipo_id = Column(String(50), ForeignKey("equipos.id_codigo_qr"))
  tipo_servicio = Column(String(50))
  fecha_servicio = Column(DateTime, default=datetime.utcnow)
  tecnico_responsable = Column(String(100), nullable=False)
  refacciones = Column(Text, nullable=True)
  observaciones = Column(Text, nullable=False)
  proxima_fecha = Column(DateTime, nullable=True)

  equipo = relationship("Equipo", back_populates="mantenimientos")