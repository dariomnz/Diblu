tool
extends Node

var entrances : Array setget ,get_entrances
var rooms : Array setget ,get_rooms
var corridors : Array setget ,get_corridors

func new_entrance(parent_node : Node,owner_node : Node,rand : RandomNumberGenerator) -> General_room:
	"""Instance a new aleatory entrance"""
	var _rooms = get_entrances()
	var room_instance : General_room = _rooms[rand.randi_range(0,len(_rooms)-1)].instance()
	parent_node.add_child(room_instance)
	room_instance.initialize()
	room_instance.set_owner(owner_node)
	return room_instance
	
	
func new_room(parent_node : Node,owner_node : Node,rand : RandomNumberGenerator) -> General_room:
	"""Instance a new aleatory room"""
	var _rooms = get_rooms()
	var room_instance : General_room = _rooms[rand.randi_range(0,len(_rooms)-1)].instance()
	parent_node.add_child(room_instance)
	room_instance.initialize()
	room_instance.set_owner(owner_node)
	return room_instance
	
	
func new_exit(parent_node : Node,owner_node : Node,rand : RandomNumberGenerator) -> General_room:
	"""Instance a new aleatory exit"""
	var _rooms = get_exits()
	var room_instance : General_room = _rooms[rand.randi_range(0,len(_rooms)-1)].instance()
	parent_node.add_child(room_instance)
	room_instance.initialize()
	room_instance.set_owner(owner_node)
	return room_instance
	
	
func new_corridor(parent_node : Node,owner_node : Node,rand : RandomNumberGenerator) -> Corridor:
	"""Instance a new aleatory corridor"""
	var _corridors = get_corridors()
	var corridor_instance : Corridor = _corridors[rand.randi_range(0,len(_corridors)-1)].instance()
	parent_node.add_child(corridor_instance)
	corridor_instance.initialize()
	corridor_instance.set_owner(owner_node)
	
	corridor_instance.randomize_length(5,7)
	
	return corridor_instance
	
	
func get_entrances() -> Array:
	"""Get the posible entrances"""
	if entrances:
		return entrances
	return get_packed_scenes("res://prefabs/Dungeon/Rooms/Entrance/")


func get_rooms() -> Array:
	"""Get the posible rooms"""
	if rooms:
		return rooms
	return get_packed_scenes("res://prefabs/Dungeon/Rooms/Normal/")
	
	
func get_exits() -> Array:
	"""Get the posible Exits"""
	if entrances:
		return entrances
	return get_packed_scenes("res://prefabs/Dungeon/Rooms/Exit/")
	
	
func get_corridors() -> Array:
	"""Get the posible corridors"""
	if corridors:
		return corridors
	return get_packed_scenes("res://prefabs/Dungeon/Corridors/")


func get_packed_scenes(dir_path : String) -> Array:
	"""Get the packedscenes in the directory path"""
	var directory = Directory.new()
	var packed_scenes : Array = []
	
	directory.open(dir_path)
	directory.list_dir_begin()
	while true:
		var file = directory.get_next()
		if file == "":
			break
		elif not file.begins_with("."):
			packed_scenes.append(load(dir_path+file))
	return packed_scenes
