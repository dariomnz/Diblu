extends AnimationPlayer

# Override
# States que hacen seek entre ellos
var states_seek : = {}
# Override
# Nodes que pueden pasar de uno a otro
var nodes : = {}

# Override
# Direcciones posibles de la animacion 4 o 2
var posible_directions : = 4

func _ready():
	var _err = connect("animation_finished",self,"animation_ended")
#	travel("idle")


var current_state = null

var current_node = "idle"

var anim_direction : String = "_front"

var current_velocity = Vector2(0,0) setget update_direction

func travel(animation_name : String,forced = false):
	if animation_name in nodes[current_node] or forced:
		
		current_node = animation_name
		
#		update_direction()
		
		_set_animation(current_node,anim_direction,forced)

	
func update_direction(newDirection):
	if current_velocity != newDirection:
		current_velocity = newDirection
		match(posible_directions):
			4:
				if abs(current_velocity.x )> abs(current_velocity.y):
					if current_velocity.x >= 0:
						anim_direction = "_right"
					else:
						anim_direction = "_left"
				else:
					if current_velocity.y >= 0:
						anim_direction = "_front"
					else:
						anim_direction = "_back"
			2:
				if current_velocity.x >= 0:
					anim_direction = "_right"
				else:
					anim_direction = "_left"
#	_set_animation(current_node + anim_direction)
	
	
func _set_animation(animation_name,animation_direction,forced = false):
#	if animation_name == current_state:
#		print ("AnimationPlayer_Manager.gd -- WARNING: animation is already ", animation_name)
#		return true
	var seek_time = 0
	if has_animation(animation_name+animation_direction):
		if current_state != null:
			
			if forced:
				current_state = animation_name
				play(animation_name+animation_direction, -1)
				if seek_time!=0:
					seek(seek_time)
				return true
				
			if current_state+anim_direction != animation_name+animation_direction:
				if current_state in states_seek and animation_name in states_seek[current_state]:
					seek_time=current_animation_position
			else:
				return false
				
			var possible_animations = nodes[current_node]
			
			if animation_name in possible_animations:
				current_state = animation_name
				play(animation_name+animation_direction, -1)
				if seek_time!=0:
					seek(seek_time)
				return true
			else:
				print ("AnimationPlayer_Manager.gd -- WARNING: Cannot change to ", animation_name, " from ", current_state)
				return false
		else:
			current_state = animation_name
			play(animation_name+animation_direction, -1)
			if seek_time!=0:
				seek(seek_time)
			return true
	return false


# Override
# Define a donde pasa cuando cambia
func animation_ended(anim_name : String):
	
	anim_name = anim_name.split("_")[0]
	
	if anim_name == "idle":
		travel("idle",true)
