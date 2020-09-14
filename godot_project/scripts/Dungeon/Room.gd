tool
extends General_room
class_name Room


	
#
#func update_walls_corridor(corridor_direction : int,corridor_position : Vector2, corridor_size : int):
#	"""The corridor_position must be a tilemap position"""
#	return
#
#	#Adjustment because corridor_position is center in the corridor
#	var adjustment = int(corridor_size/2.0)+1
#	match corridor_direction:
#			global_var.UP:
#				corridor_position.x-=adjustment-1
#				corridor_position.y-=1
#			global_var.DOWN:
#				corridor_position.x-=adjustment-1
#				corridor_position.y+=1
#			global_var.RIGHT:
#				corridor_position.y-=adjustment
#			global_var.LEFT:
#				corridor_position.y-=adjustment
#
#	for num in range(corridor_size+1):
#		if num !=0:
#			match corridor_direction:
#				global_var.UP:
#					if num != corridor_size:
#						corridor_position.x+=1
#				global_var.DOWN:
#					if num != corridor_size:
#						corridor_position.x+=1
#				global_var.RIGHT:
#					corridor_position.y+=1
#				global_var.LEFT:
#					corridor_position.y+=1
#
#		$Walls.set_cell(corridor_position.x,corridor_position.y,-1)
#
#
