from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

engine = create_engine("mysql://flask:flask2024@localhost/mataroin", echo=False)
# Declarative base
Base = declarative_base()


#json_str = json.dumps(json_result, ensure_ascii=False, indent=4)

# Definición del modelo para 'dispositivos'
class Dispositivos(Base):
    __tablename__ = 'dispositivos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(25), nullable=False)
    descripcion = Column(String(240))
    f_crea = Column(DateTime)
    f_mod = Column(DateTime)
    f_elim = Column(DateTime)

    # Constraint para clave única en 'id'
    __table_args__ = (
        UniqueConstraint('id'),
    )

    def __repr__(self):
        return f"<Dispositivos(id='{self.id}', nombre='{self.nombre}')>"

# Definición del modelo para 'paises'
class Paises(Base):
    __tablename__ = 'paises'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    f_crea = Column(DateTime, default=datetime.now)
    f_mod = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    f_elim = Column(DateTime)

    # Constraint para clave única en 'id'
    __table_args__ = (
        UniqueConstraint('id'),
    )

    def __repr__(self):
        return f"<Paises(id='{self.id}', nombre='{self.nombre}')>"
    

# Definición del modelo para 'tags'
class Tags(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(240), nullable=False)
    f_crea = Column(Date)
    f_mod = Column(Date)
    f_elim = Column(Date)

    # Constraint para clave única en 'id'
    __table_args__ = (
        UniqueConstraint('id'),
    )

    def __repr__(self):
        return f"<Tags(id='{self.id}', nombre='{self.nombre}')>"

# Definición del modelo para 'cookies'
class Cookies(Base):
    __tablename__ = 'cookies'
    
    id = Column(Integer, primary_key=True)
    id_pais = Column(Integer, ForeignKey('paises.id'))
    id_dispositivo = Column(Integer, ForeignKey('dispositivos.id'))
    fecha_y_hora = Column(DateTime)
    id_tag = Column(Integer, ForeignKey('tags.id'))
    comprar = Column(Boolean)
    f_crea = Column(DateTime)
    f_mod = Column(DateTime)
    f_elim = Column(DateTime)

    # Relaciones
    pais = relationship("Paises", backref="cookies")
    dispositivo = relationship("Dispositivos", backref="cookies")
    tags = relationship("Tags", backref="cookies")

    def __repr__(self):
        return f"<Cookies(id='{self.id}', fecha_y_hora='{self.fecha_y_hora}')>"


# Definición de la clase Estadisticas
class Estadisticas(Base):
    __tablename__ = 'estadisticas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(200))
    estadistica = Column(Text)
    f_crea = Column(DateTime, default=None)
    f_mod = Column(DateTime, default=None)
    f_elim = Column(DateTime, default=None)


# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear una nueva instancia de Estadisticas con los datos que deseas insertar
'''nueva_estadistica = Estadisticas(
    descripcion="Descripción de ejemplo",
    estadistica="Estadística de ejemplo",
    f_crea=datetime.now(),
    f_mod=datetime.now(),
    f_elim=None
)'''

#Hacer un left join
query = (
    session.query(Cookies, Paises, Dispositivos, Tags)
    .outerjoin(Paises, Cookies.id_pais == Paises.id)
    .outerjoin(Dispositivos, Cookies.id_dispositivo == Dispositivos.id)
    .outerjoin(Tags, Cookies.id_tag == Tags.id)
)


#Ejecutar el left join
results = query.filter(Cookies.id !=None)


# Lista para almacenar los diccionarios
result_list = []

# Mostrar el left join y convertir a diccionario
for cook, pai, dip, tac in results:
    result_dict = {
        "Pais": pai.nombre,
        "Dispositivo": dip.nombre,
        "Timestamp": cook.fecha_y_hora.strftime('%Y-%m-%d %H:%M:%S'),
        "Tag": tac.nombre,
        'Compra': cook.comprar
    }
    result_list.append(result_dict)

# Mostrar la lista de diccionarios
'''for item in result_list:
    print(item)'''

print(result_list)

# Añadir la instancia a la sesión y confirmar la transacción
#session.add(nueva_estadistica)
session.commit()

# Creación de las tablas
Base.metadata.create_all(engine)

# Creación de la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Añadir la instancia a la sesión y confirmar la transacción
#session.add(nueva_estadistica)
session.commit()
