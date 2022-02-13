extends Area2D


func _ready():
	pass


func _on_Portal_body_entered(body):
	if body in get_tree().get_nodes_in_group("player"):
		global.change_scene("res://scenes/Title Screen.tscn")
