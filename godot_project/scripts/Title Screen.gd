extends Control

func _ready():
	get_tree().paused = false
	OS.window_maximized = true

func _on_Play_pressed():
	var _err = get_tree().change_scene("res://scenes/Game.tscn")


func _on_Exit_pressed():
	get_tree().quit()


func _on_Play_dungeon_pressed():
	var _err = get_tree().change_scene("res://scenes/Loading screen.tscn")
