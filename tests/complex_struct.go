type complexStruct struct {
    prop1 string
	prop2 int
	prop3 float64
	prop4 bool
	prop5 []string
	prop6 []int
	prop7 []float64
	prop8 []bool
	prop9 struct {
		prop91 []string
		prop92 int
		prop93 []float64
		prop94 []bool
		prop95 struct {
			prop951 auxComplexStruct1
		}
	}
}

type auxComplexStruct1 struct {
    prop9511 []string
	prop9512 []int
	prop9513 auxComplexStruct2
	prop9514 bool
	prop9515 struct {
		prop95151 string
		prop95152 int
		prop95153 float64
		prop95154 bool
		prop95155 struct {
			prop951551 auxComplexStruct3
		}
	}
}

type auxComplexStruct2 struct {
	prop95131 [][]string
	prop95132 auxComplexStruct4
}

type auxComplexStruct3 struct {
	prop9515511 [][][][]bool
}

type auxComplexStruct4 struct {}