tool
extends Control


func create_rooms(total_rooms : Array):
	for room in total_rooms:
		create_room(room)
			
func create_room(room : General_room):
	var minimap : TileMap = $Minimap
	var room_position = minimap.world_to_map(room.global_position)
	var walls_arr = room.get_floor_arr()
	for wall in walls_arr:
		var x = room_position.x+wall.x
		var y = room_position.y+wall.y
		minimap.set_cell(x,y,minimap.tile_set.find_tile_by_name("Floor"))
		minimap.update_bitmask_area(Vector2(x,y))
			
func get_camera_path():
	return $Camera2D.get_path()
