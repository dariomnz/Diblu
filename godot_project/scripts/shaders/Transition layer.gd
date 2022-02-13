extends CanvasLayer

#signal finished

onready var animationPlayer : AnimationPlayer = $Transition/TransitionPlayer

#
#func _ready():
#	animationPlayer.play("setup")
#
#func initialize():
#	play()
	
	
func play(transition_name:String):
	if animationPlayer.has_animation(transition_name):
		animationPlayer.play(transition_name)

func get_anim_length():
	return animationPlayer.current_animation_length
	
	
func _on_TransitionPlayer_animation_finished(_anim_name):
#	emit_signal("finished")
	queue_free()
