extends Node

signal on_change_debug(newBool)

func _ready():
	emit_signal("on_change_debug")
