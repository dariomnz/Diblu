extends CanvasModulate

#onready var initial_light


# Valor que va de 0 a 1 para ver la luz del cielo
export var actual_light = 1.0 setget update_light

onready var timer_wait_time = $Timer.wait_time

var is_night = false

export var update_factor = 0.001


func _on_Timer_timeout():
	
	$Timer.wait_time = timer_wait_time
	if is_night:
		update_light( fmod((actual_light+update_factor) , 1.0 ))
		if actual_light >= 0.9:
#			print(is_day)
			is_night = false
			$Timer.wait_time = 10
	else:
		update_light( fmod((actual_light-update_factor) , 1.0 ))
		if actual_light <= 0.1:
#			print(is_day)
			is_night = true
			$Timer.wait_time = 10
		
	
func update_light(newLight):
	
	if newLight < 0.5:
		if (actual_light - newLight) < 0:
			newLight += update_factor*2
		else:
			newLight -= update_factor*2
			
#		newLight += (actual_light - newLight) + 0.05
	actual_light = newLight
#	print(actual_light)
	color = Color(actual_light,actual_light,actual_light,1.0)
	for light_source in get_tree().get_nodes_in_group("light"):
		light_source.actual_day_multiplayer = (1.1 - actual_light)
		light_source.energy = light_source.initial_energy * (1.1 - actual_light)
#		light_source.texture_scale = light_source.initial_texture_scale * (1.1 - actual_light)
