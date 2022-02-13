extends "res://scripts/tilemap/tiles/Tall_tile.gd"


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

#var trees = {
#	1:[48,224,32,48],
#	2:[80,224,32,48],
#	3:[112,224,32,48],
#}
# Called when the node enters the scene tree for the first time.
func _ready():
	posible_tiles= {
	1:[48,224,32,48],
	2:[80,224,32,48],
	3:[112,224,32,48],
}
	parent_ready()
	

func _hit(_body):
	
	global.create_float_text(self,1)
	
	$AnimationPlayer.play("hit")
	if randi()%100<10:
		spawn_loot()
		
func spawn_loot():
	var rand_offset = Vector2(0,randi()%10-20)
	
	if randi()%100 <30:
		global.spawn_item(position+rand_offset,"log")
	else:
		global.spawn_item(position+rand_offset,"leaf")
	
	if randi()%100 <50:
		global.spawn_item(position+rand_offset,"red_apple")
	else:
		global.spawn_item(position+rand_offset,"green_apple")

