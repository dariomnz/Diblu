extends Light2D

onready var is_shoot = false


func _on_Area2D_body_entered(body):
	if not is_shoot:
		if body in get_tree().get_nodes_in_group("player"):
			$AnimationPlayer.play("light")
			is_shoot = true
			
			if get_tree().has_group("minimap"):
				get_tree().get_nodes_in_group("minimap")[0].create_room(get_parent())
