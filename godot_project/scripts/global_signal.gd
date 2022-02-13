extends Node

signal on_change_debug(newBool)
signal on_change_zoom(newZoom)

func _ready():
	emit_signal("on_change_debug")
	emit_signal("on_change_zoom")
