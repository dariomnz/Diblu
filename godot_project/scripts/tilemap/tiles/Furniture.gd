extends Node2D
class_name Furniture

signal destroy(furniture)


var id : String setget set_id,get_id
var chunk_position : Vector2 = Vector2.ZERO

var max_health = 5
var health = max_health

func destroy():
	emit_signal("destroy",self)
	queue_free()

func set_id(newID):
	id = newID
	
	var arrPos = id.split(",")
	
	position = Vector2(int(arrPos[0]),int(arrPos[1])) + chunk_position

func get_id():
	return str(position.x)+","+str(position.y)
	
func _on_Regen_timer_timeout():
	if health < max_health:
		$Regen_timer.start()
		health += 1
