tool
extends TileMap
class_name Dungeon_generator

signal upgrade_loading(percentage)

export(bool) var generate_new_dungeon setget generate_dungeon
export(int,3,50) var max_rooms = 10 
export(int,3,50) var min_rooms = 3 

export(Vector2) var wall_border :=Vector2(60,60)

export(Vector2) var start_position := Vector2(1000,1000)


var rand : = RandomNumberGenerator.new()

var last_room : General_room = null
var used_rects : Array = []
var next_trys : Array = []

var actual_rooms : Array = []
var total_rooms : Array = []


var num_rooms : int setget ,get_num_rooms

func _ready():
	generate_dungeon(true)
	
func generate_dungeon(can_generate):
	if not can_generate:
		return
	
	var start_time = OS.get_ticks_msec()
	
	#Clear the level
	for child in get_children():
		if child.name != "Walls":
			child.queue_free()
	
	var walls : Walls = $Walls
	walls.clear()
	
	rand.randomize()
	
	#Generate the rooms
	for _num_room in range(get_num_rooms()):
		
		generate_new_room()
		emit_signal("upgrade_loading",_num_room*1.0/num_rooms*0.4)
		yield(get_tree(), "idle_frame")
	
	var connect_exit = get_rooms_depth(int(get_max_depth()/2.0))
	
	while(true):
		last_room = connect_exit[rand.randi_range(0,len(connect_exit)-1)]
		if try_generate_new_room(get_rand_direction(),true):
			break
		
	generate_inter_corridors()
	
	#Calculate the rect for the dungeon walls
	var bucle_count = 0
	var total_rect : Rect2
	for used_rect in used_rects:
		if !total_rect:
			total_rect = used_rect
		total_rect = total_rect.merge(used_rect)
	
	#Fill the walls
	total_rect.position = world_to_map(total_rect.position)-wall_border
	total_rect.size = world_to_map(total_rect.size)+wall_border*2
	var total_bucle_count = total_rect.get_area()
	var step_to_upgrade_loading = int(total_rect.size.x*0.5)
	for x in range(total_rect.position.x,total_rect.position.x+total_rect.size.x):
		for y in range(total_rect.position.y,total_rect.position.y+total_rect.size.y):
			bucle_count +=1
			walls.set_cell_parent(x,y-2,walls.tile_set.find_tile_by_name("Wall_top"),false,false,false,Vector2.ONE)
			
		if x % step_to_upgrade_loading == 0:
			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.6)
			yield(get_tree(), "idle_frame")
			
#	walls.update_bitmask_region(total_rect.position,total_rect.position+total_rect.size)
	
	#Clear the external borders of the walls
#	bucle_count = 0
#	for x in range(total_rect.position.x,total_rect.position.x+total_rect.size.x):
#		for y in range(total_rect.position.y,total_rect.position.y+total_rect.size.y):
#			bucle_count += 1
#			if x==total_rect.position.x or x==total_rect.position.x+1 or x==total_rect.position.x+2\
#			 or x==total_rect.position.x+total_rect.size.x-1\
#			 or x==total_rect.position.x+total_rect.size.x-2\
#			 or x==total_rect.position.x+total_rect.size.x-3:
#				walls.set_cellv(Vector2(x,y),-1)
#			if y==total_rect.position.y or y==total_rect.position.y+1 or y==total_rect.position.y+2:
#				walls.set_cellv(Vector2(x,y-2),-1)
#				continue
#			if y==total_rect.position.y+total_rect.size.y-1\
#			 or y==total_rect.position.y+total_rect.size.y-2\
#			 or y==total_rect.position.y+total_rect.size.y-3:
#				walls.set_cellv(Vector2(x,y),-1)
#				continue
#
#		if x % step_to_upgrade_loading == 0:
#			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.6)
#			yield(get_tree(), "idle_frame")
	
	#Remove the walls for the rooms
	bucle_count = 0
	total_bucle_count = int(len(total_rooms)/4.0)
	for room in total_rooms:
		bucle_count +=1
		remove_walls(room)
		if bucle_count % 4 == 0:
			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.8)
			yield(get_tree(), "idle_frame")
	
	if get_tree().has_group("minimap"):
		get_tree().get_nodes_in_group("minimap")[0].create_rooms(total_rooms)
	
	#Clear the data used
	used_rects.clear()
	actual_rooms.clear()
	total_rooms.clear()
	last_room = null
	
	print("Time to generate ",num_rooms," rooms: ",OS.get_ticks_msec()-start_time," ms")
	

func generate_new_room():
	"""Generate a room"""
	var is_generate = false
	var tryed : Array = []
	while(not is_generate):
		
		var next_direction = get_rand_direction()
			
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
		
		if try_generate_new_room(next_direction):
			is_generate = true
	
	
func try_generate_new_room(direction : int,is_exit : bool = false) -> bool:
	"""Try generate to rooms whit the corridor"""
	if not direction in [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]:
		return false
	
	#determine the direction
	var from : int = direction
	var to : int = global_var.FROM_TO[from]
	var is_horizontal : bool = true
	
	if direction == global_var.UP or direction == global_var.DOWN:
		is_horizontal = false
	
	#This is when is the first room, the entrance
	if not last_room:
		last_room = DungeonDB.new_entrance(self,get_parent(),rand)
		last_room.global_position = start_position
	
	var last_posible_exits = last_room.posible_exits
	
	#Chek if the room has exits in direction
	if last_posible_exits[from].empty():
		return false
	
	var out_corridor_position = last_posible_exits[from][rand.randi_range(0,len(last_posible_exits[from])-1)]
	
	#Instance new corridor
	var corridor = DungeonDB.new_corridor(last_room,get_parent(),rand)
	if is_horizontal:
		corridor.direction = global_var.HORIZONTAL
	else:
		corridor.direction = global_var.VERTICAL
	
	#Put the corridor in the position from the room
	out_corridor_position = map_to_world(out_corridor_position)+last_room.global_position
	
	#Correcion for the corridor position
	out_corridor_position -= map_to_world(corridor.posible_exits[to][0])
	
	corridor.global_position = out_corridor_position
	
	#Instance new room
	var room : General_room
	if is_exit:
		room = DungeonDB.new_exit(last_room,get_parent(),rand)
	else:
		room = DungeonDB.new_room(last_room,get_parent(),rand)
	var posible_entrances = room.posible_exits

	#Adjustment for the entrance
	room.global_position = corridor.global_position + map_to_world(corridor.posible_exits[from][0])
		
	if posible_entrances[to].empty():
		room.free()
		corridor.free()
		return false
		
	var in_corridor_position = posible_entrances[to][rand.randi_range(0,len(posible_entrances[to])-1)]
	
	#Put the room in the position from the corridor
	in_corridor_position = map_to_world(in_corridor_position)
	
	room.global_position -= in_corridor_position
	
	#Check if is a space without use
	var room_used_flor = room.used_floor
	for used_rect in used_rects:
		if room_used_flor.intersects(used_rect):
			room.free()
			corridor.free()
			return false
	
	
	corridor.free()
	#Append data for the rect to check collisions and create the walls
	if not last_room.used_floor in used_rects:
		used_rects.append(last_room.used_floor)
#	if not corridor.used_floor in used_rects:
#		used_rects.append(corridor.used_floor)
	if not room.used_floor in used_rects:
		used_rects.append(room.used_floor)
	
	#Append data for the trys of the rooms
	if not last_room in actual_rooms:
		actual_rooms.append(last_room)
	if not room in actual_rooms:
		actual_rooms.append(room)
		
	#Append data for clear the walls of the room
	if not last_room in total_rooms:
		total_rooms.append(last_room)
#	if not corridor in total_rooms:
#		total_rooms.append(corridor)
	if not room in total_rooms:
		total_rooms.append(room)
		
	return true
	
	
func remove_walls(room : General_room):
	"""Remove the walls that currently are in the floor of the room"""
	var room_position = world_to_map(room.global_position)
	var walls_arr = room.get_floor_arr()
	var walls = $Walls
	for wall in walls_arr:
		walls.set_cell(room_position.x+wall.x,room_position.y+wall.y,walls.tile_set.find_tile_by_name("Wall_remove"))
	
	



func get_rand_direction() -> int:
	"""Return a aleatory direction"""
	var posible_direction = [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]
	return posible_direction[rand.randi_range(0,len(posible_direction)-1)]


func get_num_rooms() -> int:
	if not num_rooms or Engine.editor_hint:
		num_rooms = rand.randi_range(min_rooms,max_rooms)
	return num_rooms
	
	
func get_rooms_depth(more_than : int) -> Array:
	"""Return a array with the rooms that are more_than the enter of the dungeon"""
	var _rooms : Array = []
	_get_rooms_depth(self,0,more_than,_rooms)
	return _rooms
	

func _get_rooms_depth(root : Node,actual_depth : int,more_than : int,rooms_arr : Array):
	"""Recursive method of get_rooms_depth"""
	for child in root.get_children():
		if "Room" in child.name:
			if actual_depth > more_than:
				rooms_arr.append(child)
			_get_rooms_depth(child,actual_depth+1,more_than,rooms_arr)
		elif "Corridor" in child.name:
			_get_rooms_depth(child,actual_depth,more_than,rooms_arr)
	
func get_max_depth() -> int:
	"""Return the maximun depth in the dungeon"""
	return _get_max_depth(self,0)
	
	
func _get_max_depth(root : Node,actual_depth : int):
	"""Recursive method of get_max_depth"""
	for child in root.get_children():
		if "Room" in child.name:
			return _get_max_depth(child,actual_depth+1)
		elif "Corridor" in child.name:
			return _get_max_depth(child,actual_depth)
	return actual_depth

func get_posible_corridors() -> Array:
	#Formato posible_corridor es un array con posicion de entrada y salida
	var posible_corridor : Array = []
	var max_corridor_legth = 12 * $Walls.cell_size.x
	for room1 in total_rooms:
		if not "Room" in room1.name:
			continue
		for room2 in total_rooms:
			if (not "Room" in room2.name) or room1 == room2:
				continue
			var room1_posible_exits : Array = room1.posible_exits
			var room2_posible_exits : Array = room2.posible_exits
			
			
			for direction in global_var.directions.values():
				var from = direction
				var to = global_var.FROM_TO[from]
				var is_find = false
				room1_posible_exits[from].shuffle()
				for _posible_room1_corridor in room1_posible_exits[from]:
					room2_posible_exits[to].shuffle()
					var _map_posible_room1_corridor = map_to_world(_posible_room1_corridor) + room1.global_position
					for _posible_room2_corridor in room2_posible_exits[to]:
						var _map_posible_room2_corridor = map_to_world(_posible_room2_corridor) + room2.global_position
						if from == global_var.UP or from == global_var.DOWN:
							if _map_posible_room1_corridor.x == _map_posible_room2_corridor.x and \
							abs(_map_posible_room1_corridor.y - _map_posible_room2_corridor.y) <= max_corridor_legth:
								posible_corridor.append([from,_map_posible_room1_corridor,_map_posible_room2_corridor])
								is_find = true
								break
						else:
							if _map_posible_room1_corridor.y == _map_posible_room2_corridor.y and \
							abs(_map_posible_room1_corridor.x - _map_posible_room2_corridor.x) <= max_corridor_legth:
								posible_corridor.append([from,_map_posible_room1_corridor,_map_posible_room2_corridor])
								is_find = true
								break
					if is_find:
						break
	return posible_corridor

func generate_inter_corridors():
	var posible_corridor = get_posible_corridors()
	var walls = $Walls
	var bucle_count = 0
	var total_bucle_count = len(posible_corridor)
	for _posible_corridor in posible_corridor:
		bucle_count += 1
		if bucle_count % 4 == 0:
			emit_signal("upgrade_loading",bucle_count*1.0/total_bucle_count*0.2+0.4)
			yield(get_tree(), "idle_frame")
		var from = _posible_corridor[0]
		var position1 = _posible_corridor[1]
		var position2 = _posible_corridor[2]
		var is_horizontal : bool = true
		
		if from == global_var.UP or from == global_var.DOWN:
			is_horizontal = false
			
		var corridor = DungeonDB.new_corridor(self,get_parent(),rand)
		corridor.corridor_length = abs(((position2-position1)/walls.cell_size).length())
		if is_horizontal:
			corridor.direction = global_var.HORIZONTAL
		else:
			corridor.direction = global_var.VERTICAL
		var out_corridor_position
		match from:
			global_var.UP:
				out_corridor_position = position1
			global_var.DOWN:
				out_corridor_position = position2
			global_var.LEFT:
				out_corridor_position = position1
			global_var.RIGHT:
				out_corridor_position = position2
		
		out_corridor_position -= map_to_world(corridor.posible_exits[from][0])
		out_corridor_position += walls.cell_size
	
		corridor.global_position = out_corridor_position
		
		var corridor_used_floor = corridor.used_floor
		var must_continue = false
		for used_rect in used_rects:
			if corridor_used_floor.intersects(used_rect):
				corridor.free()
				must_continue = true
				break
		if must_continue:
			continue

		if not corridor.used_floor in used_rects:
			used_rects.append(corridor.used_floor)

		if not corridor in total_rooms:
			total_rooms.append(corridor)
		









