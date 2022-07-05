type persona struct {
	nombre string
	edad int
	ventas []float64
	activo bool
}

type pais struct {
	nombre string
	codigo struct {
		prefijo string
		sufijo string
	}
}