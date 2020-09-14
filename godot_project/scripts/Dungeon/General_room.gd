tool
extends TileMap
class_name General_room


var posible_exits : Array setget ,get_posible_exits

var used_floor : Rect2 setget ,get_floor_rect

#func _ready():
#	$Exits.visible = false
#	$Walls.clear()

func initialize():
	$Exits.visible = false
	$Walls.clear()

func get_posible_exits() -> Array:
	var exit_array : Array = [global_var.UP,global_var.DOWN,global_var.LEFT,global_var.RIGHT]
	
	for direction in exit_array:
		var current_posible_exits : TileMap
		match direction:
			global_var.UP:
				current_posible_exits = $Exits/Up
			global_var.DOWN:
				current_posible_exits = $Exits/Down
			global_var.LEFT:
				current_posible_exits = $Exits/Left
			global_var.RIGHT:
				current_posible_exits = $Exits/Right
				
		exit_array[direction] = current_posible_exits.get_used_cells()
	
	return exit_array

func get_floor_rect() -> Rect2:
	var _used_floor = $Floor.get_used_rect()
	_used_floor.position *= cell_size
	_used_floor.size *= cell_size
#	print(_used_floor)
	_used_floor.position += global_position
#	print(_used_floor)
	return _used_floor
	

func get_floor_arr() -> Array:
	return $Floor.get_used_cells()
