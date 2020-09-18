extends Node


func create_float_text(obj : Node2D,text):
	var damage_text = preload("res://prefabs/GUI/Floating text.tscn").instance()
	
	damage_text.initialize(obj.global_position,text)
	damage_text.z_index=obj.z_index+1
	
	get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",damage_text)

func spawn_item(world_position : Vector2,item_name : String,amount : int = 1):
	get_tree().get_nodes_in_group("Chunk_control")[0].spawn_item(world_position,item_name,amount)


func create_transition(transition_name  : String):
	"""Return the lengyh of the animation"""
	var transition = preload("res://prefabs/shaders/Transition layer.tscn").instance()
	get_tree().root.add_child(transition)
	transition.play(transition_name)
	return transition.get_anim_length()
	
func change_scene(path : String,transition_name = null ):
	var _transition_time
	if transition_name:
		_transition_time = create_transition(transition_name+" in")
		yield(get_tree().create_timer(_transition_time),"timeout")
		
	var new_scene = load(path).instance()
	for child in get_tree().root.get_children():
		if not child.name.begins_with("global"):
			child.queue_free()
	get_tree().root.add_child(new_scene)
	if transition_name:
		create_transition(transition_name+" out")
