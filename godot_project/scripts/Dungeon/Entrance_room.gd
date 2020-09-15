tool
extends General_room

func _ready():
	var player = preload("res://prefabs/entity/Slime/Slime.tscn").instance()
	add_child(player)
	player.global_position = $Spawn_point.global_position
