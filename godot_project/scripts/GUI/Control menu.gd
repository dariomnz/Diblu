extends Control
class_name Menu_control
"""

"""


var out_rect_position : = Vector2(-600,-1024) setget set_out_rect_position

const NONE = "NONE"
const PAUSE = "PAUSE"
const SETTINGS = "SETTINGS"

var actual_menu = NONE



func _unhandled_input(_event):
	if Input.is_action_just_pressed("ui_cancel"):
		if get_tree().paused == true:
			get_tree().paused = false
			travel(NONE)
		else:
			get_tree().paused = true
			travel(PAUSE)




func travel(newMenu):
	var newAnimation = actual_menu + "->" + newMenu
	if $AnimationPlayer.has_animation(newAnimation):
		$AnimationPlayer.play(newAnimation)
		actual_menu = newMenu

func _on_Control_menu_resized():
	
	set_out_rect_position(get_viewport_rect().size)

func set_out_rect_position(newValue):
	out_rect_position = newValue
	
	for animation in $AnimationPlayer.get_animation_list():
		for track in range($AnimationPlayer.get_animation(animation).get_track_count()):
			var start_vector = $AnimationPlayer.get_animation(animation).track_get_key_value(track,0)
			var end_vector = $AnimationPlayer.get_animation(animation).track_get_key_value(track,1)
			
			if typeof(start_vector) == TYPE_VECTOR2 and typeof(end_vector) == TYPE_VECTOR2:
				if start_vector == Vector2(0,0):
					if end_vector.x == 0:
						if end_vector.y > 0:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,1,Vector2(0,out_rect_position.y))
						else:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,1,Vector2(0,-out_rect_position.y))
							
					else:
						if end_vector.x > 0:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,1,Vector2(out_rect_position.x,0))
						else:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,1,Vector2(-out_rect_position.x,0))
							
				else:
					if start_vector.x == 0:
						if start_vector.y > 0:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,0,Vector2(0,out_rect_position.y))
						else:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,0,Vector2(0,-out_rect_position.y))
						
					else:
						if start_vector.x > 0:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,0,Vector2(out_rect_position.x,0))
						else:
							$AnimationPlayer.get_animation(animation).track_set_key_value(track,0,Vector2(-out_rect_position.x,0))
					
				
func change_debug(newDebug):
	global_var.is_debug = newDebug
	
	$GUI.visible = newDebug
	
	var camera = get_tree().get_nodes_in_group("camera")[0]
	if newDebug:
		camera.max_zoom = 100
	else:
		camera.max_zoom = 2
