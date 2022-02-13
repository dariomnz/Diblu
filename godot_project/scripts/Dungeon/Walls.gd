tool
extends TileMap
class_name Walls

func set_cell(x: int, y: int, tile: int, flip_x: bool = false, flip_y: bool = false, transpose: bool = false, autotile_coord: Vector2 = Vector2( 0, 0 )):
	
	var wall_down=tile_set.find_tile_by_name("Wall_down")
	var wall_middle=tile_set.find_tile_by_name("Wall_middle")
	var wall_top=tile_set.find_tile_by_name("Wall_top")
	var wall_remove=tile_set.find_tile_by_name("Wall_remove")
	
	
	match tile:
		wall_down:
			set_cell(x,y-1,wall_middle)
			if get_cell(x,y) != wall_top and get_cell(x,y) != wall_middle:
				.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
		wall_middle:
			set_cell(x,y-1,wall_top)
			if get_cell(x,y) != wall_top:
				.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
		
		wall_top:
			.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
			update_bitmask_area(Vector2(x,y))
		
		wall_remove:
			if get_cell(x,y-2) == wall_top:
				.set_cell(x,y-2,-1)
				if get_cell(x,y-1) == wall_middle:
					.set_cell(x,y-1,-1)
				if get_cell(x,y) == wall_down:
					.set_cell(x,y,-1)
				
				if get_cell(x,y-3) == wall_top:
					set_cell(x,y-1,wall_down)
				if get_cell(x,y-3) == wall_middle:
					set_cell(x,y-2,wall_down)
					
				update_bitmask_area(Vector2(x,y-2))
		_:
			.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)

func set_cell_parent(x: int, y: int, tile: int, flip_x: bool = false, flip_y: bool = false, transpose: bool = false, autotile_coord: Vector2 = Vector2( 0, 0 )):
	.set_cell(x, y, tile, flip_x, flip_y, transpose, autotile_coord)
