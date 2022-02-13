extends "res://scripts/tilemap/tiles/Furniture.gd"


func _hit(_hitter):
	
	health -= 1
	$Regen_timer.start()
	
	if health == 0:
		destroy()

func destroy():
	.destroy()
	
	global.spawn_item(position,"campfire")
	
func change_animation():
	var nextAnimation = "idle"+str(randi()%3+1)
	$AnimationPlayer.stop()
	$AnimationPlayer.play(nextAnimation)
	
