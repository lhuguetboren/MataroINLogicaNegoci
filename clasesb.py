from sqlalchemy import create_engine, Column, Integer, String, DateTime,Enum,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

# Configuración de la conexión a la base de datos
engine = create_engine("mysql://flask:flask2024@localhost/mataroin", echo=True)

def get_current_time_in_spain():
    spain_tz = pytz.timezone('Europe/Madrid')
    return datetime.now(spain_tz)

Base = declarative_base()

# Definición del modelo
class Biblioteca(Base):
    __tablename__ = 'biblioteca'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))
    nombre = Column(String(100))
    descripcion = Column(String(50))
    filename = Column(String(50))
    duracion = Column(Integer)
    texto = Column(String(50))
    imagen = Column(String(50))
    formato = Column(String(50))
    f_crea = Column(DateTime, default=get_current_time_in_spain)
    f_mod = Column(DateTime, default=get_current_time_in_spain, onupdate=get_current_time_in_spain)

    tags_relacion = relationship('TagsRelacion', back_populates='biblioteca')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(240), nullable=False)
    f_crea = Column(DateTime, default=get_current_time_in_spain)
    f_elim = Column(DateTime, default=get_current_time_in_spain)
    f_mod = Column(DateTime, default=get_current_time_in_spain, onupdate=get_current_time_in_spain)

    tags_relacion = relationship('TagsRelacion', back_populates='tag')

class TagsRelacion(Base):
    __tablename__ = 'tags_relacion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    origen = Column(String,nullable=False)
    id_origen = Column(Integer, ForeignKey('biblioteca.id'), nullable=False)
    id_tag = Column(Integer, ForeignKey('tags.id'), nullable=False)
    f_crea = Column(DateTime, default=get_current_time_in_spain)
    f_mod = Column(DateTime, default=get_current_time_in_spain, onupdate=get_current_time_in_spain)
    f_elim = Column(DateTime, default=get_current_time_in_spain)

    biblioteca = relationship('Biblioteca', back_populates='tags_relacion')
    tag = relationship('Tag', back_populates='tags_relacion')

    

    def __repr__(self):
        return f"<Biblioteca(id='{self.id}', tipo={self.tipo}, nombre={self.nombre}, descripcion={self.descripcion})>"

    def guardar(self, session):
        session.add(self)
        session.commit()

    

# Creación de las tablas
Base.metadata.create_all(engine)

# Creación de la sesión
Session = sessionmaker(bind=engine)
session = Session()


