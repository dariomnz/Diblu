extends Camera2D

var current_zoom = 0.5 setget update_zoom,get_zoom

var default_zoom = 0.5

var max_zoom = 1
var min_zoom = 0.1

func _input(_event):
	var increment = 1.10
	
	if Input.is_action_just_pressed("ui_scroll_down"):
		current_zoom *= increment
		if current_zoom > max_zoom:
			current_zoom = max_zoom
		update_zoom(current_zoom)
	if Input.is_action_just_pressed("ui_scroll_up"):
		current_zoom/=increment
		if current_zoom < min_zoom:
			current_zoom = min_zoom
		update_zoom(current_zoom)
	if Input.is_action_just_pressed("ui_scroll_click"):
		current_zoom = default_zoom
		update_zoom(current_zoom)
	
func update_zoom(newZoom):
	zoom.x=newZoom
	zoom.y=newZoom
	
	current_zoom=newZoom
	
	global_signal.emit_signal("on_change_zoom",get_zoom())
	

func get_zoom():
	return Vector2(current_zoom*2,current_zoom*2)
