extends Node


func create_float_text(obj : Node2D,text):
	var damage_text = preload("res://prefabs/GUI/Floating text.tscn").instance()
	
	damage_text.initialize(obj.global_position,text)
	damage_text.z_index=obj.z_index+1
	
	get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",damage_text)

func spawn_item(world_position : Vector2,item_name : String,amount : int = 1):
	get_tree().get_nodes_in_group("Chunk_control")[0].spawn_item(world_position,item_name,amount)
