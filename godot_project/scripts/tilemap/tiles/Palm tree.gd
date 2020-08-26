extends "res://scripts/tilemap/tiles/Tall_tile.gd"


func _ready():
	posible_tiles= {
	1:[0,304,48,64],
	2:[48,304,48,64],
	3:[0,368,48,64],
	4:[48,368,48,64],
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

