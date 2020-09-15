tool
extends TileMap
class_name Dungeon_generator

signal upgrade_loading(percentage)

#var rooms = [
#	preload("res://prefabs/Dungeon/Rooms/Room1.tscn")
#]
#
#var corridors = [
#	preload("res://prefabs/Dungeon/Corridor/Corridor1.tscn")
#]

export(bool) var generate_new_dungeon setget generate_dungeon
export(int,3,50) var max_rooms = 10 
export(int,3,50) var min_rooms = 3 

export(Vector2) var wall_border :=Vector2(60,60)

export(Vector2) var start_position := Vector2(1000,1000)


var rand : = RandomNumberGenerator.new()

var entrances : Array setget ,get_entrances
var rooms : Array setget ,get_rooms
var corridors : Array setget ,get_corridors

var last_room : General_room = null
var used_rects : Array = []
var next_trys : Array = []

var actual_rooms : Array = []
var total_rooms : Array = []


var num_rooms : int setget ,get_num_rooms

#var try_number = 0

func _ready():
#	global_position = start_position
	generate_dungeon(true)
	
	
	
	
	
func generate_dungeon(can_generate):
	if not can_generate:
		return
	
	
	var start_time = OS.get_ticks_msec()
	
	#Clear the level
	for child in get_children():
		if child.name != "Walls":
			child.queue_free()
	
	$Walls.clear()
#
#	for x in range(-20,20):
#		for y in range(-20,20):
#			$Walls.set_cell(x,y,$Walls.tile_set.find_tile_by_name("Wall_down"))
#			$Walls.update_bitmask_area(Vector2(x,y))
	
	rand.randomize()
	
	

	for _num_room in range(get_num_rooms()):
		
		try_generate_new_room()
		emit_signal("upgrade_loading",_num_room*1.0/num_rooms*0.4)
		yield(get_tree(), "idle_frame")
#		var next_direction = rand.randi_range(0,3)
#
#		next_trys = [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]
#
#		next_trys.erase(next_direction)
#		if generate(next_direction) == -1:
#			break
		
#		if not actual_rooms.empty():
#			last_room = actual_rooms[rand.randi_range(0,len(actual_rooms)-1)]
#		if Engine.editor_hint:
#			yield(get_tree().create_timer(0.2),"timeout")
		
#	for direction in [global_var.UP,global_var.LEFT,global_var.UP,global_var.RIGHT,global_var.RIGHT,global_var.RIGHT,global_var.DOWN,global_var.DOWN]:
#		generate(direction)
#	print("try_number  ",try_number)
#	try_number = 0
	var bucle_count = 0
	var total_rect : Rect2
	for used_rect in used_rects:
		if !total_rect:
			total_rect = used_rect
		total_rect = total_rect.merge(used_rect)

	total_rect.position = world_to_map(total_rect.position)-wall_border
	total_rect.size = world_to_map(total_rect.size)+wall_border*2
	var total_bucle_count = total_rect.get_area()
	var step_to_upgrade_loading = int(total_rect.size.x*0.5)
	for x in range(total_rect.position.x,total_rect.position.x+total_rect.size.x):
		for y in range(total_rect.position.y,total_rect.position.y+total_rect.size.y):
			bucle_count +=1
			$Walls.set_cellv(Vector2(x,y-2),$Walls.tile_set.find_tile_by_name("Wall_top"))
#			$Walls.set_cell(x,y,$Walls.tile_set.find_tile_by_name("Wall_down"))
			$Walls.update_bitmask_area(Vector2(x,y-2))
			
		if x % step_to_upgrade_loading == 0:
			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.4)
			yield(get_tree(), "idle_frame")
			
			
#	for used_rect in used_rects:
#
#		used_rect.position = world_to_map(used_rect.position)-wall_border
#		used_rect.size = world_to_map(used_rect.size)+wall_border*2
#		for x in range(used_rect.position.x,used_rect.position.x+used_rect.size.x):
#			for y in range(used_rect.position.y,used_rect.position.y+used_rect.size.y):
#				bucle_count+=1;
#				if get_cell(x,y-2) != $Walls.tile_set.find_tile_by_name("Wall_top"):
#					$Walls.set_cell(x,y,$Walls.tile_set.find_tile_by_name("Wall_down"))
#					$Walls.update_bitmask_area(Vector2(x,y))
#					iterations_count+=1;
			

	
	bucle_count = 0
	for x in range(total_rect.position.x,total_rect.position.x+total_rect.size.x):
		for y in range(total_rect.position.y,total_rect.position.y+total_rect.size.y):
			bucle_count += 1
			if x==total_rect.position.x or x==total_rect.position.x+1 or x==total_rect.position.x+2\
			 or x==total_rect.position.x+total_rect.size.x-1\
			 or x==total_rect.position.x+total_rect.size.x-2\
			 or x==total_rect.position.x+total_rect.size.x-3:
				$Walls.set_cellv(Vector2(x,y),-1)
			if y==total_rect.position.y or y==total_rect.position.y+1 or y==total_rect.position.y+2:
				$Walls.set_cellv(Vector2(x,y-2),-1)
				continue
			if y==total_rect.position.y+total_rect.size.y-1\
			 or y==total_rect.position.y+total_rect.size.y-2\
			 or y==total_rect.position.y+total_rect.size.y-3:
				$Walls.set_cellv(Vector2(x,y),-1)
				continue
			
		if x % step_to_upgrade_loading == 0:
			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.6)
			yield(get_tree(), "idle_frame")

#	print("iteracions  ",iterations_count, "bucle   ",bucle_count)
	bucle_count = 0
	total_bucle_count = len(total_rooms)
	for room in total_rooms:
		bucle_count +=1
		remove_walls(room)
		emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.8)
		yield(get_tree(), "idle_frame")
#	print(total_rect.size)
	
	used_rects.clear()
	actual_rooms.clear()
	total_rooms.clear()
	last_room = null
	
	print("Time to generate ",num_rooms," rooms: ",OS.get_ticks_msec()-start_time," ms")

func try_generate_new_room():
	var is_generate = false
	var tryed : Array = []
	while(not is_generate):
	
		var posible_direction = [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]
		
		var next_direction = posible_direction[rand.randi_range(0,len(posible_direction)-1)]
			
		
		if not actual_rooms.empty():
			var is_choose = false
			while(not is_choose):
				last_room = actual_rooms[rand.randi_range(0,len(actual_rooms)-1)]
				
				if not last_room in tryed:
					is_choose = true
				elif not tryed.empty():
					tryed.append(last_room)
				elif len(tryed) >= len(actual_rooms):
					tryed.clear()
				
			
	#	next_trys = [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]
		
	#	next_trys.erase(next_direction)
		
		if generate_new_room(next_direction) != -1:
			is_generate = true
	#		if not actual_rooms.empty():
	#			last_room = actual_rooms[rand.randi_range(0,len(actual_rooms)-1)]
#			try_generate_new_room()
	
func generate_new_room(direction : int) -> int:
	"""Generate to rooms whit the corridor"""
	if not direction in [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]:
		return -1
		
#	try_number +=1
	var from : int
	var to : int
	var is_horizontal : bool = true
	
	match direction:
		global_var.UP:
			from = global_var.UP
			to = global_var.DOWN
			is_horizontal = false
		global_var.DOWN:
			from = global_var.DOWN
			to = global_var.UP
			is_horizontal = false
		global_var.LEFT:
			from = global_var.LEFT
			to = global_var.RIGHT
		global_var.RIGHT:
			from = global_var.RIGHT
			to = global_var.LEFT
	
	#This is when is the first room, the entrance
	if not last_room:
		last_room = new_entrance(self)
		last_room.global_position = start_position
		
	var last_posible_exits = last_room.posible_exits
	
	if last_posible_exits[from].empty():
		return -1
	
	var out_corridor_position = last_posible_exits[from][rand.randi_range(0,len(last_posible_exits[from])-1)]
	
	var corridor := new_corridor(last_room)
	if is_horizontal:
		corridor.direction = global_var.HORIZONTAL
	else:
		corridor.direction = global_var.VERTICAL
		
	#Update the walls of the Room
#	var out_clear_position = out_corridor_position
#	last_room.update_walls_corridor(from,out_corridor_position,corridor.corridor_width)
	
	#Put the corridor in the position from the room
	out_corridor_position = map_to_world(out_corridor_position)+last_room.global_position
	
	#Correcion for the corridor position
	out_corridor_position -= map_to_world(corridor.posible_exits[to][0])
	
	corridor.global_position = out_corridor_position
	
	var room : Room = new_room(corridor)
	var posible_entrances = room.posible_exits

	#Adjustment for the entrance
	room.global_position = corridor.global_position + map_to_world(corridor.posible_exits[from][0])
		
	if posible_entrances[to].empty():
		room.free()
		corridor.free()
		return -1
		
	var in_corridor_position = posible_entrances[to][rand.randi_range(0,len(posible_entrances[to])-1)]
	
#	var in_clear_position = in_corridor_position
	#Update the walls of the Room
#	room.update_walls_corridor(to,in_corridor_position,corridor.corridor_width)
	
	#Put the room in the position from the corridor
	in_corridor_position = map_to_world(in_corridor_position)
	
	room.global_position -= in_corridor_position
	
	
#	print(used_rects)
	#Check if is a space without use
	var room_used_flor = room.used_floor
	for used_rect in used_rects:
		if room_used_flor.intersects(used_rect):
#			if next_trys.empty():
#				corridor.free()
#				room.free()
#				return -1
#			var next_direction = next_trys[rand.randi_range(0,len(next_trys)-1)]
			
#			next_trys.erase(next_direction) 
#			var _err = generate(next_direction)
			room.free()
			corridor.free()
#			print(room)
			return -1
	
	
	#Update the walls of the Room
#	last_room.update_walls_corridor(from,out_clear_position,corridor.corridor_width)
	
	#Update the walls of the Room
#	room.update_walls_corridor(to,in_clear_position,corridor.corridor_width)
	
	
	if not last_room.used_floor in used_rects:
		used_rects.append(last_room.used_floor)
	if not corridor.used_floor in used_rects:
		used_rects.append(corridor.used_floor)
	if not room.used_floor in used_rects:
		used_rects.append(room.used_floor)
	
	
	if not last_room in actual_rooms:
		actual_rooms.append(last_room)
	if not room in actual_rooms:
		actual_rooms.append(room)
		
		
	if not last_room in total_rooms:
		total_rooms.append(last_room)
	if not corridor in total_rooms:
		total_rooms.append(corridor)
	if not room in total_rooms:
		total_rooms.append(room)
		
		
	return 0
	
func remove_walls(room : General_room):
	var room_position = world_to_map(room.global_position)
	var walls_arr = room.get_floor_arr()
	for wall in walls_arr:
		$Walls.set_cell(room_position.x+wall.x,room_position.y+wall.y,$Walls.tile_set.find_tile_by_name("Wall_remove"))
	
func new_entrance(parent_node : Node) -> General_room:
	var _rooms = get_entrances()
	var room_instance : General_room = _rooms[rand.randi_range(0,len(_rooms)-1)].instance()
	parent_node.add_child(room_instance)
	room_instance.initialize()
	room_instance.set_owner(get_parent())
	return room_instance
	
func new_room(parent_node : Node) -> General_room:
	var _rooms = get_rooms()
	var room_instance : General_room = _rooms[rand.randi_range(0,len(_rooms)-1)].instance()
	parent_node.add_child(room_instance)
	room_instance.initialize()
	room_instance.set_owner(get_parent())
	return room_instance
	
	
func new_corridor(parent_node : Node) -> Corridor:
	var _corridors = get_corridors()
	var corridor_instance : Corridor = _corridors[rand.randi_range(0,len(_corridors)-1)].instance()
#		corridor_instance.global_position = Vector2(rand.randi()%1000,rand.randi()%600)
	parent_node.add_child(corridor_instance)
	corridor_instance.initialize()
	corridor_instance.set_owner(get_parent())
	
	corridor_instance.randomize_length(7)
	
	return corridor_instance
	
	
func get_entrances() -> Array:
	if entrances:
		return entrances
	return get_packed_scenes("res://prefabs/Dungeon/Rooms/Entrance/")

func get_rooms() -> Array:
	if rooms:
		return rooms
	return get_packed_scenes("res://prefabs/Dungeon/Rooms/Normal/")
		
	
#	var directory = Directory.new()
#	var dir_path = "res://prefabs/Dungeon/Rooms/Normal/"
#	var rooms_scenes : Array = []
#
#	directory.open(dir_path)
#	directory.list_dir_begin()
#	while true:
#		var file = directory.get_next()
#		if file == "":
#			break
#		elif not file.begins_with("."):
#			rooms_scenes.append(load(dir_path+file))
#	rooms = rooms_scenes
#	return rooms
	
func get_corridors() -> Array:
	if corridors:
		return corridors
	return get_packed_scenes("res://prefabs/Dungeon/Corridors/")
#	var directory = Directory.new()
#	var dir_path = "res://prefabs/Dungeon/Corridors/"
#	var corridors_scenes : Array = []
#
#	directory.open(dir_path)
#	directory.list_dir_begin()
#	while true:
#		var file = directory.get_next()
#		if file == "":
#			break
#		elif not file.begins_with("."):
#			corridors_scenes.append(load(dir_path+file))
#	corridors = corridors_scenes
#	return corridors

func get_packed_scenes(dir_path : String) -> Array:
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

func get_num_rooms() -> int:
	if not num_rooms or Engine.editor_hint:
		num_rooms = rand.randi_range(min_rooms,max_rooms)
	return num_rooms
