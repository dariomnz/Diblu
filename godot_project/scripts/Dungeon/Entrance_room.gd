tool
extends General_room

func _ready():
	var player = preload("res://prefabs/entity/Slime/Slime.tscn").instance()
	add_child(player)
	player.global_position = $Spawn_point.global_position
	
#	if get_tree().has_group("minimap"):
#		get_tree().get_nodes_in_group("minimap")[0].create_room(self)
