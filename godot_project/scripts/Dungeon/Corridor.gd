tool
extends General_room
class_name Corridor

export(int,3,10) var corridor_width setget set_corridor_width
export(int,3,100) var corridor_length = 1 setget set_corridor_length

export(int,FLAGS,"Horizontal","Vertical") var direction = global_var.HORIZONTAL setget set_direction

func _ready():
	update_size()
#	._ready()

func randomize_length(max_value):
	var rand = RandomNumberGenerator.new()
	rand.randomize()
	
	corridor_length = rand.randi_range(3,max_value)
	update_size()
	if has_node("Walls"):
		$Walls.clear()

func set_corridor_width(new_corridor_width) -> void:
	if new_corridor_width == corridor_width:
		return
	corridor_width = new_corridor_width
	update_size()
	if has_node("Walls"):
		$Walls.clear()

func set_corridor_length(new_corridor_length) -> void:
	if new_corridor_length == corridor_length:
		return
	corridor_length = new_corridor_length
	update_size()
	if has_node("Walls"):
		$Walls.clear()
	
func set_direction(new_direction) -> void:
	if new_direction == direction:
		return
	if not new_direction in [global_var.HORIZONTAL,global_var.VERTICAL]:
		if direction == global_var.HORIZONTAL:
			direction = global_var.VERTICAL
		else:
			direction = global_var.HORIZONTAL
	else:
		direction = new_direction
	update_size()
	if has_node("Walls"):
		$Walls.clear()
	
func update_size() -> void:
	if not (has_node("Walls") and has_node("Floor") and has_node("Exits/Up") and has_node("Exits/Down") and has_node("Exits/Left") and has_node("Exits/Right")):
		return
	$Walls.clear()
	$Floor.clear()
	$Exits/Up.clear()
	$Exits/Down.clear()
	$Exits/Left.clear()
	$Exits/Right.clear()
	
	var floor_tile_idx = $Floor.tile_set.find_tile_by_name("Floor_atlas")
	var walls_tile_idx = $Walls.tile_set.find_tile_by_name("Wall_down")
	match direction:
		global_var.HORIZONTAL:
			for x in corridor_length+2:
				for y in corridor_width:
					#Update for the walls
					if x!=0 and x!=corridor_length+1:
						if y==0:
							$Walls.set_cell(x,y,walls_tile_idx)
						if y == corridor_width-1:
							$Walls.set_cell(x,y+1,walls_tile_idx)
					
					#Update fot the floor
					if y != 0 and x != 0 and x != corridor_length+1 and y!=corridor_width-1:
						$Floor.set_cell(x,y,floor_tile_idx)
						$Floor.update_bitmask_area(Vector2(x,y))
						
					#Update for exits
					if y==stepify(corridor_width/2.0,1.0):
						if x==0:
							$Exits/Left.set_cell(x,y-1,0)
						elif x == corridor_length+1:
							$Exits/Right.set_cell(x,y-1,0)
							
		global_var.VERTICAL:
			for x in corridor_width:
				for y in corridor_length+1:
					#Update for the walls
					if y!=0:
						if x==0 or x == corridor_width-1:
							$Walls.set_cell(x,y,walls_tile_idx)
					
					#Update fot the floor
					if y != 0 and x != 0 and x != corridor_width-1:
						$Floor.set_cell(x,y,floor_tile_idx)
						$Floor.update_bitmask_area(Vector2(x,y))
						
					#Update for exits
					if x==corridor_width/2:
						if y==0:
							$Exits/Up.set_cell(x,y,0)
						elif y == corridor_length:
							$Exits/Down.set_cell(x,y+1,0)
						
	
	
