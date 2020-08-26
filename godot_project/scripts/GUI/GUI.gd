extends Control


func _ready():
	var _err = global_signal.connect("on_change_debug",self,"_on_change_debug")

func _on_change_debug(newBool):
	visible = newBool
