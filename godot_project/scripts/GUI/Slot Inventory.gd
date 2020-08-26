extends Button

signal clicked

func _ready():
	var _err = connect("button_down",self,"_buttom_down")
	
func _buttom_down():
	emit_signal("clicked",self)
