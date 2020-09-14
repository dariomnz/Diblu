extends Light2D



func _on_Area2D_body_entered(body):
	if body in get_tree().get_nodes_in_group("player"):
		$AnimationPlayer.play("light")
