extends Item_hand

var can_shoot = true
var can_charge_shoot = true

func action(number: int):
	
	match number:
		1:
			if not can_shoot:
				return
		2:
			if not can_charge_shoot:
				return
				
	var animation_name = "action"+str(number)
	if actionPlayer.has_animation(animation_name) and not actionPlayer.is_playing():
		actionPlayer.play(animation_name)
		
		if has_method(animation_name):
			call(animation_name)
		
		
		
func create_water_projectile1():
	restart_shoot_delay()
	player.create_water_projectile($ChargingParticles.global_position,10)
	
func create_water_projectile2():
	restart_charge_shoot_delay()
	player.create_water_projectile($ChargingParticles.global_position,25)

func restart_shoot_delay():
	can_shoot = false
	$Shoot_delay.start()

func restart_charge_shoot_delay():
	can_charge_shoot = false
	$Charge_shoot_delay.start()
	

func _on_Shoot_delay_timeout():
	can_shoot = true
	
func _on_Charge_shoot_delay_timeout():
	can_charge_shoot = true
