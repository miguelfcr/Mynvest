from sqlalchemy import Column, Integer, String, Date, Float, BigInteger, ForeignKey, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload

_Base = declarative_base()

class Controll:
	def __init__(self):
		database_uri = 'postgres+psycopg2://postgres:postgres@localhost:5432/mynvest'
		self.engine = create_engine(database_uri)
		self.Session = sessionmaker(bind=self.engine)

	def recreate_database(self):
		_Base.metadata.drop_all(self.engine)
		_Base.metadata.create_all(self.engine)

	def insert(self, object_list):
		session = self.Session()
		for obj in object_list:
			session.add(obj)
		session.commit()
		session.close()

	def get_ativo(self, papel):
		session = self.Session()
		ObjAtivo = session.query(Ativo)\
						.options(joinedload(Ativo.indicadores))\
						.options(joinedload(Ativo.balanco))\
						.options(joinedload(Ativo.demonstrativo))\
						.filter_by(acao=papel).first()
		session.close()

		if not ObjAtivo:
			ObjAtivo = Ativo()

		return ObjAtivo

class Ativo(_Base):
	__tablename__ = 'ativo'
	id = Column(Integer, Sequence('ativo_id_seq'), primary_key=True)
	acao = Column(String, unique=True, nullable=False, index=True)
	nome_empresa = Column(String)
	setor = Column(String)
	subsetor = Column(String)
	cotacao = Column(Float)
	valor_mercado = Column(BigInteger)
	valor_firma = Column(BigInteger)
	numero_acoes = Column(BigInteger)
	data_ultima_cotacao = Column(Date)
	data_ultimo_balanco = Column(Date)
	data_ultima_atualizacao = Column(Date)

	def __repr__(self):
		return "<Ativo(id='{}', acao='{}', nome empresa={}, setor={}, subsetor={}, cotacao={}, valor mercado={}, valor firma={}, "\
				"numero acoes={}, data ultima cotacao={}, data ultimo balanco={} "\
				.format(self.id, self.acao, self.nome_empresa, self.setor, self.subsetor, self.cotacao, self.valor_mercado, 
						self.valor_firma, self.numero_acoes, self.data_ultima_cotacao, self.data_ultimo_balanco)

class Balanco(_Base):
	__tablename__ = 'balanco'
	id = Column(Integer, Sequence('balanco_id_seq'), primary_key=True)
	ativo_id = Column(Integer, ForeignKey('ativo.id'))
	valor_ativo = Column(Float)
	disponibilidades = Column(Float)
	ativo_circulante = Column(Float)
	divida_bruta = Column(Float)
	divida_liquida = Column(Float)
	patrimonio_liquido = Column(Float)

class Demonstrativo(_Base):
	__tablename__ = 'demonstrativo'
	id = Column(Integer, Sequence('demonstrativo_id_seq'), primary_key=True)
	ativo_id = Column(Integer, ForeignKey('ativo.id'))
	receita_liquida_12 = Column(Float)
	ebit_12 = Column(Float)
	lucro_liquido_12 = Column(Float)
	receita_liquida_3 = Column(Float)
	ebit_3 = Column(Float)
	lucro_liquido_3 = Column(Float)

class Indicadores(_Base):
	__tablename__ = 'indicadores'
	id = Column(Integer, Sequence('indicadores_id_seq'), primary_key=True)
	ativo_id = Column(Integer, ForeignKey('ativo.id'))
	p_l = Column(Float)
	p_vp = Column(Float)
	p_ebit = Column(Float)
	psr = Column(Float)
	p_ativos = Column(Float)
	p_cap_giro = Column(Float)
	p_ativ_circ_liq = Column(Float)
	div_yield = Column(Float)
	ev_ebit = Column(Float)
	giro_ativos = Column(Float)
	cres_rec5 = Column(Float)
	lpa = Column(Float)
	vpa = Column(Float)
	marg_bruta = Column(Float)
	marg_ebit = Column(Float)
	marg_liquida = Column(Float)
	ebit_ativo = Column(Float)
	roic = Column(Float)
	roe = Column(Float)
	liquidez_corr = Column(Float)
	div_bruta_patrim = Column(Float)

# Cria os relacionamentos das tabelas
Balanco.ativo = relationship("Ativo", back_populates="balanco")
Demonstrativo.ativo = relationship("Ativo", back_populates="demonstrativo")
Indicadores.ativo = relationship("Ativo", back_populates="indicadores")

Ativo.indicadores = relationship("Indicadores", order_by=Indicadores.id, back_populates="ativo")
Ativo.balanco = relationship("Balanco", order_by=Balanco.id, back_populates="ativo")
Ativo.demonstrativo = relationship("Demonstrativo", order_by=Demonstrativo.id, back_populates="ativo")

if __name__ == "__main__":
	C = Controll()
	C.recreate_database()
