type persona struct {
	nombre string
	edad int
	pariente persona1
	activo bool
}
type persona1 struct {
	nombre string
	edad int
	pariente persona
	activo bool
}

