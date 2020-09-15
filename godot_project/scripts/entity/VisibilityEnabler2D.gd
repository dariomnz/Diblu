extends VisibilityEnabler2D


func _on_VisibilityEnabler2D_screen_exited():
	get_parent().set_physics_process(false)
	
func _on_VisibilityEnabler2D_screen_entered():
	get_parent().set_physics_process(true)
