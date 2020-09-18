extends Control


func _ready():
	get_tree().paused = false
	OS.window_borderless = true
	OS.window_maximized = true

func _on_Play_pressed():
	global.change_scene("res://scenes/Game.tscn","center")


func _on_Exit_pressed():
	get_tree().quit()


func _on_Play_dungeon_pressed():
	global.change_scene("res://scenes/Loading screen.tscn")
