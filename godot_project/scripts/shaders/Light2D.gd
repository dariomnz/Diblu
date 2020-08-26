extends Light2D

export(float) var initial_energy setget update_energy 
export(float) var initial_texture_scale setget update_texture_scale

var actual_day_multiplayer = 1.0

func _ready():
	initial_energy = energy
	initial_texture_scale = texture_scale
	
	
func update_energy(newEnergy):
	initial_energy = newEnergy
	energy = initial_energy * actual_day_multiplayer
	
func update_texture_scale(newTexture_scale):
	initial_texture_scale = newTexture_scale
	texture_scale = initial_texture_scale * actual_day_multiplayer

