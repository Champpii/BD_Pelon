from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DimFecha(Base):
    __tablename__ = 'DIM_FECHA'
    Fecha_Key = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Completa = Column(Date, nullable=False, unique=True)
    Dia = Column(Integer, nullable=False)
    Dia_Semana = Column(String(20), nullable=False)
    Semana = Column(Integer, nullable=False)
    Mes = Column(Integer, nullable=False)
    Trimestre = Column(Integer, nullable=False)
    Año = Column(Integer, nullable=False)
    Indicador_Fin_Semana = Column(Boolean, nullable=False)
    Indicador_Feriado = Column(Boolean, nullable=False)

class DimCategoria(Base):
    __tablename__ = 'DIM_CATEGORIA'
    Categoria_Key = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Categoria = Column(String(100), nullable=False)
    Descripcion = Column(String)
    Categoria_Padre = Column(Integer, ForeignKey('DIM_CATEGORIA.Categoria_Key'), nullable=True)
    subcategorias = relationship("DimCategoria", remote_side=[Categoria_Key])

class DimMarca(Base):
    __tablename__ = 'DIM_MARCA'
    Marca_Key = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Marca = Column(String(100), nullable=False, unique=True)

class DimModelo(Base):
    __tablename__ = 'DIM_MODELO'
    Modelo_Key = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Modelo = Column(String(100), nullable=False)
    Año_Lanzamiento = Column(Integer, nullable=False)
    Marca_Key = Column(Integer, ForeignKey('DIM_MARCA.Marca_Key'), nullable=False)
    marca = relationship("DimMarca")

class DimProducto(Base):
    __tablename__ = 'DIM_PRODUCTO'
    Producto_Key = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Producto = Column(String(100), nullable=False)
    Descripcion = Column(String)
    Modelo_Key = Column(Integer, ForeignKey('DIM_MODELO.Modelo_Key'), nullable=False)
    Año_Fabricacion = Column(Integer, nullable=False)
    Color = Column(String(30))
    Precio_Lista = Column(DECIMAL(10, 2), nullable=False)
    Categoria_Key = Column(Integer, ForeignKey('DIM_CATEGORIA.Categoria_Key'), nullable=False)
    modelo = relationship("DimModelo")
    categoria = relationship("DimCategoria")

class FactVentas(Base):
    __tablename__ = 'FACT_VENTAS'
    Venta_Key = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Key = Column(Integer, ForeignKey('DIM_FECHA.Fecha_Key'), nullable=False)
    Producto_Key = Column(Integer, ForeignKey('DIM_PRODUCTO.Producto_Key'), nullable=False)
    Cantidad_Vendida = Column(Integer, nullable=False)
    Precio_Unitario = Column(DECIMAL(10, 2), nullable=False)
    Descuento_Aplicado = Column(DECIMAL(10, 2), default=0.00)
    Margen_Ganancia = Column(DECIMAL(10, 2), nullable=False)
