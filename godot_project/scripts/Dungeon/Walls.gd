tool
extends TileMap


func set_cell(x: int, y: int, tile: int, flip_x: bool = false, flip_y: bool = false, transpose: bool = false, autotile_coord: Vector2 = Vector2( 0, 0 )):
	
	
#	if tile == tile_set.find_tile_by_name("Wall_down2"):
#		if get_cell(x,y-1) == -1 or tile_set.find_tile_by_name("Wall_down2"):
#			set_cell(x,y-1,tile_set.find_tile_by_name("Wall_down1"))
#		if get_cell(x,y-2) == -1 or tile_set.find_tile_by_name("Wall_down1")or tile_set.find_tile_by_name("Wall_down2"):
#			set_cell(x,y-2,tile_set.find_tile_by_name("Wall"))
#	set_cellv(Vector2(x,y),-1)
	
	if tile == tile_set.find_tile_by_name("Wall_down"):
		set_cell(x,y-1,tile_set.find_tile_by_name("Wall_middle"))
		if get_cell(x,y) != tile_set.find_tile_by_name("Wall_top") and get_cell(x,y) != tile_set.find_tile_by_name("Wall_middle"):
			.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
		
	elif tile == tile_set.find_tile_by_name("Wall_middle"):
		set_cell(x,y-1,tile_set.find_tile_by_name("Wall_top"))
		if get_cell(x,y) != tile_set.find_tile_by_name("Wall_top"):
			.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
		
	elif tile == tile_set.find_tile_by_name("Wall_top"):
		.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
		update_bitmask_area(Vector2(x,y))
		
	
	elif tile == tile_set.find_tile_by_name("Wall_remove"):
		if get_cell(x,y-2) == tile_set.find_tile_by_name("Wall_top"):
			.set_cell(x,y-2,-1)
			if get_cell(x,y-1) == tile_set.find_tile_by_name("Wall_middle"):
				.set_cell(x,y-1,-1)
			if get_cell(x,y) == tile_set.find_tile_by_name("Wall_down"):
				.set_cell(x,y,-1)
			
			if get_cell(x,y-3) == tile_set.find_tile_by_name("Wall_top"):
				set_cell(x,y-1,tile_set.find_tile_by_name("Wall_down"))
			if get_cell(x,y-3) == tile_set.find_tile_by_name("Wall_middle"):
				set_cell(x,y-2,tile_set.find_tile_by_name("Wall_down"))
				
			update_bitmask_area(Vector2(x,y-2))
#			if get_cell(x,y-1) == tile_set.find_tile_by_name("Wall_middle"):
#				.set_cell(x,y-1,-1)
#			else:
#				.set_cell(x,y,tile_set.find_tile_by_name("Wall_top"))
	else:
		.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
