extends Area2D


func hit(hitter):
	if get_parent().has_method("_hit"):
		get_parent()._hit(hitter)
