
def calcula_anualidad(
		monto: float,
		tasa_mes: float,
		plazo_meses):
	
	t2 = (1 + tasa_mes) ** -plazo_meses
	return (monto * tasa_mes) / (1-t2)


def calcula_intereses(
		periodo: int,
		anualidad: float,
		tasa_mes: float,
		capital_periodo_anterior: float):
	"""
	Calcula los diferentes parametros de la tabla de amortización
	basandose en reglas de recurrencia:
	Interes: I(n) = i C(n-1), donde i es la tasa mensual y C el capital
	Amortizacion: A(n) = a - I(n),
		donde a es la anualidad (constante): a = i M / [1- [1+i]^-n],
		Siendo M el monto
	Capital: C(n) = C(n-1) - A(n)

	La función devuelve una tupla con los valores: (periodo o mes, a, I, A, C)
	"""
	interes_calculado = tasa_mes * capital_periodo_anterior
	amortizacion_calculado = anualidad - interes_calculado
	capital_calculado = capital_periodo_anterior - amortizacion_calculado
	return (
		periodo,
		anualidad,
		interes_calculado,
		amortizacion_calculado,
		capital_calculado )


def calcula_tabla_amortizacion(monto: float, tasa_mes: float, plazo_meses: int) -> list[tuple[int, float, float, float, float]]:
	anualidad: float = calcula_anualidad(monto, tasa_mes, plazo_meses)

	intereses_calculados: tuple[int, float, float, float, float] = \
		(0, 0, 0, 0, monto)

	tabla_amortizacion: list[tuple[int, float, float, float, float]] = \
		[intereses_calculados]

	for periodo in range(plazo_meses):
		intereses_calculados: tuple[int, float, float, float, float] = \
			calcula_intereses(periodo+1, anualidad, tasa_mes, intereses_calculados[4])
		tabla_amortizacion.append(intereses_calculados)
	
	return tabla_amortizacion